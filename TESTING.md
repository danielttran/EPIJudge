# Testing and code structure

Run `./scripts/Setup.ps1` on a new clone to check the prerequisites, restore
packages, and build the solution. Unit tests need .NET 10 and Node.js 24;
the HTTP grading suites also need the language toolchains listed in README.md.

## Displayed solutions and the Interview Cake collection

`solutions/coverage.json` enumerates all 334 runnable questions (218 EPI,
75 Blind 75, 41 Interview Cake) in all five languages, for 1,670 displayed
solutions. Rebuild the resource after source or explanation changes:

```powershell
dotnet run --project scripts/SolutionsAudit -- inventory
python scripts/solutions/build_catalog.py
python -m unittest discover -s scripts/solutions -p test_random_checker.py -v
dotnet run --project scripts/SolutionsAudit -- --report=all
dotnet run --no-build --project scripts/SolutionsAudit -- boundaries
dotnet run --no-build --project scripts/SolutionsAudit -- walkthroughs --language=csharp
# Repeat walkthroughs with javascript, python, cpp and java.
dotnet run --project scripts/interviewcake/Audit -- csharp all
# Repeat the preceding Interview Cake command for javascript, python, cpp and java.
dotnet run --no-build --project scripts/SolutionsAudit -- describe
python scripts/solutions/evidence.py
dotnet build EPIJudge.Web.slnx -c Release --disable-build-servers --maxcpucount:1
python scripts/verify_solutions_http.py --dll EpiJudge.Web/bin/Release/net10.0/EpiJudge.Web.dll --browser
python scripts/verify_interviewcake_http.py --dll EpiJudge.Web/bin/Release/net10.0/EpiJudge.Web.dll
```

`SolutionsAudit` runs the exact embedded source through the editor's submission
contract, with every available corpus row. `--language=python` (or another
supported language) partitions the matrix. `--ids=a,b` selects targeted reruns;
`--batch=1` through `--batch=5` select the original disjoint EPI authoring groups.
`--files` is an author diagnostic and cannot satisfy final displayed-code
acceptance. The evidence tool checks every explicit pair against current source,
metadata, corpus and compiled-harness fingerprints. Boundary audits exercise all
five languages; walkthrough audits execute the selected language’s own notes.
Run all five language partitions to cover all 1,670 walkthroughs.
Both use isolated temporary corpora, leaving original test data unchanged.

The Interview Cake audit separately executes each of its 41 starters, actual
correct algorithms and deliberately flawed algorithms in every language. Its
property checks cover valid alternative duplicates, paths, modes and colorings;
mutable node identity and preserved inputs; stateful sequences; real controlled
filesystem fixtures; injected random choices, exact small permutation
probabilities and deterministic distribution checks. Finite tests do not prove
asymptotic bounds or universal random independence. Disclosed bounded domains and
adapter choices are recorded in `interviewcake/provenance/contracts.json`.

The HTTP suite compares all 1,670 payloads with the generated resource and checks
that reads change no practice storage. Chromium covers all three collections,
selected-language solution switching, independent editor drafts, keyboard tabs,
loading/error/retry/unavailable states, copy failures, narrow layouts, local
artwork and backup preservation. It uses Playwright's installed Chromium or
`CHROMIUM_PATH`. The UI has no action that replaces the editor with a solution.

The cloud verification ran the current Python solutions on both Python 3.12.14
and an isolated Python 3.14.8 installation; CI explicitly uses Python 3.14.
The complete algorithm matrix runs on Linux. Windows build, native smoke and
storage checks are covered by the existing Windows workflow. Run a fresh-checkout locked dependency install and
build when changing generated content or build initialization.

## Fast regression checks

```powershell
./Test.ps1
# Include backend reports and enforce frontend coverage thresholds:
./Test.ps1 -Coverage
```

Run these from the repository root. The website can stay open: `Test.ps1`
builds the test project and all its dependencies under `.epi-runs/test-build/`,
away from the DLLs loaded by the development server. It stops on a failed check.
It installs frontend dependencies if `node_modules` is missing.

To run just one side:

```powershell
dotnet test EpiJudge.Tests/EpiJudge.Tests.csproj --artifacts-path .epi-runs/test-build -p:ShouldRunNpmInstall=false
npm --prefix epijudge.client test
```

`npm test` runs once without coverage; `npm run test:watch` watches changes.
`dotnet test EpiJudge.Tests/EpiJudge.Tests.csproj --artifacts-path .epi-runs/test-build --collect:"XPlat Code Coverage"`
writes a Cobertura report under `EpiJudge.Tests/TestResults/`.
Frontend reports are under `epijudge.client/coverage/`. These folders are ignored.

The frontend tests control network responses and timers and render React hooks
and components in jsdom. They cover debounce/coalescing, edits during saves,
per-language/problem isolation, revision conflicts, recovery storage failures,
legacy migration, imports/exports, subscriptions, stale requests, grading errors,
and drawer/history interactions. Monaco and actual compiler execution belong to
the launch and HTTP checks below, rather than mocked unit tests.

Frontend coverage gates apply to the persistence, asynchronous coordination,
and language starter helpers listed in `vitest.config.ts`: at least 90% lines/statements, 85% functions,
and 80% branches. This is not a whole-application coverage claim. UI components
have behavioral tests; generated catalogs and embedded language harnesses are
verified through the catalog and execution suites.

The backend unit tests exercise backup validation, progress rules, and submission
lifecycle failures. Only the process runner and submission-history write boundary
have test doubles. Storage tests use real SQLite databases in unique temporary
directories and remove them afterward. They cover competing writers, persistence,
source snapshots, hidden-case stripping, pagination, backup merge/idempotence,
transaction rollback, schema protection, and interrupted-attempt recovery.

## Full integration checks

```powershell
npm --prefix epijudge.client run build
dotnet build EPIJudge.Web.slnx
dotnet run --project scripts/WebAudit/WebAudit.csproj
python scripts/verify_problem_wording.py
./scripts/Verify-Web.ps1 -StartServer -CheckFrontend
./scripts/Verify-NativeWeb.ps1 -StartServer
./scripts/Verify-Practice.ps1
```

Stop a running development server before rebuilding its DLLs on Windows.
Use Ctrl+C in its terminal (or stop debugging in Visual Studio), then rebuild.
If a build reports a DLL locked by `.NET Host`, a server is still running;
retrying the same build will not release that lock. The isolated test command
above avoids this problem without stopping the site.
Run dependency installation and solution builds sequentially: the JavaScript
project can run its own npm install when package metadata changes.
The HTTP scripts start and stop temporary servers and use isolated practice data,
leaving the normal profile database untouched. Use different `-BaseUrl` ports
when running the suites concurrently. Intentional infinite-loop tests can take
over a minute. The GitHub workflow runs both the fast and integration checks.

To test isolated Release binaries with the HTTP suites, pass
`-DllPath <absolute path to EpiJudge.Web.dll>` to any of the three scripts.
This avoids accidentally testing an older Debug build or rebuilding locked DLLs.

## Compiler and unused-code checks

The application, framework, test, and catalog-audit C# projects treat warnings as
errors. TypeScript rejects unused imports/locals/parameters, unreachable code,
unused labels, and switch fallthrough during its normal build. These project
settings do not promote warnings in user-submitted solution code to errors.

```powershell
dotnet build EPIJudge.Web.slnx -c Release --artifacts-path .epi-runs/compiler-audit -p:ShouldRunNpmInstall=false -p:WarningLevel=9999 -p:EnforceCodeStyleInBuild=true -warnaserror
dotnet format analyzers EPIJudge.Web.slnx --no-restore --diagnostics IDE0005 IDE0051 IDE0052 --verify-no-changes --severity info
```

Roslyn skips the JavaScript `.esproj`; the TypeScript build checks that project.
Unused public APIs and runtime-generated/reflection-based entry points require
reference tracing and execution tests, not deletion based only on analyzer output.

## Responsibility boundaries

- `ProblemLibrary` owns the drawer and filtering; `HistoryPanel` displays snapshots.
- `useSubmissionHistory` owns history requests, pagination, cancellation, and stale-response guards.
- `useSubmission` owns the grading lifecycle and keeps grading success separate from refresh failures.
- `PracticeClient` coordinates draft revisions, autosave, conflicts, and progress.
- `practiceApi` owns persistence HTTP requests and backup transfer.
- `DraftRecovery` owns per-tab recovery copies; `legacyMigration` handles old browser formats.
- `usePractice` binds an app-scoped client to React and browser lifecycle events.
- `PracticeDatabase` owns SQLite setup/connections and startup recovery.
- `PracticeStore` contains concrete SQL operations, without a generic repository layer.
- `PracticeProgress` and `PracticeBackupValidator` contain testable rules.
- `SubmissionService` captures source, runs grading, and finalizes results; HTTP endpoints map outcomes to responses.

The database schema and backup version remain unchanged. New abstractions should
earn their place through a real responsibility or external boundary; do not add
one interface per class or mock SQL to test database behavior.

## Blind 75 acceptance

Run the five-language matrix from the root:

```powershell
python scripts/blind75/validate.py
dotnet run --project scripts/Blind75Audit -- all
dotnet run --project scripts/Blind75Audit -- adversarial
dotnet run --project scripts/Blind75Audit -- describe
python scripts/blind75/evidence.py
```

This executes 375 typed starters, 375 actual correct algorithm fixtures, and
375 deliberately incorrect algorithms, followed by 10 static-memory codec
adversaries. Negative fixtures include correct-looking
outputs with copied nodes, aliased graphs, replaced matrix rows, altered original
values, partial-word matches and incorrect medians. Each report under
`.epi-runs/blind75-audit-*.json` records source, corpus and harness hashes.
`all <language>` selects one language. Reports from targeted reruns can be
validated against all current inputs with `python scripts/blind75/evidence.py`
after `describe` refreshes the compiled-harness fingerprints.

The clean-checkout startup regression runs on isolated temporary directories,
including a missing `.epi-runs` directory, repeated runs that preserve existing
evidence, nested missing parents, and a conflicting file:

```powershell
python -m unittest discover -s scripts -p test_blind75_http.py -v
```

The browser/HTTP suite starts temporary local profiles. It exercises the real
Monaco editor, all five language drafts, Submit, history restoration, backup
transfer, failed-save recovery, all local diagrams with external origins blocked,
invalid requests, syntax/runtime errors, busy responses, five real timeouts and
recovery after each timeout:

```powershell
node epijudge.client/node_modules/playwright-core/cli.js install chromium
python scripts/verify_blind75_http.py --dll EpiJudge.Web/bin/Release/net10.0/EpiJudge.Web.dll --browser
```

Build Release and the frontend first. `CHROMIUM_PATH` may select an installed
Chromium executable. `--no-timeouts` is a diagnostic shortcut and is explicitly
reported as skipped; it is not final acceptance. The existing Windows workflow
remains, while `Blind 75 checks` adds Linux/Python 3.14 execution and browser checks.

## Question and explanation clarity

`/scripts/clarity/parts/` contains disjoint authoring/review shards covering all
334 questions and 1,670 implementations. Each question supplies its description,
constraints, teaching examples, executable example cases, five callable contracts,
and written review decisions. The EPI, Blind75 and Interview Cake generators apply
these authored statements; Interview Cake explanation overrides also live in its
`algorithms_<language>.json` authoring sources. Edit sources, then regenerate.

```sh
python scripts/clarity/build.py
python scripts/generate_web_catalog.py
python scripts/blind75/generate.py
python scripts/interviewcake/generate.py
python scripts/solutions/build_catalog.py
python scripts/code_workspace/native.py
python scripts/code_workspace/managed.py
python scripts/code_workspace/isolated.py
python scripts/code_workspace/build.py
python scripts/clarity/build.py --check
python scripts/clarity/audit.py check
```

Review each question against its actual callables, adapters and original corpus:

1. State the input domain, representation, indexing, output, tie rules, mutation,
   identity requirements and empty/boundary behavior. Distinguish a callable’s
   return value from the wrapper-observed result. Record language differences
   before the learner opens Solution; do not silently invent a shared domain.
2. Read each language implementation. Explain the invariant or recurrence and
   why it proves the result; derive a small trace and justify time and live
   auxiliary storage from that code. A shared algorithm may share reasoning;
   a different loop, data structure, copying strategy or numeric model needs its
   own analysis. Record limitations rather than presenting them as proven facts.
3. Write decisions and evidence paths in the owning shard and semantic ledger.
   `audit.py inventory` only adds pending entries. After actual rereview, update
   the reviewed statement/code/notes/callable fingerprints in `review.json`.
   Never mark a record reviewed merely because required fields are populated.
4. Execute every authored example, each language’s walkthrough and added boundary
   fixtures, plus the complete original corpus. Original test data remains
   unchanged. The generated `boundaries-clarity-*.json` files are additive.
   Native EPI tree fixtures use `[null]` for an empty tree, matching the original
   TSV protocol; `[]` remains the ordinary empty-array encoding. Nearest-star
   fixture expectations list distances in ascending order; the native comparator
   sorts returned stars, so the callable itself may return them in any order.
5. Rebuild the app and inspect the longest explanations and unbroken source paths in all five languages
   on desktop, a 320px mobile viewport and native browser 200% zoom:
   `node scripts/clarity/browser.cjs http://127.0.0.1:PORT`.
   The existing `scripts/verify_learn_layout.cjs` suite separately covers controls,
   focus and shared layouts. Review screenshots as well as geometry assertions.

`code_workspace/run_matrix.py` runs the full callable solution/starter matrix,
all-language boundaries, all 1,670 walkthroughs and Interview Cake fixtures with
bounded process concurrency. Its durable job ledger and logs are under
`.epi-runs/callable-matrix-<tag>*`. `scripts/code_workspace/evidence.py` requires
current source, corpus, code and fixture fingerprints; stale or failed executions
cannot satisfy acceptance. Semantic review, structural coverage, executable
correctness and rendered usability remain separate gates.

Maximum-client-credit regression checks exercise all five independent oracles
with valid alternative ties, missing/lower-credit clients, negative increments,
replacement, removal and reinitialization. Run
`python scripts/clarity/credits_oracle_tests.py` and
`dotnet run --project scripts/clarity/CreditsAudit -c Release`. The latter uses
the actual callable composition and judge path, including deliberately false
Lookup implementations that must never validate their own Max result.
