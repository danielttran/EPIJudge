# Learn organization acceptance

All 12 existing local reading companions are mapped exactly once in
[the inventory](../../epijudge.client/src/reading/learnInventory.json). Their
original IDs, bodies, quizzes, checkpoints, hints, source references, simulator,
and saved-document contracts are preserved. The topic mapping is Foundations
(4 concurrency articles), Trees & Graphs (2), and System Design (6).

There are no locally stored Interview Cake reading articles. No archived course
content or external articles were imported. All 41 Interview Cake coding tasks
remain in Practice alongside 218 EPI and 75 Blind 75 questions. The runner,
solution, collection and callable-code source trees are byte-unchanged from
master `80452689d24f16d0d22a4a5b7f6df12300d8a75d`.

Final local checks:

| Scope | Result |
| --- | --- |
| Reading inventory | All 12 bodies, hashes, source labels, durations and topic mappings pass; 7 justified links resolve to real coding problems |
| Frontend | 214 tests pass; existing coverage gates pass; strict TypeScript/Vite build passes |
| Backend | 207 tests pass, no skips; warnings-as-errors build has zero warnings/errors |
| Learn browser | 119 checks pass across every article; desktop/mobile, keyboard, search/filter history, deep links, legacy redirects, notes, drafts, backups and API failure |
| Existing Solutions regression | 7,077 HTTP checks and its complete browser suite pass |
| Existing callable workspace regression | 14,186 HTTP checks and all 80 representative browser views pass; all five actual language timeouts run |
| Style | Scoped Prettier, Ruff check/format, Node syntax, and diff checks pass |
| Clean checkout | Fresh detached checkout at `7640005`, fresh dependencies and outputs, matching frontend build, all frontend/backend tests and 119 browser checks pass |

The clean checkout reused installed toolchains and normal dependency caches,
while installing its own dependencies and generating its own build outputs.
It ran the inventory and HTTP/browser checks with Python 3.14.8; the working
checkout also ran them with Python 3.12.14. Functional source is unchanged after
that checkout; subsequent changes record evidence and strengthen CI lint.

Each of the four screenshots below was inspected as rendered pixels. That review
found and repaired a mobile fixed-height inheritance bug that caused text to
overlap the sidebar. A browser geometry assertion now prevents its recurrence.
Related links wait for the actual catalog, and the UI distinguishes loading from
absence. Browser results contain zero external asset requests and zero page errors.

- [Learn index, desktop](learn-index-desktop.png)
- [Learn article, desktop](learn-article-desktop.png)
- [Learn index, mobile](learn-index-mobile.png)
- [Learn article, mobile](learn-article-mobile.png)

Library screenshot delivery returned a transport error before confirming any
file IDs. It was not retried. The images are preserved here and in CI artifacts;
this delivery limitation does not affect application correctness.

Intermediate failures and their fixes remain recorded in the local `.epi-runs/`
evidence. The Solutions workflow reruns the Learn inventory and browser audit,
alongside the existing master workflows. Final-master CI results are recorded
separately after publication. No deployment is part of this change.
