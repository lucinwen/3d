"""Lesson 20: task-aware 3D data quality scoring.
Python 3.10+, standard library only. Synthetic teaching data, not production evidence.
"""
import argparse
import json
from pathlib import Path

PROFILES = {
    "static_classification": {
        "weights": {"geometry": .25, "topology": .10, "appearance": .05, "annotation": .30, "provenance": .15, "task_fit": .15},
        "required": ["geometry", "annotation", "provenance", "task_fit"],
        "min_coverage": .80, "accept": 85.0, "review": 70.0,
    },
    "character_animation": {
        "weights": {"geometry": .15, "topology": .20, "appearance": .05, "annotation": .20, "provenance": .15, "task_fit": .25},
        "required": ["geometry", "topology", "annotation", "provenance", "task_fit"],
        "min_coverage": .90, "accept": 85.0, "review": 70.0,
    },
}
ASSETS = [
    {"asset_id": "A-clean-prop", "scores": {"geometry": 94, "topology": 90, "appearance": 70, "annotation": 92, "provenance": 100, "task_fit": 90}, "gates": {"parse_success": True, "license_approved": True, "geometry_binding_valid": True}},
    {"asset_id": "B-license-unknown", "scores": {"geometry": 99, "topology": 96, "appearance": 95, "annotation": 98, "provenance": 100, "task_fit": 99}, "gates": {"parse_success": True, "license_approved": False, "geometry_binding_valid": True}},
    {"asset_id": "C-static-only", "scores": {"geometry": 96, "topology": 55, "appearance": 85, "annotation": 90, "provenance": 100, "task_fit": 92}, "gates": {"parse_success": True, "license_approved": True, "geometry_binding_valid": True}},
    {"asset_id": "D-missing-annotation", "scores": {"geometry": 90, "topology": 88, "appearance": None, "annotation": None, "provenance": 100, "task_fit": 84}, "gates": {"parse_success": True, "license_approved": True, "geometry_binding_valid": True}},
    {"asset_id": "E-balanced-character", "scores": {"geometry": 88, "topology": 94, "appearance": 75, "annotation": 91, "provenance": 100, "task_fit": 96}, "gates": {"parse_success": True, "license_approved": True, "geometry_binding_valid": True}},
]
POLICY_VERSION = "lesson20-demo-policy-1.0"

def evaluate(asset, profile_name):
    profile = PROFILES[profile_name]
    weights, scores = profile["weights"], asset["scores"]
    total_weight = sum(weights.values())
    observed_weight = weighted_sum = 0.0
    contributions, missing = {}, []
    for name, weight in weights.items():
        value = scores.get(name)
        if value is None:
            missing.append(name)
            contributions[name] = None
            continue
        if not isinstance(value, (int, float)) or not 0 <= value <= 100:
            raise ValueError(f"{asset['asset_id']}: invalid score for {name}")
        observed_weight += weight
        weighted_sum += weight * value
        contributions[name] = round(weight * value, 4)
    raw_score = weighted_sum / observed_weight if observed_weight else None
    coverage = observed_weight / total_weight
    failed_gates = [name for name, passed in asset["gates"].items() if not passed]
    missing_required = [name for name in profile["required"] if scores.get(name) is None]
    reasons = []
    if failed_gates:
        decision = "quarantine"
        reasons.extend("hard_gate_failed:" + name for name in failed_gates)
    elif missing_required:
        decision = "review"
        reasons.extend("required_dimension_missing:" + name for name in missing_required)
    elif coverage < profile["min_coverage"]:
        decision = "review"
        reasons.append("weight_coverage_below_minimum")
    elif raw_score >= profile["accept"]:
        decision = "accept"
    elif raw_score >= profile["review"]:
        decision = "review"
        reasons.append("score_in_review_band")
    else:
        decision = "reject"
        reasons.append("score_below_review_floor")
    return {
        "asset_id": asset["asset_id"], "task_profile": profile_name,
        "policy_version": POLICY_VERSION,
        "raw_score": round(raw_score, 3) if raw_score is not None else None,
        "weight_coverage": round(coverage, 3),
        "dimension_contributions": contributions,
        "missing_dimensions": missing, "failed_hard_gates": failed_gates,
        "missing_required_dimensions": missing_required,
        "decision": decision, "decision_reasons": reasons,
        "calibrated_probability": None,
        "calibration_note": "No independent reference labels; raw score is not a probability."
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    results = [evaluate(asset, profile) for asset in ASSETS for profile in PROFILES]
    report = {
        "experiment": "synthetic task-aware scoring demonstration; not production evidence",
        "policy_version": POLICY_VERSION, "profiles": PROFILES, "results": results,
        "checks": {
            "failed_license_gate_never_accepted": all(r["decision"] != "accept" for r in results if r["asset_id"] == "B-license-unknown"),
            "same_asset_task_scores_can_differ": len({r["raw_score"] for r in results if r["asset_id"] == "A-clean-prop"}) > 1,
            "missing_required_annotation_routes_review": all(r["decision"] == "review" for r in results if r["asset_id"] == "D-missing-annotation"),
            "no_calibrated_probability_fabricated": all(r["calibrated_probability"] is None for r in results),
        }
    }
    assert all(report["checks"].values()), report["checks"]
    payload = json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")
    print(payload)

if __name__ == "__main__":
    main()
