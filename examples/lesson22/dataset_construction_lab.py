#!/usr/bin/env python3
"""Lesson 22: synthetic metadata splitting and leakage audit; Python 3.10+."""
import argparse
import copy
import hashlib
import json
import math
import platform
import random
import statistics
from collections import Counter, defaultdict
from pathlib import Path

SPLITS = ("train", "validation", "test")
SEED = 22


def canonical(value):
    """Local JSON encoding contract; not a complete RFC 8785 implementation."""
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def make_rows():
    """120 synthetic asset families; 3 imagined views x 2 LOD records per family."""
    rows = []
    for category, base_mm in (("chair", 1000), ("table", 1500), ("lamp", 800)):
        for family_index in range(40):
            family = f"{category}-{family_index:03d}"
            for view in range(3):
                for lod in range(2):
                    rows.append({
                        "sample_id": f"{family}/view-{view}/lod-{lod}",
                        "asset_id": family, "family_id": family, "class_name": category,
                        "source_id": f"synthetic-source-{family_index % 2}",
                        "view_id": view, "lod": lod,
                        "bbox_diagonal_mm": base_mm + 3 * family_index,
                    })
    return sorted(rows, key=lambda row: row["sample_id"])


def validate_rows(rows):
    required = {"sample_id", "asset_id", "family_id", "class_name", "source_id",
                "view_id", "lod", "bbox_diagonal_mm"}
    seen, family_classes = set(), {}
    for row in rows:
        if not required <= row.keys():
            raise ValueError("missing_row_fields")
        if not all(isinstance(row[k], str) and row[k] for k in
                   ("sample_id", "asset_id", "family_id", "class_name", "source_id")):
            raise ValueError("invalid_identity")
        if row["sample_id"] in seen:
            raise ValueError("duplicate_sample_id")
        seen.add(row["sample_id"])
        old = family_classes.setdefault(row["family_id"], row["class_name"])
        if old != row["class_name"]:
            raise ValueError("mixed_class_group_not_supported")
        value = row["bbox_diagonal_mm"]
        if type(value) not in (int, float) or not math.isfinite(value) or value <= 0:
            raise ValueError("invalid_feature")


def row_random_split(rows, seed=SEED):
    """Deliberately wrong protocol for unseen-family evaluation."""
    ids = sorted(row["sample_id"] for row in rows)
    random.Random(seed).shuffle(ids)
    train_n, validation_n = 70 * len(ids) // 100, 15 * len(ids) // 100
    return {"train": sorted(ids[:train_n]),
            "validation": sorted(ids[train_n:train_n + validation_n]),
            "test": sorted(ids[train_n + validation_n:])}


def grouped_stratified_split(rows, seed=SEED):
    """Teaching special case: one class/group, equal rows/group in main fixture."""
    validate_rows(rows)
    families = defaultdict(list)
    for row in rows:
        families[row["family_id"]].append(row)
    by_class = defaultdict(list)
    for family, members in families.items():
        by_class[members[0]["class_name"]].append(family)
    result = {name: [] for name in SPLITS}
    rng = random.Random(seed)
    for category in sorted(by_class):
        groups = sorted(by_class[category])
        if len(groups) < 3:
            raise ValueError("infeasible_class_group_support:" + category)
        rng.shuffle(groups)
        validation_n = max(1, 15 * len(groups) // 100)
        test_n = max(1, 15 * len(groups) // 100)
        train_n = len(groups) - validation_n - test_n
        buckets = (groups[:train_n], groups[train_n:train_n + validation_n],
                   groups[train_n + validation_n:])
        for split, selected in zip(SPLITS, buckets):
            result[split].extend(row["sample_id"] for group in selected
                                 for row in families[group])
    return {name: sorted(ids) for name, ids in result.items()}


def validate_assignment(rows, assignment, require_group_isolation=True):
    validate_rows(rows)
    if set(assignment) != set(SPLITS) or any(not assignment[s] for s in SPLITS):
        raise ValueError("missing_or_empty_split")
    row_map = {row["sample_id"]: row for row in rows}
    assigned, family_split = set(), {}
    for split in SPLITS:
        for sample_id in assignment[split]:
            if sample_id not in row_map:
                raise ValueError("unknown_assigned_sample")
            if sample_id in assigned:
                raise ValueError("duplicate_or_cross_assigned_sample")
            assigned.add(sample_id)
            family = row_map[sample_id]["family_id"]
            prior = family_split.setdefault(family, split)
            if require_group_isolation and prior != split:
                raise ValueError("family_split_leakage")
    if assigned != set(row_map):
        raise ValueError("unassigned_sample")


def summarize(rows, assignment):
    row_map = {row["sample_id"]: row for row in rows}
    groups = {s: {row_map[i]["family_id"] for i in assignment[s]} for s in SPLITS}
    family_splits = defaultdict(set)
    for split, group_ids in groups.items():
        for family in group_ids:
            family_splits[family].add(split)
    support = {}
    for split in SPLITS:
        subset = [row_map[i] for i in assignment[split]]
        class_groups = defaultdict(set)
        for row in subset:
            class_groups[row["class_name"]].add(row["family_id"])
        support[split] = {
            "rows": len(subset), "families": len(groups[split]),
            "class_rows": dict(sorted(Counter(r["class_name"] for r in subset).items())),
            "class_families": {c: len(g) for c, g in sorted(class_groups.items())},
        }
    test_seen = sum(row_map[i]["family_id"] in groups["train"] for i in assignment["test"])
    return {"support": support,
            "cross_split_family_count": sum(len(s) > 1 for s in family_splits.values()),
            "train_test_family_intersection": len(groups["train"] & groups["test"]),
            "train_validation_family_intersection": len(groups["train"] & groups["validation"]),
            "validation_test_family_intersection": len(groups["validation"] & groups["test"]),
            "test_rows_with_training_family": test_seen,
            "test_family_exposure_rate": test_seen / len(assignment["test"])}


def fit_preprocessor(rows, assignment, fit_ids):
    """Permit exactly the frozen training members, never validation/test rows."""
    validate_assignment(rows, assignment)
    if len(fit_ids) != len(set(fit_ids)) or set(fit_ids) != set(assignment["train"]):
        raise ValueError("preprocessor_fit_scope_must_equal_train")
    row_map = {row["sample_id"]: row for row in rows}
    values = [row_map[i]["bbox_diagonal_mm"] for i in sorted(fit_ids)]
    std = statistics.pstdev(values)
    if std == 0:
        raise ValueError("zero_variance_feature")
    return {"feature": "bbox_diagonal_mm", "input_unit": "mm",
            "fit_split": "train", "fit_count": len(fit_ids),
            "fit_member_ids_sha256": digest(sorted(fit_ids)),
            "mean": statistics.fmean(values), "population_std": std,
            "output_unit": "dimensionless"}


def transformed_split_means(rows, assignment, fitted):
    lookup = {r["sample_id"]: r["bbox_diagonal_mm"] for r in rows}
    return {s: statistics.fmean((lookup[i] - fitted["mean"]) / fitted["population_std"]
                               for i in assignment[s]) for s in SPLITS}


def augment_from_train(rows, assignment, parent_id):
    """Metadata-only scalar scaling; this does not transform a real mesh."""
    lookup = {r["sample_id"]: r for r in rows}
    if parent_id not in lookup or parent_id not in assignment["train"]:
        raise ValueError("augmentation_parent_not_train")
    child = copy.deepcopy(lookup[parent_id])
    child.update(sample_id=parent_id + "/aug-scale-1.01", parent_id=parent_id,
                 split="train", augmentation="synthetic_scalar_scale_1.01")
    child["bbox_diagonal_mm"] *= 1.01
    return child


def identity_lookup_accuracy(rows, assignment):
    """Intentional shortcut baseline: family->label lookup, else train majority."""
    lookup = {r["sample_id"]: r for r in rows}
    train = [lookup[i] for i in assignment["train"]]
    memory = {r["family_id"]: r["class_name"] for r in train}
    counts = Counter(r["class_name"] for r in train)
    fallback = sorted(counts, key=lambda c: (-counts[c], c))[0]
    correct = sum(memory.get(lookup[i]["family_id"], fallback) == lookup[i]["class_name"]
                  for i in assignment["test"])
    return {"correct": correct, "test_rows": len(assignment["test"]),
            "accuracy": correct / len(assignment["test"]),
            "unknown_family_fallback": fallback}


def run_lab():
    rows = make_rows()
    bad_split = row_random_split(rows)
    good_split = grouped_stratified_split(rows)
    validate_assignment(rows, bad_split, require_group_isolation=False)
    validate_assignment(rows, good_split)
    manifest = {"schema_version": "split-manifest/1",
        "task": "closed-set category prediction for previously unseen asset families",
        "dataset_sha256": digest(rows), "seed": SEED,
        "method": "single-class-family stratified shuffle v1",
        "target_group_ratios": {"train": 0.70, "validation": 0.15, "test": 0.15},
        "group_registry": "explicit-synthetic-family-registry-v1",
        "membership": good_split}
    frozen_hash = digest(manifest)
    stats = fit_preprocessor(rows, good_split, good_split["train"])
    augmented = [augment_from_train(rows, good_split, i) for i in good_split["train"][:3]]
    assert all(r["family_id"] == next(x["family_id"] for x in rows
               if x["sample_id"] == r["parent_id"]) and r["split"] == "train"
               for r in augmented)
    changed_test = copy.deepcopy(rows)
    held_out = set(good_split["validation"]) | set(good_split["test"])
    for row in changed_test:
        if row["sample_id"] in held_out:
            row["bbox_diagonal_mm"] += 10000
    independent_stats = fit_preprocessor(changed_test, good_split, good_split["train"])
    assert independent_stats == stats
    faults = {}
    def must_reject(name, action, expected):
        try:
            action()
        except ValueError as error:
            assert str(error) == expected, (name, str(error))
            faults[name] = {"blocked": True, "reason": str(error)}
        else:
            raise AssertionError("invalid case accepted: " + name)
        assert digest(manifest) == frozen_hash
    missing = copy.deepcopy(rows)
    del missing[0]["family_id"]
    must_reject("missing_family", lambda: grouped_stratified_split(missing), "missing_row_fields")
    duplicated = rows + [copy.deepcopy(rows[0])]
    must_reject("duplicate_sample_id", lambda: grouped_stratified_split(duplicated),
                "duplicate_sample_id")
    unassigned = copy.deepcopy(good_split)
    unassigned["train"].pop()
    must_reject("unassigned_sample", lambda: validate_assignment(rows, unassigned), "unassigned_sample")
    cross = copy.deepcopy(good_split)
    cross["test"].append(cross["train"][0])
    must_reject("cross_assigned_sample", lambda: validate_assignment(rows, cross),
                "duplicate_or_cross_assigned_sample")
    must_reject("family_leakage", lambda: validate_assignment(rows, bad_split), "family_split_leakage")
    must_reject("fit_on_all_rows", lambda: fit_preprocessor(rows, good_split,
                [r["sample_id"] for r in rows]), "preprocessor_fit_scope_must_equal_train")
    must_reject("augment_test_parent", lambda: augment_from_train(rows, good_split,
                good_split["test"][0]), "augmentation_parent_not_train")
    rare = [copy.deepcopy(r) for r in rows if r["family_id"] in ("lamp-000", "lamp-001")]
    for row in rare:
        row["class_name"] = "rare"
    must_reject("rare_class_only_two_groups", lambda: grouped_stratified_split(rare),
                "infeasible_class_group_support:rare")
    assert good_split == grouped_stratified_split(list(reversed(rows)))
    return {"experiment": "actual execution; synthetic metadata only, not a trained 3D model",
        "python_version": platform.python_version(),
        "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "seed": SEED, "candidate_rows": len(rows), "candidate_families": 120,
        "input_schema": {"feature_shape": [len(rows), 1], "feature_unit": "millimeters",
                        "views_per_family": 3, "lods_per_view": 2, "classes": ["chair", "lamp", "table"]},
        "row_random": summarize(rows, bad_split), "grouped_stratified": summarize(rows, good_split),
        "split_manifest": manifest, "split_manifest_sha256": frozen_hash,
        "fitted_preprocessor": stats, "standardized_split_means": transformed_split_means(rows, good_split, stats),
        "held_out_feature_shift_mm": 10000,
        "train_fitted_stats_unchanged_after_held_out_shift": independent_stats == stats,
        "counterfactual_wrong_all_data_mean_after_shift": statistics.fmean(
            r["bbox_diagonal_mm"] for r in changed_test),
        "augmented_train_metadata_examples": augmented,
        "identity_lookup_toy": {"warning": "Family-ID shortcut diagnostic, not geometry learning or production accuracy",
            "row_random": identity_lookup_accuracy(rows, bad_split),
            "grouped_stratified": identity_lookup_accuracy(rows, good_split)},
        "fault_injection_checks": faults, "frozen_manifest_unchanged_after_faults": digest(manifest) == frozen_hash,
        "same_input_reordered_same_split": True,
        "limits": ["synthetic metadata; no actual mesh parsing, rendering or neural training",
            "known family IDs; no near-duplicate discovery or multi-relation component construction",
            "single-class groups; main fixture has equal group sizes; not a general constrained optimizer",
            "no time/domain/OOD holdout, calibration split, confidence intervals or prospective evaluation",
            "mean/std is an explicit one-feature example; fitted from base train rows before augmentation",
            "JSON encoding and random shuffle are pinned by source and Python version; not cross-language canonicalization"]}
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    text = json.dumps(run_lab(), ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")

