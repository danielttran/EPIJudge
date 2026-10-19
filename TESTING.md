# Testing and code structure

Run `./scripts/Setup.ps1` on a new clone to check the prerequisites, restore
packages, and build the solution. Unit tests need .NET 10 and Node.js 24;
the HTTP grading suites also need the language toolchains listed in README.md.

## Fast regression checks

```powershell
dotnet test EpiJudge.Tests/EpiJudge.Tests.csproj
cd epijudge.client
npm ci
npm run test:coverage
```

`npm test` runs once without coverage; `npm run test:watch` watches changes.
`dotnet test EpiJudge.Tests/EpiJudge.Tests.csproj --collect:"XPlat Code Coverage"`
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
Run dependency installation and solution builds sequentially: the JavaScript
project can run its own npm install when package metadata changes.
The HTTP scripts start and stop temporary servers and use isolated practice data,
leaving the normal profile database untouched. Use different `-BaseUrl` ports
when running the suites concurrently. Intentional infinite-loop tests can take
over a minute. The GitHub workflow runs both the fast and integration checks.

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
