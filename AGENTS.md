# AGENTS.md — 3D AI Data Academy

This file is the mandatory entry point for every AI agent and human contributor working in this repository.

## Mission

Maintain a rigorous, cumulative learning and engineering curriculum for 3D AI Data, 3D generation/reconstruction, data quality, benchmarking, game production/technical art, and reliable Agent Harness systems. The repository must remain understandable and maintainable by a different AI agent with no access to prior chats.

## Mandatory onboarding

Before changing anything, read in this order:
1. README.md
2. docs/00-curriculum-roadmap.md
3. docs/01-teaching-standard.md
4. docs/02-practice-projects-and-acceptance.md
5. docs/03-project-state.md
6. docs/04-agent-handoff.md
7. lessons/README.md
8. The exact lesson(s) relevant to the task

Do not rely on chat summaries when repository sources are available. Do not assume a lesson is mastered merely because it is present.

## Curriculum invariants

- Preserve the six-course curriculum and its order.
- Teach exactly one knowledge unit per lesson.
- Do not merge, skip, or silently reorder units.
- Each knowledge unit must use: Concept → Principle → Data Structures → Algorithms → Engineering Implementation → Evaluation Metrics → Practical Case → Interview Follow-ups → Quiz.
- Explain fundamentals before advanced details; define every symbol, unit, coordinate convention, and assumption.
- Distinguish established facts, paper-specific methods, engineering recommendations, illustrative examples, and user-project measurements.
- Never fabricate experiments, benchmark scores, citations, repository contents, or successful execution.
- Mark illustrative numbers and thresholds explicitly as examples.
- Do not claim geometric accuracy metrics when no valid ground-truth geometry exists.
- Explain metric limitations and protocol dependencies.

## Content quality requirements

- Use precise technical language; provide Chinese explanations and English terminology on first use.
- Include equations with variable definitions, units, assumptions, and interpretation.
- Explain data schemas and coordinate systems explicitly.
- Code must be labelled as runnable, pseudocode, or conceptual. Runnable code must state dependencies, input assumptions, commands, expected output, and known limitations.
- Provide failure modes, diagnostics, and alternative methods.
- Include citations/references for papers and official tool documentation when adding research claims.
- Preserve prior lesson material; improve by adding corrections/addenda rather than silently deleting substantive content.
- Do not confuse view synthesis with geometric reconstruction, rendering quality with asset quality, or a generated plausible backside with observed ground truth.

## Collaboration workflow

For every task:
1. Inspect current files and git state.
2. State the exact files to change.
3. Make focused changes; avoid overwriting unrelated work.
4. Verify created/updated files by fetching them from GitHub after commit.
5. Update docs/03-project-state.md and docs/04-agent-handoff.md when lesson progress, decisions, or next tasks change.
6. Update lessons/README.md when lessons are added.
7. Report commit links and verification honestly.

For parallel agents:
- Assign non-overlapping file ownership.
- One integrator reviews consistency, citations, notation, and duplication.
- Never let multiple agents overwrite the same file concurrently.
- All outputs must be merged and checked by the integrator.

## Learner state

The learner is preparing for technical interviews involving 3D generation, AI Data, evaluation, and production workflows. Teach deeply and sequentially. Use relevant prior project examples only when supported by the project record. Do not exaggerate the learner's technical implementation or claim unverified outcomes.

## Completion definition

A lesson is not "mastered" until the learner has completed its quiz/open questions and demonstrated understanding in explanation or implementation. Use these states:
- planned
- drafted
- taught
- practiced
- assessed
- mastered
- needs-review

Repository presence means documented, not necessarily mastered.
\n\n## Verbatim archive rule\nWhen the learner asks for verbatim archival, preserve the exact original assistant message and asset binaries without paraphrase. If the exact source or image binary cannot be accessed, label it missing or reconstructed; never claim a reconstructed lesson is verbatim. Follow archive/README.md. Keep transcripts, image asset manifests, image prompts, Q&A, quizzes and code mapped to their lesson and original order.\n