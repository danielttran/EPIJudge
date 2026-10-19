# Code and cleanup audit

Audited October 19, 2026. Scope: the current web solution, frontend runtime import
graph, retained grading frameworks/reference answers, catalog generation and
verification tools, and the accumulated study-plan/reading changes.

## Removed safely

| Item | Evidence and reason |
| --- | --- |
| Default `React` import in `ErrorBoundary.tsx` | TypeScript reported TS6133 with unused-symbol checks enabled. The JSX runtime and named `Component` import cover the component. |
| `errorInfo` state and its update | Written on crashes but never read or displayed. Error logging and retry behavior remain. |
| Error screen's legacy clear-all-browser-storage action | Deleted every `epi:` key, including pending unsaved answers. Reload and editor retry remain, with recovery copies preserved. |
| `Microsoft.AspNetCore.Http.Features` import in `PracticeEndpoints.cs` | No types from that namespace are used in this file. |
| `.workspace-label` CSS rule | No runtime component or generated class expression references it. Data-dependent difficulty styles remain. |

The earlier Review-mode cleanup is also complete: no workload tabs, phase
argument/type/state, phase labels, or phase CSS remain. A small migration removes
only the retired `epi:studyPhase` preference. Plans retain 18/41/65/92 items.
Other exercises remain accessible outside plans; answers and progress are retained.

## Retained deliberately

- All five solution projects have current responsibilities: React client,
  ASP.NET Core host, submission runner, shared C# framework, and tests.
- All 21 frontend runtime TypeScript/TSX modules are reachable through relative
  imports from `main.tsx`. Declaration files and tests are separate compiler/test
  inputs. Markdown is loaded through the explicit content glob.
- `GenericTest`, `JudgeOptions`, `TypeGrammar`, and `TestResult` are not part of
  ordinary web submission execution, but the retained C# reference answers call
  `GenericTest.Run`. Removing them would break those sources.
- C++/Java/Python starters, wrappers, shared frameworks, and original types are
  execution dependencies. The native runner copies and adapts those frameworks;
  Python uses the original conversion/validation helpers.
- Reference solution folders support study and validation, including wording
  verification. They are source collections, not retired websites.
- `config.json` is read by the retained language frameworks and C# reference
  helpers. Catalog JSON, mapping data, generators, native fixtures, and audit
  tools are used by maintenance or regression checks.
- Legacy browser migration/recovery and language aliases still have explicit
  compatibility uses. Public APIs and reflection/generated-harness entry points
  were not classified as dead simply because the compiler cannot trace callers.
- IDE launch/Live Unit Testing configuration remains. `.lutignore` now excludes
  generated artifacts, dependency caches, and personal practice databases.

Old ignored `bin`, `obj`, cache, and test-output directories are disposable build
artifacts, not maintained source. They can be removed when no process uses them;
the audit uses isolated outputs instead of interfering with a running website.

## Compiler safeguards

C# application, framework, test, and audit projects treat warnings as errors.
The audited Release solution was built with warning level 9999 and code-style
build enforcement: **zero warnings, zero errors**. These settings are scoped to
the maintained projects; submitted user programs do not inherit them.

TypeScript's normal build now rejects unused imports/locals/parameters,
unreachable code, unused labels, and switch fallthrough. Roslyn's IDE0005,
IDE0051, and IDE0052 audit reported no unused C# private members after cleanup.
Roslyn scanned 46 C# files; its unsupported `.esproj` workspace message is
expected, and TypeScript checks the frontend separately.

The HTTP audit scripts accept an explicit `-DllPath`, so they test these Release
binaries rather than an older Debug build. New error-boundary tests verify that
crashes retain browser recovery data and the editor can retry. The longer App
save/reload integration test has a 15-second outer allowance; its assertions and
individual synchronization checks remain unchanged.

## Verification

- Release solution build: zero warnings and zero errors.
- TypeScript check and production frontend build: passed.
- Backend tests with coverage: 90 passed, including real SQLite persistence.
- Frontend tests with coverage: 136 passed across 11 suites. The configured
  persistence/coordination/model coverage gates passed; this is not a claim of
  whole-application coverage.
- Catalog audit: zero failures; all 218 corpora and all C# starter/harness builds
  checked, custom validators exercised, broken fixtures rejected.
- Wording/provenance audit: all 218 problems passed, including 8,850
  wording-sensitive corpus cases.
- Repository toolchain prerequisite check: .NET, Node, Python, C++, and Java passed.
- npm dependency audit: zero reported vulnerabilities, including development dependencies.
- Direct frontend startup: HTTP 200, no redirect, same-origin hot reload, and
  transformed application/editor readiness passed.
- C#/JavaScript/Python HTTP suite: passed full-corpus runs, custom validators,
  compile/runtime errors, hidden-case redaction, request protection, and timeout
  termination. The suite's isolated server stopped successfully.
- Native HTTP suite: all 24 C++/Java submission checks passed, including accepted
  and rejected full-corpus fixtures, compiler/runtime errors, hidden-case
  protection, and both execution timeouts. Both 218-starter catalogs passed;
  the isolated server stopped successfully.
- Storage HTTP suite: all 57 checks passed across all five languages, including
  reading notes, optimistic conflicts, restarts, crash recovery, migration,
  pagination, and backup transfer to a fresh database. Its servers stopped.
- Final staged whitespace and credential/personal-data checks passed. Generated
  artifacts, private practice databases, and local tool paths are excluded from Git.

This is evidence of no additional confirmed removal candidates in the inspected
code, not a proof that every possible runtime path is covered. The study-guide
source remains a community transcription, not an independently certified book
edition inventory.
