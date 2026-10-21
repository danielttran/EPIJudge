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
| Learn browser | 120 checks pass across every article; desktop/mobile, keyboard, search/filter history, deep links, legacy redirects, notes, drafts, backups and API failure |
| Expanded layout audit | 1,137 checks pass across 64 rendered states; geometry, full-viewport screenshots, hit targets and keyboard reachability checked |
| Existing Solutions regression | 7,077 HTTP checks and its complete browser suite pass |
| Existing callable workspace regression | 14,186 HTTP checks and all 80 representative browser views pass; all five actual language timeouts run |
| Style | Scoped Prettier, Ruff check/format, Node syntax, and diff checks pass |
| Clean checkout | Fresh detached checkout at `7640005`, then refreshed to the final functional source, fresh dependencies and outputs, matching frontend build, all frontend/backend tests and 120 browser checks pass |

The clean checkout reused installed toolchains and normal dependency caches,
while installing its own dependencies and generating its own build outputs.
It ran the inventory and HTTP/browser checks with Python 3.14.8; the working
checkout also ran them with Python 3.12.14. Reading files are pinned to LF, and
their hashes also pass in a separate `core.autocrlf=true` checkout. The final
Learn-only search correction was followed by refreshed builds, unit and browser
checks in both the working and detached checkouts. Existing Practice regressions
precede that isolated search correction; no runner or Practice logic changed.

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

The first CI run exposed a test-lifecycle race: a new navigation test could end
before its debounced save, allowing that request to reach the following test's
fetch mock. The test now waits for the saved status and verifies its exact single
write. The starter-view no-write assertion is unchanged. All 214 frontend tests,
three consecutive 32-test App runs, and the strict build pass after this test-only
repair; application code and rendered assets are unchanged.

## Expanded layout review

The later layout audit covers these exact profiles:

| Profile | Viewport |
| --- | --- |
| Desktop | 1440×1000 CSS pixels, 100% zoom |
| Tablet | 820×1180 CSS pixels, 100% zoom |
| Narrow phone | 320×740 CSS pixels, 100% zoom |
| Native 200% zoom | 1440×1000 browser window; measured 720×456 CSS viewport, DPR 2; full native capture 1440×913 pixels |

Every profile runs the same 16 states: Learn index, empty search, long card title,
the longest existing article title, synthetic unbroken heading/breadcrumb stress,
expanded article hint/simulator/quiz, scrolled expanded content, focused notes,
controlled catalog loading, catalog HTTP 503, missing article, Practice problem,
expanded provided types, expanded history/results, JavaScript Solution, and the
problem-library dialog with an empty search. Synthetic text exists only in the
isolated browser DOM and does not alter the inventory or user data.

The audit checks page overflow and text clipping; article/sidebar and header
geometry; enabled controls with `elementFromPoint` after scrolling them into view;
keyboard focus visibility and reachability; modal focus containment; and the
visible Monaco surface. Natural wrapping, scrollable code/input fields, and
intentional modal overlays are allowed. It does not impose a blanket prohibition
on overlapping boxes. Full native screenshots are dimension-checked so browser
zoom cannot silently crop the visual evidence.

This review found and repaired long-title overflow, tablet navigation covered by
the Run button, a 320-pixel Practice header wider than its viewport, and results
controls covered by an expanded helper/editor panel at 200% zoom. Pixel review
also caught an inner Monaco editor collapsing inside its otherwise visible
mobile container. Constrained Practice panels now reflow vertically, the editable
surface has a definite height, and long text wraps within its container. The
audit requires nonempty rendered code as well as a usable editor rectangle.
Focus outlines also cover selects, normal textareas and disclosure controls.
No question, algorithm, runner contract or saved-draft format changed.

All 64 state images and the detailed assertions are retained as CI artifacts.
All 64 views were inspected as rendered pixels in 16 labeled contact sheets,
with individual original images inspected for the native zoom and mobile editor
findings. Manual pixel review supplements the geometry and hit tests. The committed
screenshots above are delivery previews, not substitutes for the full matrix.

- [Solution at native 200% zoom](zoom200-practice-solution.png)
- [Mobile expanded helper and history](phone320-practice-history-expanded.png)

Coverage is headless desktop Chromium with emulated tablet/phone dimensions and
actual browser zoom. Physical touch devices, Safari, Firefox and screen-reader
usability were not tested; these checks do not prove the absence of every
possible visual issue.
