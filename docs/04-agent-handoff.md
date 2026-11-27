# Agent Handoff Protocol

## Purpose
Enable another AI agent to continue the academy without depending on the original chat.

## Start-of-task checklist
1. Read AGENTS.md.
2. Read docs/03-project-state.md.
3. Read docs/00-curriculum-roadmap.md and docs/01-teaching-standard.md.
4. Read lessons/README.md and the current lesson.
5. Read archive/README.md before any verbatim transcript/image recovery.
6. Inspect recent commits and user-provided changes where available.
7. Identify the exact current unit. Do not ask the learner to repeat known context.

## Current handoff snapshot
- Repository: lucinwen/3d
- Active unit: Course 3, Lesson 18 — Data Cleaning & Deduplication.
- Lesson 17: taught; assessment not verified.
- Lesson 18: taught and structured teaching file archived; quiz and open-ended answers pending.
- Next unit after Lesson 18 assessment: Lesson 19 — Semantic Annotation & Part Labeling.
- Teaching format: Concept → Principle → Data Structure → Algorithm → Engineering → Metrics → Case Study → Interview Questions → Quiz.
- Learner prefers one unit at a time and deep explanations, not compressed glossaries.

## Lesson 18 archive
- lessons/lesson-18-data-cleaning-deduplication.md
- Topics: anomaly taxonomy, statistical outlier detection, exact/geometric/semantic near-duplicate, canonicalization, fingerprints, Chamfer, ICP, ANN, duplicate graphs, Precision/Recall, non-destructive cleaning, distributed pipeline.
- Quiz and interview responses have not yet been submitted or assessed.

## Verbatim archive rules
- Follow archive/README.md.
- Preserve exact original assistant/user text, code, formulas, tables, questions, answers, quiz options, explanations, citations and message order.
- Label every artifact verbatim, reconstructed, missing, asset-original or asset-reference-only.
- Never claim a query string, thumbnail, citation or newly generated image is the original binary image.
- Do not silently correct a verbatim transcript; add a separate correction note.
- Verify each committed file by fetching it again.

## How to continue
1. Teach the current unit only.
2. Follow all nine teaching sections.
3. Do not advance before the learner's current assessment is addressed.
4. After teaching, mark taught; after practice, practiced/assessed/mastered only when evidence supports it.
5. Commit lesson file and update index, project state and handoff.
6. Clearly state remaining source/image recovery work.

## Multi-agent roles
- Curriculum Architect: roadmap and dependencies.
- Research Agent: papers, official docs, terminology and citations.
- Technical Instructor: derivations and lesson content.
- Engineering Agent: validate code, dependencies and commands.
- Evaluation Agent: metrics, benchmark validity and edge cases.
- Integrator: consistency, citations, repo state and final verification.

Use separate branches or disjoint files for parallel work. Never allow multiple agents to concurrently edit the same lesson file.

## Required handoff note
Record date, task owner, files changed, commit SHA/link, what was verified, what remains incomplete, next exact action, and learner status.

## Prompt for a new AI
"Read AGENTS.md and the onboarding documents in order. Continue the current active unit from docs/03-project-state.md. Preserve the six-course roadmap and nine-part teaching standard. Do not invent prior work or move to the next unit before assessment. Update lesson index, state and handoff, and verify all GitHub files."
