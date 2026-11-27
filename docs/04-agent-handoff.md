# Agent Handoff Protocol

## Purpose

This file lets a new AI agent continue work without depending on the original chat history.

## Start-of-task checklist

1. Read AGENTS.md.
2. Read docs/03-project-state.md.
3. Read docs/00-curriculum-roadmap.md and docs/01-teaching-standard.md.
4. Read lessons/README.md and the current lesson.
5. Inspect recent commits and any uncommitted/user-provided changes if the connected environment exposes them.
6. Identify the learner's exact request and current unit. Do not ask the learner to repeat information already recorded here.

## Current handoff snapshot

- Active repository: lucinwen/3d
- Active curriculum: six courses, 51 units.
- Active unit: Course 2, Lesson 16 — Retopology.
- Prior lessons: Lessons 1–12 have structured teaching archives; Lesson 13 (SDF) taught in chat but exact source file pending; Lesson 14 (Diffusion) has a structured teaching archive. Exact transcript and binary image recovery is tracked in archive/README.md. See archive-completeness caveat in docs/03-project-state.md.
- Teaching format: nine-part unit structure.
- Next planned unit after Lesson 16 assessment: Course 3, Lesson 17 — 3D Data Acquisition and Dataset Construction.
- Learner prefers one unit at a time and deep explanations, not compressed glossaries.

## How to continue a lesson

1. Teach the current unit only.
2. Follow all nine sections from docs/01-teaching-standard.md.
3. If the learner asks for a correction, update the relevant lesson and record the correction.
4. Do not advance automatically before the learner's quiz/open questions are addressed.
5. After the lesson, update status to taught. After learner practice, update practiced/assessed/mastered as evidence supports.
6. Commit lesson source and update the lesson index, state, and this handoff snapshot.

## Multi-agent task allocation

Recommended roles:
- Curriculum Architect: maintains roadmap, sequence, learning dependencies.
- Research Agent: verifies papers, official docs, terminology and citations.
- Technical Instructor: writes the lesson and derives equations.
- Engineering Agent: validates code, dependencies, commands and sample outputs.
- Evaluation Agent: checks metrics, benchmark design, statistical validity and edge cases.
- Editor/Integrator: checks consistency, duplication, language, citations and repo state.

Use separate branches or disjoint files for parallel work. The Integrator owns final merges. Never allow multiple agents to concurrently edit the same lesson file.

## Required handoff note after each task

Record:
- Date.
- Agent/task owner (if known).
- Files changed.
- Commit SHA/link.
- What was verified.
- What remains incomplete.
- Next exact action.
- Learner status (not started / taught / practiced / assessed / mastered / needs-review).

## Prompt for a new AI

"Read AGENTS.md and the onboarding documents in the specified order. Continue the current active unit from docs/03-project-state.md. Preserve the six-course curriculum and nine-part teaching standard. Do not repeat completed content, invent prior work, or move to the next unit before the learner completes the current unit's assessment. When finished, update lesson index, project state, handoff notes, and verify the GitHub files."
