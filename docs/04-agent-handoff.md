# Agent Handoff Protocol

## Purpose

Enable another AI agent to continue the academy without depending on the original chat. User instructions and the latest verified repository state determine the task; older notes are evidence, not a reason to block a clear new request.

## Start-of-task checklist

1. Read `AGENTS.md` and its mandatory onboarding files in order.
2. Read `docs/03-project-state.md`, the relevant lesson and its source manifest.
3. Inspect the current remote branch/tree and recent commits before changing files.
4. Read `archive/README.md` before historical transcript/image recovery.
5. Identify the learner's exact current request and known assessment state. Do not ask them to repeat context already available.
6. State the files to change; assign disjoint ownership when working in parallel.

## Current handoff snapshot

- Date: 2026-11-27 (Asia/Shanghai).
- Repository: `lucinwen/3d`, default branch `main`.
- Active unit: Course 3, Lesson 19 — Semantic Annotation & Part Labeling.
- Teaching: current delivery covers the complete nine-part lesson and a runnable synthetic-data lab.
- Learner state: taught, not individually assessed. No submitted learner quiz/practice evidence has been verified for any lesson.
- Next planned unit: Lesson 20 — Data Quality Scoring. Continue when explicitly requested; an unsubmitted quiz does not cancel the learner's authorization to continue.
- Format: Concept → Principle → Data Structures → Algorithms → Engineering → Metrics → Case Study → Interview Follow-ups → Quiz.
- Preference: one knowledge unit at a time, deep explanation, complete source preservation and maintainable handoff.

## Repository corrections made with Lesson 19

The pre-update remote tree at `3909814f076e9a41a5e86e24afc8b4523250ccec` contains Lessons 1–12, 14–16 and 18. **Lesson 13 and Lesson 17 teaching files are missing.** Earlier Lesson 17 links/state claims were not evidence of upload. The index and state now identify those gaps without pretending to reconstruct original text.

The first roadmap numbered standardization as 18, cleaning as 19, deduplication as 20 and annotation as 21. The learner subsequently explicitly requested 17 acquisition/construction, 18 cleaning/deduplication and 19 semantic/part annotation. The roadmap now records that revision and the old-to-current topic coverage mapping. Units 20–25 remain planned, not user-assessed or already taught. Check missing standardization details before declaring that topic complete.

README navigation is updated. Literal escaped newlines at the end of `AGENTS.md` are formatted as real Markdown lines without dropping their substantive instructions.

## Lesson 19 deliverables

- `lessons/lesson-19-semantic-annotation-part-labeling.md`.
- `archive/lessons/19/transcript.md` and per-lesson source/asset manifests.
- `examples/lesson19/annotation_lab.py` and `examples/lesson19/README.md`.
- Updated `README.md`, `AGENTS.md`, roadmap, lesson index, project state and this handoff.

The per-lesson manifest must say exactly whether a retained text is the newly authored teaching source or a verified export of the delivered chat. Do not call a second local copy proof of a recovered historical transcript. Preserve every section, equation, code snippet, diagram source, interview answer and quiz explanation in the current teaching source. Historical Lessons 1–18 still need original-source recovery.

## Lesson 19 technical guardrails

1. Keep semantic class, object instance, part semantic class and part instance separate. ID magnitude has no geometric meaning.
2. Part boundaries are an ontology decision; connected components, OBJ objects and material slots are only possible cues.
3. Bind labels to geometry revision, coordinate convention and point/vertex/face ordering. Preserve provenance when sampling or transferring labels.
4. Separate unannotated, ambiguous, background, absent part, not visible and evaluation ignore policies.
5. Keep automatic predictions and human-approved labels distinct; record model, confidence, reviewer, policy version and edits.
6. Report per-class/per-part performance and small-part/boundary failures. Semantic accuracy alone cannot validate object instances.
7. Exclude only protocol-defined invalid ground-truth elements from evaluation; a model's ignore prediction on valid ground truth remains a mistake.
8. Treat synthetic lab outputs as checks of a teaching implementation, not real-world annotation accuracy or learner mastery.

## Archival rules

- Follow `archive/README.md`; preserve exact original message and artifact order where the original is available.
- Label the source status explicitly; never substitute a reconstruction for the requested verbatim archive.
- A query string, caption, thumbnail, reference URL or newly generated replacement is not the original binary image.
- Add technical corrections in a separate note; do not silently modify a preserved original transcript.
- Read committed files back from GitHub and compare content/hashes before reporting a successful exact upload.
- Do not publish unrelated private source documents simply because they were attached to the chat.

## How to continue

1. Fulfill the learner's requested unit with all nine sections.
2. Mark taught after delivery. Mark practiced/assessed/mastered only when learner evidence supports it.
3. If answers are provided, evaluate reasoning and implementation; keep unresolved gaps explicit.
4. If the learner requests the next lesson, continue it and retain outstanding assessments separately.
5. Save complete lesson content, code, diagram/asset sources, answers and provenance; update index/state/handoff.
6. Verify GitHub writes and report the actual commit, tested commands, limitations and remaining recovery gaps.

## Multi-agent roles

Curriculum Architect maintains dependencies; Research Agent checks primary sources; Instructor writes the full teaching chain; Engineering Agent runs the example; Evaluation Agent checks protocols and edge cases; Integrator checks consistency and publishes. Use disjoint files or isolated branches; the integrator alone performs final publication.

## Publication and verification record

Content commit: [0346bb3695a727c86b59ebfb02c7f80c28d1c967](https://github.com/lucinwen/3d/commit/0346bb3695a727c86b59ebfb02c7f80c28d1c967). All 18 files were fetched from that exact GitHub commit and matched the complete prepared UTF-8 source. The lab was rerun by the integrator with exit code 0; its JSON matched the committed report. Exact file hashes, geometry/ignore checks, citation roundtrip scope and historical gaps are recorded in `archive/lessons/19/delivery-verification.json`. This verification note and report are published in a following metadata commit. The final chat UI has not been independently exported and compared; do not extend file-integrity evidence into such a claim.

## Prompt for a new AI

"Read AGENTS.md and onboarding files, inspect the live repository, and continue the learner's explicit request. Current unit is Lesson 19; next planned unit is Lesson 20. Preserve all nine teaching sections and full source artifacts. Do not invent learner mastery or historical archive completeness. Lesson 13 and Lesson 17 teaching sources remain missing. Preserve course sequence revision history, update index/state/handoff, and verify GitHub files after publication."
