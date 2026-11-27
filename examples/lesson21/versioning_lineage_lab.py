#!/usr/bin/env python3
"""Lesson 21: synthetic, single-writer snapshot and lineage lab; Python 3.10+."""
import argparse
import copy
import hashlib
import json
import os
import platform
import tempfile
import uuid
from collections import deque
from pathlib import Path


def canonical_bytes(value):
    """Our integer-only JSON convention, not a general RFC 8785 implementation."""
    def check(x):
        if x is None or type(x) in (str, int, bool):
            return
        if type(x) is list:
            for item in x:
                check(item)
        elif type(x) is dict and all(type(k) is str for k in x):
            for item in x.values():
                check(item)
        else:
            raise ValueError("unsupported_canonical_type")
    check(value)
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def sha256(blob):
    return hashlib.sha256(blob).hexdigest()


class Store:
    def __init__(self, root):
        self.root = root
        (root / "objects").mkdir(parents=True)

    def path(self, cid):
        if not isinstance(cid, str) or len(cid) != 64 or any(
                c not in "0123456789abcdef" for c in cid):
            raise ValueError("invalid_content_id")
        return self.root / "objects" / cid

    def put(self, blob):
        cid = sha256(blob)
        path = self.path(cid)
        if path.exists():
            if self.get(cid) != blob:
                raise ValueError("content_collision")
        else:
            # Exclusive create: normal API never overwrites an object.
            with path.open("xb") as file:
                file.write(blob)
        return cid

    def get(self, cid):
        try:
            blob = self.path(cid).read_bytes()
        except FileNotFoundError as error:
            raise ValueError("missing_object") from error
        if sha256(blob) != cid:
            raise ValueError("hash_mismatch")
        return blob

    def put_json(self, value):
        return self.put(canonical_bytes(value))

    def get_json(self, cid):
        return json.loads(self.get(cid))


def dependencies(obj):
    """Explicit dependency schema. Unknown kinds are rejected, never guessed."""
    kind = obj["kind"]
    if kind in ("mesh", "ontology", "quality_policy"):
        return []
    if kind == "annotation":
        return [obj["mesh_hash"], obj["ontology_hash"]]
    if kind == "recipe":
        return [obj["code_hash"], *obj["inputs"], obj["policy_hash"]]
    if kind == "release":
        return [obj["ontology_hash"], obj["quality_policy_hash"],
                obj["recipe_hash"], *[s[k] for s in obj["samples"]
                for k in ("source_hash", "mesh_hash", "annotation_hash")]]
    raise ValueError("unknown_artifact_kind")


def verify_closure(store, root_hash, opaque_hashes):
    """Read and verify every dependency, rejecting cycles; opaque=source code."""
    done, active, edges = set(), set(), set()
    def visit(cid):
        if cid in active:
            raise ValueError("dependency_cycle")
        if cid in done:
            return
        active.add(cid)
        blob = store.get(cid)
        refs = [] if cid in opaque_hashes else dependencies(json.loads(blob))
        for parent in refs:
            edges.add((parent, cid))
            visit(parent)
        active.remove(cid)
        done.add(cid)
    visit(root_hash)
    return done, edges


def validate_release(store, release, opaque_hashes):
    required = {"kind", "schema_version", "dataset_name", "ontology_hash",
                "quality_policy_hash", "recipe_hash", "split_version", "samples"}
    if not required <= release.keys() or release["kind"] != "release":
        raise ValueError("missing_release_fields")
    if release["schema_version"] != 1 or not release["samples"]:
        raise ValueError("invalid_release_schema")
    required_sample = {"asset_id", "family_id", "source_hash", "mesh_hash",
                       "annotation_hash", "split"}
    seen, family_splits = set(), {}
    ontology = store.get_json(release["ontology_hash"])
    if ontology["kind"] != "ontology":
        raise ValueError("wrong_ontology_kind")
    policy = store.get_json(release["quality_policy_hash"])
    if policy["kind"] != "quality_policy":
        raise ValueError("wrong_policy_kind")
    recipe = store.get_json(release["recipe_hash"])
    if recipe["kind"] != "recipe" or recipe["policy_hash"] != release["quality_policy_hash"]:
        raise ValueError("recipe_policy_mismatch")
    for sample in release["samples"]:
        if not required_sample <= sample.keys():
            raise ValueError("missing_sample_fields")
        if not all(isinstance(sample[k], str) and sample[k]
                   for k in ("asset_id", "family_id")):
            raise ValueError("invalid_sample_identity")
        if sample["asset_id"] in seen or sample["split"] not in ("train", "test"):
            raise ValueError("duplicate_asset_or_invalid_split")
        seen.add(sample["asset_id"])
        previous = family_splits.setdefault(sample["family_id"], sample["split"])
        if previous != sample["split"]:
            raise ValueError("family_split_leakage")
        mesh = store.get_json(sample["mesh_hash"])
        annotation = store.get_json(sample["annotation_hash"])
        if mesh["kind"] != "mesh" or annotation["kind"] != "annotation":
            raise ValueError("wrong_asset_kind")
        if annotation["mesh_hash"] != sample["mesh_hash"]:
            raise ValueError("annotation_mesh_binding_mismatch")
        if annotation["ontology_hash"] != release["ontology_hash"]:
            raise ValueError("annotation_ontology_mismatch")
        labels = annotation["face_labels"]
        if len(labels) != len(mesh["faces"]) or any(
                type(label) is not int or label not in ontology["label_ids"]
                for label in labels):
            raise ValueError("invalid_face_labels")
    # Store a candidate safely; it is not published until all checks pass.
    cid = store.put_json(release)
    closure, edges = verify_closure(store, cid, opaque_hashes)
    expected_inputs = {release["ontology_hash"], *[s[k] for s in release["samples"]
                       for k in ("source_hash", "mesh_hash", "annotation_hash")]}
    expected_config = {"samples": release["samples"], "split_version": release["split_version"]}
    if set(recipe["inputs"]) != expected_inputs or recipe["parameters"] != expected_config:
        raise ValueError("recipe_input_or_config_mismatch")
    return cid, closure, edges


def publish(store, release, opaque_hashes):
    cid, closure, edges = validate_release(store, release, opaque_hashes)
    current = store.root / "current.json"
    # Single-writer demo: same-filesystem rename exposes a whole pointer file.
    with tempfile.NamedTemporaryFile(dir=store.root, delete=False) as file:
        staged = Path(file.name)
        file.write(canonical_bytes({"release_hash": cid}))
        file.flush()
        os.fsync(file.fileno())
    try:
        os.replace(staged, current)
    finally:
        staged.unlink(missing_ok=True)
    return cid, closure, edges


def downstream(start, edges):
    children = {}
    for parent, child in edges:
        children.setdefault(parent, set()).add(child)
    visited, pending = {start}, deque([start])
    while pending:
        for child in children.get(pending.popleft(), ()):
            if child not in visited:
                visited.add(child)
                pending.append(child)
    return sorted(visited - {start})


def run_lab():
    with tempfile.TemporaryDirectory(prefix="lesson21-") as directory:
        store = Store(Path(directory))
        code_hash = store.put(Path(__file__).read_bytes())
        opaque = {code_hash}
        ontology_hash = store.put_json({"kind": "ontology", "version": "parts-v1",
                                       "label_ids": [0, 1], "names": ["base", "upper"]})
        mesh_a = {"kind": "mesh", "unit": "meter", "coordinates": "RH_Z_UP",
                  "vertices": [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]],
                  "faces": [[0, 1, 2], [0, 2, 3]]}
        mesh_b = copy.deepcopy(mesh_a)
        mesh_b["vertices"][2] = [2, 1, 0]
        samples = []
        for name, mesh, split in [("A", mesh_a, "train"), ("B", mesh_b, "test")]:
            raw_hash = store.put(json.dumps(mesh, indent=2).encode("utf-8"))
            mesh_hash = store.put_json(mesh)
            annotation_hash = store.put_json({"kind": "annotation",
                "mesh_hash": mesh_hash, "ontology_hash": ontology_hash,
                "face_labels": [0, 1]})
            samples.append({"asset_id": "asset-" + name, "family_id": "family-" + name,
                "source_hash": raw_hash, "mesh_hash": mesh_hash,
                "annotation_hash": annotation_hash, "split": split})
        source_hash, mesh_hash = samples[0]["source_hash"], samples[0]["mesh_hash"]
        recipes, releases, runs, edges = [], [], [], set()
        for threshold in (80, 85):
            policy_hash = store.put_json({"kind": "quality_policy",
                "version": "demo-threshold-" + str(threshold), "threshold": threshold,
                "note": "policy identity only; quality measurement is not implemented"})
            recipe = {"kind": "recipe", "operation": "assemble_snapshot", "code_hash": code_hash,
                "inputs": sorted({ontology_hash, *[s[k] for s in samples
                    for k in ("source_hash", "mesh_hash", "annotation_hash")]}),
                "policy_hash": policy_hash,
                "parameters": {"samples": samples, "split_version": "fixed-family-split-v1"},
                "environment": {"python": platform.python_version()}}
            recipe_hash = store.put_json(recipe)
            release = {"kind": "release", "schema_version": 1, "dataset_name": "tiny-parts",
                "ontology_hash": ontology_hash, "quality_policy_hash": policy_hash,
                "recipe_hash": recipe_hash, "split_version": "fixed-family-split-v1",
                "samples": sorted(samples, key=lambda s: s["asset_id"])}
            cid, closure, new_edges = publish(store, release, opaque)
            releases.append({"id": cid, "manifest": release, "closure_count": len(closure)})
            recipes.append(recipe_hash)
            edges.update(new_edges)
            runs.append({"run_id": str(uuid.uuid4()), "recipe_id": recipe_hash,
                         "output_id": cid, "status": "succeeded"})
        v1, v2 = releases[0]["id"], releases[1]["id"]
        repeat_id, _, _ = publish(store, copy.deepcopy(releases[1]["manifest"]), opaque)
        runs.append({"run_id": str(uuid.uuid4()), "recipe_id": recipes[1],
                     "output_id": repeat_id, "status": "succeeded"})
        checks = {}
        def must_reject(name, bad, expected):
            before = (store.root / "current.json").read_bytes()
            try:
                publish(store, bad, opaque)
            except ValueError as error:
                assert str(error) == expected, (name, str(error))
                checks[name] = {"blocked": True, "reason": str(error)}
            else:
                raise AssertionError("invalid release accepted: " + name)
            assert (store.root / "current.json").read_bytes() == before
            checks[name]["published_pointer_unchanged"] = True
        bad = copy.deepcopy(releases[1]["manifest"])
        del bad["samples"][0]["family_id"]
        must_reject("missing_family_id", bad, "missing_sample_fields")
        bad = copy.deepcopy(releases[1]["manifest"])
        bad["samples"][1]["family_id"] = "family-A"
        must_reject("cross_split_family", bad, "family_split_leakage")
        reordered = copy.deepcopy(mesh_a)
        reordered["faces"].reverse()
        reordered_hash = store.put_json(reordered)
        bad = copy.deepcopy(releases[1]["manifest"])
        bad["samples"][0]["mesh_hash"] = reordered_hash
        must_reject("same_face_count_wrong_binding", bad, "annotation_mesh_binding_mismatch")
        bad = copy.deepcopy(releases[1]["manifest"])
        bad["samples"][0]["source_hash"] = "0" * 64
        must_reject("missing_dependency", bad, "missing_object")
        bad = copy.deepcopy(releases[1]["manifest"])
        incomplete_recipe = store.get_json(bad["recipe_hash"])
        incomplete_recipe["inputs"] = []
        bad["recipe_hash"] = store.put_json(incomplete_recipe)
        must_reject("incomplete_recipe_inputs", bad, "recipe_input_or_config_mismatch")
        bad = copy.deepcopy(releases[1]["manifest"])
        changed_ontology = store.get_json(ontology_hash)
        changed_ontology["version"] = "parts-v2"
        bad["ontology_hash"] = store.put_json(changed_ontology)
        must_reject("ontology_binding_changed", bad, "annotation_ontology_mismatch")
        original = store.get(source_hash)
        # Fault injection deliberately bypasses Store's immutable API.
        store.path(source_hash).write_bytes(original + b" ")
        must_reject("corrupt_object_bytes", copy.deepcopy(releases[1]["manifest"]), "hash_mismatch")
        store.path(source_hash).write_bytes(original)
        rollback_id, _, _ = publish(store, releases[0]["manifest"], opaque)
        current_id = json.loads((store.root / "current.json").read_text())["release_hash"]
        affected = downstream(mesh_hash, edges)
        assert source_hash != mesh_hash and json.loads(store.get(source_hash)) == mesh_a
        assert v1 != v2 and recipes[0] != recipes[1] and repeat_id == v2
        assert runs[1]["run_id"] != runs[2]["run_id"]
        assert current_id == rollback_id == v1 and store.get(v2)
        assert v1 in affected and v2 in affected and samples[1]["mesh_hash"] not in affected
        return {"experiment": "actual execution on synthetic 2-asset/4-face data",
            "python_version": platform.python_version(), "code_sha256": code_hash,
            "serialization": "sorted UTF-8 JSON; str/int/bool/null/list/string-key dict; no floats",
            "asset_count": 2, "face_count": 4, "release_count": 2,
            "source_vs_canonical": {"asset_id": "asset-A", "family_id": "family-A",
                "source_hash": source_hash, "canonical_mesh_hash": mesh_hash,
                "same_parsed_geometry": True, "same_bytes": False},
            "releases": releases, "runs": runs, "fault_injection_checks": checks,
            "repeat_output_identical": repeat_id == v2, "distinct_run_ids": True,
            "rollback": {"current_release": current_id, "old_and_new_objects_retained": True},
            "lineage": {"edge_count": len(edges), "affected_by_mesh_a": affected,
                        "affected_release_count": sum(r["id"] in affected for r in releases)},
            "limits": ["single writer; no multi-writer CAS/lock or distributed transaction",
                       "temporary object store removed after run; report persists",
                       "policy versioning only; no quality scoring or license audit",
                       "explicit tiny JSON mesh; no DCC parser, semantic correctness, or near-duplicate discovery",
                       "file fsync+atomic rename; no full power-loss durability guarantee",
                       "run UUIDs vary; compare content IDs only under same source/Python environment"]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = json.dumps(run_lab(), ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
    print(report, end="")
