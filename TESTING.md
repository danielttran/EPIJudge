# Testing and code structure

Run `./scripts/Setup.ps1` on a new clone to check the prerequisites, restore
packages, and build the solution. Unit tests need .NET 10 and Node.js 24;
the HTTP grading suites also need the language toolchains listed in README.md.

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
