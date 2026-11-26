# Project State — 3D AI Data Academy

Last updated: 2026-11-26

## Current mission

Build a durable, multi-agent-maintainable learning and engineering repository for six courses and 51 knowledge units. The learner's target use includes Tencent Hunyuan 3D / AI Data technical interview preparation and long-term engineering capability.

## Current repository state

- Repository: https://github.com/lucinwen/3d
- Default branch: main
- Six-course roadmap: documented.
- Teaching standard: documented.
- Practice/capstone plan: documented.
- Lessons 1–12: archived in structured form; Lesson 13 was taught in chat and awaits repository archival; Lesson 14 Diffusion is archived.
- Agent onboarding and handoff protocol: being established.
- Lesson 14 (Diffusion): current teaching unit.

## Important completeness caveat

Lessons 1–7 were reconstructed as structured summaries from available prior-course context, not verified as verbatim transcripts of every historical teaching message. Lessons 8–10 were also condensed for repository archiving. Lesson 13 (SDF) has been taught in chat but is not yet archived as a lesson file. Do not claim the first ten lessons are byte-for-byte or detail-for-detail complete. Future work should reconcile each lesson against original conversation exports when available and add missing derivations, examples, code, references, quiz explanations, and exercises.

## Curriculum progress

| Course | Planned units | Repository documentation | Learning mastery |
|---|---:|---|---|
| 1. Computer Graphics & 3D Assets | 7 | Lessons 1–7 documented | Not yet individually assessed in this repository |
| 2. 3D Generation & Reconstruction | 9 | Lessons 8–14 in progress; 8–12 and 14 documented, 13 taught but awaiting archival | Not yet individually assessed |
| 3. 3D Data Production & Quality | 9 | Planned | Not started |
| 4. Model Evaluation & Benchmark | 8 | Planned | Not started |
| 5. Game Production & Technical Art | 9 | Planned | Not started |
| 6. Agent Harness & Engineering | 9 | Planned | Not started |

## Current lesson sequence

- Lesson 8: Text-to-3D — documented.
- Lesson 9: Image-to-3D — documented.
- Lesson 10: Multi-view Reconstruction — documented.
- Lesson 11: NeRF — documented; assessment not verified.
- Lesson 12: 3D Gaussian Splatting — documented; assessment not verified; current active unit.
- Next: Lesson 13, SDF.

## Known content risks to review

- Ensure all camera pose conventions are explicit (world-to-camera vs camera-to-world).
- Ensure monocular SfM scale ambiguity is not confused with metric reconstruction.
- Ensure CLIP similarity is not presented as a 3D geometry metric.
- Ensure point-cloud-to-mesh algorithms are described with their input assumptions.
- Ensure SDF, NeRF and 3DGS are not treated as interchangeable representations.
- Ensure all code examples state coordinate, scale and data assumptions.

## Immediate priorities

1. Complete NeRF lesson with full derivation and practical implementation.
2. Add a NeRF minimal experiment using a small multi-view dataset and a reproducible configuration.
3. Complete learner quiz and open-ended interview questions before moving to Lesson 12.
4. Reconcile lesson 1–10 archives with original source conversations where available.
5. Add references and versioned engineering examples.
6. Keep this state file and handoff file current.
