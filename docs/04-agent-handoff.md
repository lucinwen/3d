# Agent Handoff Protocol

## Purpose
Enable another AI agent to continue the academy using repository evidence, not assumptions from prior chat.

## Start-of-task checklist
1. Read AGENTS.md and mandatory onboarding files in order.
2. Read docs/03-project-state.md, the relevant lesson and source manifest.
3. Inspect the live remote branch/tree and recent commits.
4. Read archive/README.md before historical transcript/image recovery.
5. Identify the learner's current request and assessment state.

## Current handoff snapshot

- Date: 2026-11-28 (Asia/Shanghai).
- Repository: lucinwen/3d, default branch main.
- Active unit: Course 3, Lesson 22 — Training Dataset Construction.
- Teaching: current nine-part lesson with a synthetic dataset-construction lab; inspect its actual report and execution evidence for supported claims and limitations.
- Learner state: taught, not individually assessed.
- Next planned unit: Lesson 23 — Hard Sample Mining.
- Format: Concept → Principle → Data Structures → Algorithms → Engineering → Metrics → Case Study → Interview Follow-ups → Quiz.

## Lesson 20 guardrails

1. Hard gates cannot be offset by a high soft score.
2. Missing, not applicable, failed measurement and measured-zero are distinct states.
3. A weighted raw score is not a calibrated pass probability.
4. Task profiles determine required dimensions, weights and acceptance policy.
5. Calibration requires independent reference labels and group-aware data separation.
6. Report false accept, false reject, coverage, selective risk and subgroup/long-tail retention.
7. Preserve evidence, policy version, tool version, geometry/annotation revision and decision reasons.
8. Synthetic lab results are not production benchmark evidence or learner mastery.

本次未复核第 20 讲实验报告的执行来源与聊天逐字一致性，沿用文件存在不构成验证。保留其原文和来源记录；如后续开展核验，用独立补充说明记录结果，不静默改写历史转录。

## Lesson 21 guardrails

1. Keep logical asset/family IDs separate from artifact hashes. Identical bytes do not prove identical logical provenance; different bytes do not prove unrelated assets.
2. Separate recipe/configuration identity, run identity and observed output hashes. A recipe is a procedure to attempt, not proof of its execution or result.
3. Bind point/face annotations to exact geometry ordering and ontology versions. Element-count equality is necessary for some formats but is not sufficient correspondence validation.
4. Record data, annotation, ontology, quality policy and split versions in an immutable release manifest. Human-friendly names and current pointers must resolve to exact manifests.
5. Use explicit inputs, transformations and outputs for lineage; preserve both upstream traceability and downstream impact analysis. Shared source families require split-leakage checks.
6. Validate hashes, references and required bindings before publication. A failed candidate must leave the previously published pointer usable.
7. Rollback changes which valid release is selected. Revocation, authorized deletion and any treatment of trained model influence require their own recorded actions.
8. Name the reproducibility level being tested: available artifacts, verified bytes, rerunnable transformations or statistical model behavior. Do not infer cross-platform determinism from a fixed seed.
9. Retain the complete current teaching source and all answers, diagram source, code and report. Source-copy equality does not prove an independently exported delivered chat transcript.

## Lesson 22 guardrails

1. Start from the target population, input/output task and generalization claim. A fixed split ratio alone cannot define a valid evaluation.
2. Distinguish records/views from independent source assets, families, scenes, people or acquisition sessions. State which relationships are forbidden across each split for this task.
3. Group related records before partitioning; preserve the transitive closure of required separation constraints. Do not break a group to repair class proportions, and do not claim general feasibility from a simple balanced synthetic example.
4. Separate identity/duplicate discovery for split governance from fitting task preprocessors. Learned population statistics, feature selection and training transformations must follow the declared development protocol; held-out test information must not influence model development.
5. Freeze split manifests and group-registry versions. Resampling and training augmentation operate within training membership; derived records retain parent identity and allowed split.
6. Validation supports model, hyperparameter and policy selection; test estimates the prespecified target after choices are fixed. Calibration/threshold fitting requires a clear development subset or cross-fitting design. Repeated adaptive test use changes its evidential status.
7. Report class/source support, row and group counts, known overlaps and distribution differences. Natural-distribution and balanced evaluations have different estimands; specify aggregation and weighting.
8. Zero known group intersections is a bounded audit result, not a guarantee that unknown duplicates, metadata shortcuts or hidden pretraining contamination do not exist.
9. Preserve task-specific exceptions explicitly: seen-scene novel-view evaluation and unseen-object generalization allow different shared information. Never label every shared scene as leakage without reading the task contract.
10. Keep synthetic engineering checks separate from actual 3D training/generalization evidence. Learner state stays unassessed until the learner supplies evidence.

## Historical archive status
Lesson 13 and Lesson 17 teaching files remain missing. Lessons 1–18 original transcripts and image binaries remain incompletely recovered. Newly authored lesson sources are authored-current-turn, not historical verbatim exports.

## Retained Lesson 20 deliverables

- lessons/lesson-20-data-quality-scoring.md
- examples/lesson20/quality_scoring_lab.py, README.md and example-report.json
- archive/lessons/20 source and asset manifests, request copy and Mermaid diagram
- Updated README, lesson index, project state and handoff

## Lesson 21 deliverables and publication evidence

- lessons/lesson-21-data-versioning-and-lineage.md
- examples/lesson21/versioning_lineage_lab.py, README.md and example-report.json
- archive/lessons/21/: teaching transcript, request, source/asset manifests, citation map and diagram source
- archive/lessons/21/delivery-verification.json: generated by the integrating agent after remote readback; inspect this file for the exact verified commit and paths rather than assuming success from this checklist
- Updated README, lesson index, roadmap, project state and handoff

Lesson 22 deepens split design and sampling while reusing the immutable release and family-identity principles from Lesson 21. The prior Lesson 21 content and metadata commits are bce314ccc4a11a5da6211613b94f617e09f3d4a1 and 520f6f3ba37130e2e7a0dc5ca90e8ac9886bcb2c; consult its evidence record rather than treating these references as a new full re-verification.

## Lesson 22 deliverables and publication evidence

- lessons/lesson-22-training-dataset-construction.md
- examples/lesson22/dataset_construction_lab.py, README.md and example-report.json
- archive/lessons/22/: complete teaching source, exact user request, source/asset manifests, citation map and diagram source
- archive/lessons/22/execution-verification.json: actual execution evidence produced by the integrating agent
- archive/lessons/22/delivery-verification.json: actual committed-file readback scope, produced after publication; do not claim success from this checklist alone
- Updated README, lesson index, roadmap, project state and handoff

When continuing with Lesson 23, teach hard sample mining from training/development failures while keeping held-out test data outside the adaptive improvement loop. Preserve split identities and trace newly mined samples to their source families before admission. The standardization coverage gap and missing Lesson 13/17 sources remain open tasks.

Teach exactly one requested unit. Mark taught after delivery; mark practiced/assessed/mastered only when learner evidence supports it. Read committed files back from GitHub before claiming publication success.
