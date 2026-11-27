# Project State — 3D AI Data Academy

Last updated: 2026-11-27

## Current mission
Build a durable, multi-agent-maintainable learning and engineering repository for six courses and 51 knowledge units. The learner's target use includes Tencent Hunyuan 3D / AI Data technical interview preparation and long-term engineering capability.

## Current repository state
- Repository: https://github.com/lucinwen/3d
- Default branch: main
- Six-course roadmap and nine-part teaching standard documented.
- Lessons 1–18 have index entries.
- Structured teaching files exist for Lessons 1–12 and 14–18.
- Lesson 13 SDF was taught in chat; exact lesson source recovery remains pending.
- Lesson 18 Data Cleaning & Deduplication is the current active teaching unit.
- Agent onboarding and handoff protocol documented.

## Important completeness caveat
Some earlier lessons were reconstructed or condensed for repository maintenance and are not verified verbatim transcripts. Exact transcript and original image recovery is a separate task tracked in archive/README.md. Do not claim that every historical assistant message or original image binary has been archived verbatim unless each source has been recovered and checked. The current lesson files are structured teaching archives, not byte-for-byte exports of chat UI messages.

## Curriculum progress
| Course | Planned units | Repository documentation | Learning mastery |
|---|---:|---|---|
| 1. Computer Graphics & 3D Assets | 7 | Lessons 1–7 indexed | Not yet individually assessed in this repository |
| 2. 3D Generation & Reconstruction | 9 | Lessons 8–16 indexed; Lesson 13 source pending | Not yet individually assessed |
| 3. 3D Data Production & Quality | 9 | Lessons 17–18 documented; remaining units planned | Not yet individually assessed |
| 4. Model Evaluation & Benchmark | 8 | Planned | Not started |
| 5. Game Production & Technical Art | 9 | Planned | Not started |
| 6. Agent Harness & Engineering | 9 | Planned | Not started |

## Current lesson sequence
- Lesson 17: 3D Data Acquisition & Dataset Construction — taught; assessment not verified.
- Lesson 18: Data Cleaning & Deduplication — documented and taught; quiz and open-ended answers pending.
- Next after Lesson 18 assessment: Lesson 19, Semantic Annotation & Part Labeling.

## Lesson 18 key topics
File/geometry/topology/point-cloud/appearance/semantic anomalies; Bounding Box, Z-score, MAD, IQR, Mahalanobis, Isolation Forest, LOF; SHA256; Canonicalization; Geometry Fingerprint; Chamfer, ICP, multi-view similarity; ANN; Duplicate Graph; Precision/Recall/F1; non-destructive cleaning; million-scale pipeline.

## Known content risks to review
- Thresholds in examples are illustrative, not universal production standards.
- Distinguish exact file duplicate from geometric duplicate and semantic near-duplicate.
- Similarity is not sufficient evidence to delete an asset.
- ANN retrieves candidates; it does not prove geometric identity.
- Cleaning rules must be task-specific and preserve long-tail/rare valid samples.
- Preserve raw data and record repair provenance.
- Distinguish structured lesson archives from verbatim transcripts and original image binaries.

## Immediate priorities
1. Complete Lesson 18 quiz and high-level interview questions; assess answers before advancing.
2. Continue exact transcript recovery for Lessons 1–18; do not substitute summaries.
3. Recover original image binaries where available; otherwise mark image assets as reference-only/missing.
4. Recover and archive Lesson 13 SDF from its original source.
5. Add validated, reproducible experiments and versioned engineering examples.
6. Keep lesson index, project state and handoff current.
