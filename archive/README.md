# Historical Lesson Archive Policy

## User requirement

The learner requires every lesson output to be preserved verbatim, including explanations, formulas, code, interview questions and answers, quizzes, explanations, image references/prompts, and other teaching artifacts.

## Non-negotiable distinctions

Every archived artifact must be labelled as one of:
- `verbatim`: exact source text recovered from the original assistant response or a user-provided export. Do not edit, summarize, normalize, or silently correct it.
- `reconstructed`: recreated from summaries, notes, or partial context. Never describe it as verbatim.
- `missing`: source is not available yet.
- `asset-original`: exact original binary image/video/file asset is available and archived.
- `asset-reference-only`: only the original prompt/query, citation, or description is available; the binary asset is not available.

## Image handling

An inline image rendered by the chat UI is not automatically a downloadable source file. An image search query, AsyncImage query, URL, caption, or thumbnail is not the original generated asset. Preserve the exact image prompt/query and original ordering where available, but mark the binary as missing unless the exact image file can be retrieved and verified. Never fabricate a sandbox path or claim a prompt is the original image.

## Transcript handling

- Preserve complete assistant teaching messages in their original order.
- Preserve all Q&A, quiz options, correct answers, explanations, code blocks, citations, and wording.
- Do not silently fix technical mistakes in a verbatim transcript. Add a separate correction note with rationale and date.
- Include source conversation/date/message reference when available.
- Keep an index mapping lesson number to transcript, images/assets, code and quiz files.
- If only a partial transcript is available, record the exact missing range and do not fill it with invented text.

## Current recovery status (based on currently accessible historical context)

- Lessons 1–4: some original long-form text is recoverable from historical conversation context; Lesson 4 source is partial/truncated in the retrieved summary.
- Lessons 5–11: complete original message transcripts and image binaries have not yet been verified as available.
- Lessons 12–13: historical records indicate complete long-form teaching outputs exist, but the exact original message bodies and binary image assets must be retrieved from source conversation/export before claiming verbatim archival.
- Lesson 14: current conversation contains a long teaching response; preserve exact response text and image query references where recoverable. Binary images still require separate source files.
- Lesson 15: current teaching response is being archived separately; its inline image queries are references, not binary assets.

This status is not a claim that no source exists anywhere. It describes what has been verified as accessible for this archive task.

## Required per-lesson directory

Recommended:
```
archive/
  README.md
  lessons/
    01/
      transcript.md
      assets/
      asset-manifest.csv
      source-manifest.json
    02/
    ...
```

Each source manifest should include source status, original conversation date/reference, message ordering, exactness status, asset list, and missing items.

## Verification checklist

Before marking a lesson complete:
1. Compare transcript against the original source message/export.
2. Verify every section, table, equation, code block, Q&A and quiz is present.
3. Verify image binaries by opening them; preserve original ordering and mapping.
4. Verify all links/citations.
5. Record any unavailable assets or source ranges.
6. Commit to GitHub and fetch the committed files again.
7. Only then mark the lesson archive as verified.
