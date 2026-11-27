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
- Active unit: Course 3, Lesson 20 — Data Quality Scoring.
- Teaching: complete nine-part lesson and runnable synthetic-data lab.
- Learner state: taught, not individually assessed.
- Next planned unit: Lesson 21 — Data Versioning & Data Lineage.
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

## Historical archive status
Lesson 13 and Lesson 17 teaching files remain missing. Lessons 1–18 original transcripts and image binaries remain incompletely recovered. Newly authored lesson sources are authored-current-turn, not historical verbatim exports.

## Deliverables
- lessons/lesson-20-data-quality-scoring.md
- examples/lesson20/quality_scoring_lab.py, README.md and example-report.json
- archive/lessons/20 source and asset manifests, request copy and Mermaid diagram
- Updated README, lesson index, project state and handoff

Teach exactly one requested unit. Mark taught after delivery; mark practiced/assessed/mastered only when learner evidence supports it. Read committed files back from GitHub before claiming publication success.
