# Callable code cleanup validation

The final local acceptance covers 218 EPI, 75 Blind 75, and 41 Interview Cake
questions. Every starter and solution in all five languages was audited:
3,340 artifacts, including 3,304 changed strings and 36 already identical strings.
The changes include formatting and moving judge infrastructure out of visible
code; those counts do not describe algorithm defects.

The machine-readable [acceptance report](validation-results.json) binds each
execution to the displayed source, assembled program, corpus, and compiled
harness. It also records every content audit and fixture archive receipt.
Reports from obsolete program bytes cannot establish acceptance. A current
failure supersedes an earlier passing receipt until a successful rerun.

| Check | Final local result |
| --- | --- |
| Displayed algorithms, complete applicable corpora | 1,670 accepted question/language pairs; 2,048,335 case evaluations |
| Executable starters | 1,670 compile and reach the real judge |
| Content, formatting, dependencies, reproducibility | All 3,340 artifacts and 515 required reference blocks pass |
| Interview Cake starter/correct/incorrect fixtures | 615 checks; 13,245 archived execution rows verified |
| Additional boundary cases | 570 accepted evaluations across five languages |
| Original C# explanation walkthroughs | All 334 accepted |
| Generator and acceptance regressions | 74 tests on Python 3.12.14 and 3.14.8; no skips |
| Frontend/backend regressions | 198 frontend and 207 backend tests; no backend skips |
| Clean Linux checkout | Fresh dependency installation, strict frontend build, warnings-as-errors .NET build, 198 frontend and 207 backend tests pass |
| Original runner audit | Existing adapter, corpus, negative-output, compiler and malformed-maze checks pass |

A starter deliberately contains unfinished code. Its scaffold acceptance means
it compiles and enters its real judge, not that it implements the algorithm or
executes every corpus row successfully.

HTTP acceptance inspected every API artifact and exercised category submissions,
legacy programs, imports and lexical bindings, exact saved submission bytes,
compiler/runtime diagnostics, malformed input, all five actual language timeouts,
concurrent-submission rejection and recovery, drafts/history, and version 1/2
backup restoration. The comprehensive run recorded 14,186 checks; a fresh final
runtime check recorded another 8,710 checks, including all final API payloads and
original Java import/body diagnostic positions. These are distinct stages, not a
claim that every earlier check reran after a metadata-only change.

Browser acceptance covered 80 desktop starter/solution views across all five
languages and eight algorithm categories, expanded relevant references, and
mobile layouts. The 80 core rendered views were visually inspected. No external
asset requests or page errors occurred. Solution viewing/copying, tab and
language changes, selection changes, storage errors, history, recovery and backup
flows preserve editor code and its format. The full visual matrix is not a claim
that all 3,340 artifacts were individually opened in a browser; their complete
individual content audit is separate.

Defects found during validation were repaired and affected scopes rerun. These
included missing dependency closures in JavaScript merge-k-lists and Python gray
code, Java comparison annotations, a C++ skyline signature alias, Python 3.14
annotation analysis, language import/binding support, diagnostic line mapping,
and recovery storage errors. The evidence aggregator also gained a regression
for entry-list generator hashes. Existing tests and time limits were retained.

The full algorithm matrix ran on Linux with .NET 10, Node 24, Python 3.14.8,
C++17 and JDK 21. Producer output and all 74 Python regression tests were also
checked on Python 3.12.14. A full Windows algorithm matrix and other Python
versions were not run locally. Windows Website checks and all final-commit
workflows must be observed separately in GitHub Actions.

Scoped Ruff, Prettier, syntax, .NET analyzer, build, and diff checks pass. An
additional broad formatting probe found pre-existing default-Prettier drift in
the untouched `.github/workflows/test_web.yml`; it was preserved. No new problem
wording or diagrams were introduced by this cleanup. Original wording checks
still pass, and attribution remains with the original collections.

CI regenerates the content, reruns the complete matrix and fixtures, aggregates
the coverage receipts, and exercises HTTP/browser compatibility in
`.github/workflows/callable-code.yml`. Raw execution records and screenshots are
uploaded as workflow artifacts; local intermediate and repaired-failure reports
remain in `.epi-runs/` without being represented as final passes.
