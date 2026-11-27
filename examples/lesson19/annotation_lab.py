"""Lesson 19: synthetic, order-bound 3D annotations and honest semantic IoU.

Run from the repository root:
    python examples/lesson19/annotation_lab.py
    python examples/lesson19/annotation_lab.py --output /tmp/lesson19-report.json

Dependency: NumPy. No model, network request, or external asset is used.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path

import numpy as np


IGNORE = -1


def geometry_digest(vertices: np.ndarray, faces: np.ndarray) -> str:
    """An order-sensitive digest; NOT an invariant geometric duplicate hash."""
    h = hashlib.sha256(b"lesson19-ordered-triangle-mesh-v1\0")
    for array, dtype in ((vertices, "<f8"), (faces, "<i8")):
        canonical = np.ascontiguousarray(array, dtype=dtype)
        h.update(json.dumps(list(canonical.shape)).encode("ascii") + b"\0")
        h.update(canonical.tobytes(order="C"))
    return h.hexdigest()


def require_binding(vertices: np.ndarray, faces: np.ndarray, expected: str) -> None:
    if geometry_digest(vertices, faces) != expected:
        raise ValueError("Geometry/index order changed: annotation binding rejected")


def sample_labeled_surface(vertices, faces, face_semantic, face_reviewed,
                           expected_digest, count=12, seed=19):
    """Uniform surface-area sampling; each triangle has ONE semantic label.

    Coordinates are metres in a right-handed asset-local system, +Z up.
    A triangle crossing a true semantic boundary violates this input contract.
    """
    vertices = np.asarray(vertices, dtype=np.float64)
    faces = np.asarray(faces)
    semantic = np.asarray(face_semantic)
    reviewed = np.asarray(face_reviewed)
    if vertices.ndim != 2 or vertices.shape[1] != 3 or not np.isfinite(vertices).all():
        raise ValueError("Expected finite vertices[N,3]")
    if faces.ndim != 2 or faces.shape[1] != 3 or len(faces) == 0:
        raise ValueError("Expected nonempty triangular faces[F,3]")
    if not np.issubdtype(faces.dtype, np.integer):
        raise ValueError("Face indices must be integers")
    if faces.min() < 0 or faces.max() >= len(vertices):
        raise ValueError("Face index outside vertex array")
    if semantic.shape != (len(faces),) or not np.issubdtype(semantic.dtype, np.integer):
        raise ValueError("Expected integer semantic label per face")
    if np.any(semantic < IGNORE):
        raise ValueError("This demo allows only -1 or nonnegative class IDs")
    if reviewed.shape != (len(faces),) or reviewed.dtype != np.bool_:
        raise ValueError("Expected boolean reviewed flag per face")
    if not isinstance(count, int) or count <= 0:
        raise ValueError("Sample count must be a positive integer")
    require_binding(vertices, faces, expected_digest)

    triangles = vertices[faces]
    areas = 0.5 * np.linalg.norm(np.cross(triangles[:, 1] - triangles[:, 0],
                                        triangles[:, 2] - triangles[:, 0]), axis=1)
    if not np.isfinite(areas).all() or areas.sum() <= 0:
        raise ValueError("No finite positive surface area")
    rng = np.random.default_rng(seed)
    source_face_id = rng.choice(len(faces), size=count, p=areas / areas.sum())
    r, s = rng.random((2, count))
    root = np.sqrt(r)
    barycentric = np.column_stack((1 - root, root * (1 - s), root * s))
    points = (triangles[source_face_id] * barycentric[:, :, None]).sum(axis=1)
    point_labels = semantic[source_face_id]
    return {
        "points": points,
        "source_face_id": source_face_id,
        "barycentric": barycentric,
        "semantic_id": point_labels,
        "reviewed": reviewed[source_face_id],
        "train_mask": reviewed[source_face_id] & (point_labels != IGNORE),
        "face_area_m2": areas,
        "geometry_digest": expected_digest,
        "seed": seed,
    }


def semantic_metrics(ground_truth, prediction, class_count=2):
    """GT -1 is excluded; prediction -1 on valid GT is an error/abstention.

    Confusion rows are GT classes; columns are predicted classes plus abstain.
    mIoU averages classes with nonzero union (a stated protocol choice).
    """
    gt, pred = np.asarray(ground_truth), np.asarray(prediction)
    if gt.ndim != 1 or gt.shape != pred.shape or class_count <= 0:
        raise ValueError("Expected equal one-dimensional label arrays")
    for labels in (gt, pred):
        if not np.issubdtype(labels.dtype, np.integer):
            raise ValueError("Labels must be integers")
        if np.any((labels < IGNORE) | (labels >= class_count)):
            raise ValueError("Invalid semantic ID")
    valid = gt != IGNORE
    gt, pred = gt[valid], pred[valid]
    confusion = np.zeros((class_count, class_count + 1), dtype=np.int64)
    pred_columns = np.where(pred == IGNORE, class_count, pred)
    np.add.at(confusion, (gt, pred_columns), 1)
    true_positive = np.diag(confusion[:, :class_count])
    gt_support = confusion.sum(axis=1)  # Includes prediction abstentions.
    pred_support = confusion[:, :class_count].sum(axis=0)
    union = gt_support + pred_support - true_positive
    iou = [float(tp / un) if un else None for tp, un in zip(true_positive, union)]
    measured = [value for value in iou if value is not None]
    return {
        "confusion_columns": [*range(class_count), "abstain"],
        "confusion": confusion.tolist(),
        "iou": iou,
        "mean_iou": float(np.mean(measured)) if measured else None,
        "accuracy": float(true_positive.sum() / len(gt)) if len(gt) else None,
        "valid_gt_count": int(len(gt)),
        "prediction_abstentions_on_valid_gt": int(np.sum(pred == IGNORE)),
    }


def run_demo():
    # Three disconnected, artificial triangles. They are NOT a realistic chair.
    # Their areas are 1, 2, 1 square metres; class IDs are teaching-only IDs.
    vertices = np.array([[0, 0, 0], [2, 0, 0], [0, 1, 0],
                         [0, 0, 1], [4, 0, 1], [0, 1, 1],
                         [0, 0, 2], [2, 0, 2], [0, 1, 2]], dtype=float)
    faces = np.arange(9, dtype=np.int64).reshape(3, 3)
    face_semantic = np.array([0, 1, IGNORE], dtype=np.int32)
    face_reviewed = np.array([True, True, False])
    digest = geometry_digest(vertices, faces)
    samples = sample_labeled_surface(vertices, faces, face_semantic,
                                     face_reviewed, digest)

    # Independent reconstruction checks correspondence; a rendering is not enough.
    reconstructed = np.einsum("ni,nij->nj", samples["barycentric"],
                              vertices[faces[samples["source_face_id"]]])
    np.testing.assert_allclose(reconstructed, samples["points"])
    np.testing.assert_allclose(samples["barycentric"].sum(axis=1), 1)
    assert np.all(samples["barycentric"] >= 0)
    assert np.array_equal(samples["semantic_id"], face_semantic[samples["source_face_id"]])
    assert not np.any(samples["train_mask"] & (samples["semantic_id"] == IGNORE))

    # Same visible geometry, different face order: old labels must be rejected.
    binding_rejected = False
    try:
        require_binding(vertices, faces[::-1], digest)
    except ValueError:
        binding_rejected = True
    assert binding_rejected

    # A known prelabel that has not been reviewed is also excluded in this policy.
    unreviewed = sample_labeled_surface(vertices, faces, face_semantic,
                                        np.zeros(3, dtype=bool), digest)
    assert not unreviewed["train_mask"].any()

    # A moderate sample verifies the different-sized faces do not get equal weight.
    many = sample_labeled_surface(vertices, faces, face_semantic,
                                  face_reviewed, digest, count=10000)
    frequencies = np.bincount(many["source_face_id"], minlength=3) / 10000
    np.testing.assert_allclose(frequencies, [0.25, 0.5, 0.25], atol=0.025)

    metrics = semantic_metrics([0, 0, 1, 1, IGNORE], [0, IGNORE, 1, 0, 1])
    np.testing.assert_allclose(metrics["iou"], [1 / 3, 1 / 2])
    assert metrics["valid_gt_count"] == 4 and metrics["accuracy"] == 0.5
    assert semantic_metrics([IGNORE], [0])["mean_iou"] is None

    # Four points belonging to two chairs; a merged prediction has perfect semantics.
    gt_instance = np.array([11, 11, 12, 12])
    merged_instance = np.full(4, 77)
    pair_iou = [float(np.sum((gt_instance == i) & (merged_instance == 77)) /
                      np.sum((gt_instance == i) | (merged_instance == 77))) for i in (11, 12)]
    assert pair_iou == [0.5, 0.5]
    return {
        "experiment": "synthetic teaching demonstration; not a model benchmark",
        "environment": {"python": platform.python_version(), "numpy": np.__version__},
        "schema_version": "lesson19-demo-v1",
        "geometry_revision": "toy-three-triangles-v1",
        "geometry_digest": digest,
        "coordinates": {"units": "metres", "handedness": "right", "up": "+Z", "space": "asset-local"},
        "class_names": {"0": "seat_demo", "1": "back_demo", "-1": "unlabeled"},
        "face_area_m2": samples["face_area_m2"].tolist(),
        "seed": samples["seed"],
        "samples": {key: samples[key].tolist() for key in
                    ("points", "source_face_id", "barycentric", "semantic_id", "reviewed", "train_mask")},
        "checks": {"barycentric_reconstruction": "passed", "source_label_mapping": "passed",
                   "unlabeled_excluded": "passed", "unreviewed_excluded": "passed",
                   "reordered_mesh_rejected": binding_rejected,
                   "surface_sampling_frequencies_10000": frequencies.tolist(),
                   "all_gt_ignored_returns_null": "passed"},
        "semantic_metric_example": metrics,
        "merged_instance_counterexample": {
            "semantic_accuracy": 1.0, "gt_instances": 2, "predicted_instances": 1,
            "pair_iou": pair_iou, "matches_at_strict_iou_gt_0_5": 0,
            "note": "This is a toy matching counterexample, not a complete PQ/AP evaluator."},
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, help="Optionally save the full JSON report")
    args = parser.parse_args()
    report = json.dumps(run_demo(), ensure_ascii=False, indent=2, allow_nan=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report + "\n", encoding="utf-8")
    print(report)
