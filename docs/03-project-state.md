# Project State — 3D AI Data Academy

Last updated: 2026-11-27 (Asia/Shanghai)

## Current mission

Build a durable, multi-agent-maintainable repository for six courses and 51 knowledge units. The learner uses the course for 3D / AI Data technical interviews and long-term engineering capability. Keep the complete knowledge chain and enable another AI to continue from repository evidence.

## Current unit and learner state

- Active unit: Course 3, Lesson 19 — Semantic Annotation & Part Labeling.
- Teaching status: taught in the current lesson delivery; individual assessment not verified.
- Latest explicit learner request: semantic annotation, instance segmentation, part labeling, point/face labels, automatic annotation and human review.
- Next planned unit: Lesson 20 — Data Quality Scoring, when the learner requests continuation.
- No learner quiz answers or practice results have been verified for any lesson. Do not infer mastery from teaching progress, code executed by an agent, or a file's presence.
- A learner request to continue authorizes the next lesson even if an earlier quiz is unsubmitted. Keep assessment outstanding without blocking requested teaching.

## Repository evidence and completeness

- Repository: https://github.com/lucinwen/3d ; default branch: main.
- Pre-update remote tree inspected on 2026-11-27 at commit `3909814f076e9a41a5e86e24afc8b4523250ccec`.
- That tree contains historical teaching files for Lessons 1–12, 14–16 and 18.
- It contains no Lesson 13 or Lesson 17 teaching file. The previous Lesson 17 index link and state assertion were incorrect; both are corrected in this update.
- Lesson 19 adds a complete newly authored teaching source, code example and source/asset manifests. Published in content commit `0346bb3695a727c86b59ebfb02c7f80c28d1c967`; all 18 release files were fetched from that exact commit and matched against the prepared UTF-8 source. See `archive/lessons/19/delivery-verification.json` for hashes and execution evidence.
- Lesson index, current roadmap and agent handoff are maintained together.

Historical structured teaching files include condensed or reconstructed material. They are not verified byte-for-byte chat exports. Exact transcript and original-image recovery for Lessons 1–18 remains incomplete. The fact that a historical lesson was taught does not prove that its original message or original image binary is now available.

For Lesson 19, distinguish the newly authored complete teaching source and its retained copy from an independently exported chat transcript. Use the per-lesson source manifest for exact scope, source hash, artifact inventory and verification state. Do not extend Lesson 19's evidence to earlier lessons.

## Curriculum progress

| Course | Units | Documentation | Learning assessment |
|---|---:|---|---|
| 1. Computer Graphics & 3D Assets | 7 | Lessons 1–7 teaching files exist | Not verified |
| 2. 3D Generation & Reconstruction | 9 | Lessons 8–12 and 14–16 exist; 13 missing | Not verified |
| 3. 3D Data Production & Quality | 9 | 17 source/file missing; 18 structured file exists; 19 current delivery; 20–25 planned | Not verified |
| 4. Model Evaluation & Benchmark | 8 | Planned | Not started |
| 5. Game Production & Technical Art | 9 | Planned | Not started |
| 6. Agent Harness & Engineering | 9 | Planned | Not started |

## Current lesson sequence

| Lesson | Topic | Evidence/state |
|---|---|---|
| 17 | 3D Data Acquisition & Dataset Construction | Previously taught in chat; repository teaching file missing; assessment unverified |
| 18 | Data Cleaning & Deduplication | Structured teaching file exists; historical verbatim/image recovery incomplete; assessment unverified |
| 19 | Semantic Annotation & Part Labeling | Current newly authored lesson and engineering example; assessment unverified |
| 20 | Data Quality Scoring | Next planned unit; not yet taught |

The course 3 sequence differs from the first roadmap. `docs/00-curriculum-roadmap.md` records the revision and maps every old topic to its current coverage. Format parsing, units/coordinates, texture dependencies and metadata standardization still require explicit coverage checks; do not mark a mapped topic complete merely because a related term appears in Lesson 18.

## Lesson 19 artifacts and focus

- `lessons/lesson-19-semantic-annotation-part-labeling.md`: complete current teaching source.
- `archive/lessons/19/transcript.md`: retained current teaching source, with exact provenance defined by the manifest.
- `archive/lessons/19/source-manifest.json` and `asset-manifest.csv`: origin, completeness and asset inventory.
- `examples/lesson19/`: executable synthetic-data example and its run instructions.
- Core concepts: semantic class, object instance, part class, part instance, hierarchy, point/vertex/face labels, geometry-index binding, annotation ontology, automatic proposals, review and adjudication, ignore masks, semantic/instance/part metrics.
- Synthetic examples and model probabilities are not measurements from the learner's project. Running the example does not validate a production annotator.

## Content risks to preserve in later work

- Thresholds and illustrative numbers are examples, not universal production standards.
- In Lesson 18, similarity/ANN retrieval does not prove duplicate identity or justify deletion; raw data and long-tail valid assets must remain traceable.
- In Lesson 19, object/part semantic IDs and instance IDs have different meanings. A connected component or material slot is not automatically a semantic part.
- Labels tied to point/vertex/face indices must bind to the exact geometry revision and element ordering. Remeshing or reindexing can invalidate correspondence.
- Ground-truth ignore masks must not let predictions hide mistakes by emitting ignore on valid ground truth.
- Automatic pre-labels, reviewer decisions and adjudicated ground truth must have separate provenance/status. High confidence is not a correctness guarantee.
- Metric numbers depend on representation, sampling, class set, ignore policy, matching and aggregation protocol.
- Never label summaries, image queries or replacement images as recovered historical originals.

## Next actions

1. Publication/readback completed for the Lesson 19 content release: [0346bb3](https://github.com/lucinwen/3d/commit/0346bb3695a727c86b59ebfb02c7f80c28d1c967). A following metadata commit records the verification; further edits require their own verification.
2. If the learner submits Lesson 19 answers or code, assess them and update learning state from evidence. If they request Lesson 20, teach it without inventing prior assessment.
3. Recover missing Lesson 13 and Lesson 17 teaching sources from original messages/exports before claiming exact archival.
4. Continue original-text and original-image recovery for Lessons 1–18; retain explicit missing/reference-only states.
5. Keep current source, code, answer explanations, diagrams and provenance together for every new lesson.
