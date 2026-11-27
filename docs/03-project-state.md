# Project State — 3D AI Data Academy

Last updated: 2026-11-27

## Current mission

Build a durable, multi-agent-maintainable learning and engineering repository for six courses and 51 knowledge units. The learner's target use includes Tencent Hunyuan 3D / AI Data technical interview preparation and long-term engineering capability.

## Current repository state

- Repository: https://github.com/lucinwen/3d
- Default branch: main
- Six-course roadmap: documented.
- Teaching standard: documented.
- Practice/capstone plan: documented.
- Lessons 1–12: structured teaching archives exist; Lesson 13 SDF was taught in chat but its lesson file is pending recovery; Lessons 14 Diffusion, 15 Shape Generation and 16 Retopology have structured teaching files.
- Agent onboarding and handoff protocol: being established.
- Lesson 16 (Retopology): current teaching unit.

## Important completeness caveat

Lessons 1–7 were reconstructed as structured summaries from available prior-course context, not verified as verbatim transcripts of every historical teaching message. Lessons 8–10 were condensed for repository archiving. Lesson 13 (SDF) has been taught in chat but is not yet archived as a lesson file. The archive policy in archive/README.md distinguishes verbatim sources from reconstructed notes and missing image binaries. Do not claim the first ten lessons are byte-for-byte or detail-for-detail complete. Future work should reconcile each lesson against original conversation exports when available and add missing derivations, examples, code, references, quiz explanations, and exercises.

## Curriculum progress

| Course | Planned units | Repository documentation | Learning mastery |
|---|---:|---|---|
| 1. Computer Graphics & 3D Assets | 7 | Lessons 1–7 documented | Not yet individually assessed in this repository |
| 2. 3D Generation & Reconstruction | 9 | Lessons 8–16 in progress; 8–12 and 14–16 documented; 13 taught but awaiting original-source recovery | Not yet individually assessed |
| 3. 3D Data Production & Quality | 9 | Planned | Not started |
| 4. Model Evaluation & Benchmark | 8 | Planned | Not started |
| 5. Game Production & Technical Art | 9 | Planned | Not started |
| 6. Agent Harness & Engineering | 9 | Planned | Not started |

## Current lesson sequence

- Lesson 8: Text-to-3D — documented.
- Lesson 9: Image-to-3D — documented.
- Lesson 10: Multi-view Reconstruction — documented.
- Lesson 11: NeRF — documented; assessment not verified.
- Lesson 12: 3D Gaussian Splatting — documented; assessment not verified.
- Lesson 13: SDF — taught in chat; original lesson file pending recovery.
- Lesson 14: Diffusion — documented; assessment not verified.
- Lesson 15: Shape Generation — documented; assessment not verified.
- Lesson 16: Retopology — documented; assessment not verified; current active unit.
- Next: Course 3, Lesson 17 — 3D Data Acquisition and Dataset Construction.

## Known content risks to review

- Ensure all camera pose conventions are explicit (world-to-camera vs camera-to-world).
- Ensure monocular SfM scale ambiguity is not confused with metric reconstruction.
- Ensure CLIP similarity is not presented as a 3D geometry metric.
- Ensure point-cloud-to-mesh algorithms are described with their input assumptions.
- Ensure SDF, NeRF and 3DGS are not treated as interchangeable representations.
- Ensure all code examples state coordinate, scale and data assumptions.

## Immediate priorities

1. Complete the Retopology quiz and open-ended interview questions before moving to Course 3, Lesson 17.
2. Recover and archive exact original transcripts for Lessons 1–16; do not substitute summaries.
3. Recover original image binaries where available; otherwise retain prompts/references and mark binaries missing.
4. Archive Lesson 13 (SDF) from its original source.
5. Add reproducible experiments and versioned engineering examples.
6. Keep this state file and handoff file current.
