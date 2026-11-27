# Project State — 3D AI Data Academy

Last updated: 2026-11-28 (Asia/Shanghai)

## Current unit and learner state

- Active unit: Course 3, Lesson 21 — Data Versioning & Data Lineage.
- Teaching status: taught in the current delivery; individual assessment not verified.
- Next planned unit: Lesson 22 — Training Dataset Construction, when requested.
- No learner quiz answers or practice results have been verified. Do not infer mastery from teaching progress, code executed by an agent, or file presence.

## Repository

- Repository: https://github.com/lucinwen/3d ; default branch: main.
- Lesson 19 content commit: 0346bb3695a727c86b59ebfb02c7f80c28d1c967; verification metadata commit: 64fcf00c2628a4249d9da5046a774366e6f2c9db.
- Lessons 13 and 17 teaching files remain missing. Original transcripts/images for Lessons 1–18 remain incompletely recovered.
- Course 3 sequence: 17 acquisition/construction, 18 cleaning/deduplication, 19 semantic/part annotation, 20 quality scoring, 21 versioning/lineage, 22 training dataset construction, 23 hard sample mining, 24 synthetic data/augmentation, 25 integrated data pipeline.
- Format/coordinate/units/texture metadata standardization remains a coverage gap to check.

## Lesson 20 artifacts

- lessons/lesson-20-data-quality-scoring.md: complete nine-section lesson.
- examples/lesson20/quality_scoring_lab.py: runnable synthetic Python example, standard library only.
- examples/lesson20/README.md and example-report.json: instructions and retained report; execution provenance is not reverified in this update.
- archive/lessons/20/: retained authored source, request copy, flowchart source and provenance manifests.
- Guardrails: hard gates cannot be offset by soft scores; missing evidence is not zero or full score; raw weighted score is not calibrated probability; task profiles differ; calibration needs independent reference labels; protect long-tail diversity.
- Synthetic examples do not establish real-world quality or learner mastery.

**Verification scope note:** 本次未复核第 20 讲实验报告的执行来源与聊天逐字一致性，沿用文件存在不构成验证。本次任务是第 21 讲，不据此更改第 20 讲原文或宣称补档完成。

## Lesson 21 artifacts and teaching boundaries

- lessons/lesson-21-data-versioning-and-lineage.md: nine-part teaching source on data versioning and lineage.
- examples/lesson21/versioning_lineage_lab.py, README.md and example-report.json: synthetic versioning lab, commands, report and explicit limitations. Actual execution evidence must be read from the report and accompanying instructions.
- archive/lessons/21/: prepared teaching transcript, source/asset manifests, request, citation map and diagram source. The source is authored-current-turn; an independently exported chat transcript is a separate claim.
- Publication verification: use archive/lessons/21/delivery-verification.json when present. Its commit, path and hash comparisons define the verified scope; this state file alone does not prove remote readback success.
- Distinguish logical asset/family identity, byte-level artifact digest, recipe identity, execution identity and dataset release identity.
- Bind point/face labels to the exact geometry representation and ontology. Equal element counts do not establish correspondence after reordering or retopology.
- Freeze data, labels, ontology, quality policy and split membership for a release; preserve dependencies and explicit transformation parameters.
- Trace upstream causes and downstream impact through a versioned dependency graph. Validate a candidate before changing a published pointer; rollback does not itself revoke data or erase downstream model influence.
- A deterministic content record is not a guarantee of identical training results across hardware, software or stochastic execution. State the level of reproducibility actually checked.

## Next actions

1. If the learner submits Lesson 20 or Lesson 21 answers or code, assess that submission and update learning state from evidence.
2. If the learner requests Lesson 22, teach training dataset construction without inventing prior assessment.
3. Recover missing Lesson 13 and Lesson 17 sources from original messages/exports.
4. Continue original-text and original-image recovery for Lessons 1–18.
5. Keep lesson source, code, report, diagram source, provenance and handoff together for every new lesson.
