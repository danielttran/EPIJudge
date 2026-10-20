# EPI Practice website

A local React + TypeScript website with an ASP.NET Core API and a submission
worker supporting **C#, JavaScript, Python, C++17, and Java 21**.
All **218 EPI problems** remain available with their real TSV test files.
A separate **75-problem Blind 75 collection** adds original statements, local
artwork and independent test corpora in the exact Crackr order. This is the repository's catalog,
not every exercise or variant in every edition of the EPI book.

![The local React workspace showing a C# solution and passing test results](../docs/website-preview.png)

## Start with the Visual Studio Play button

1. Open **`EPIJudge.Web.slnx`** from the repository root in Visual Studio 2026.
2. Set **EpiJudge.Web** as the startup project if it is not already selected.
3. Select the **Website** launch profile, then press **F5** or the green Play button.

The website opens directly at **`http://localhost:5178`** and stays at that URL.
ASP.NET Core starts Vite in the background and waits until React is ready before
it begins listening. Frontend requests and hot-reload WebSockets pass through
the C# server, so there is no SPA proxy landing page or browser redirect.
Readiness includes the transformed application and editor modules, not just a
static marker. React and all five Monaco language imports are pre-bundled and
warmed before opening the workspace, including on an empty dependency cache.
If the initial scripts fail to load, the HTML fallback shows a reload action
after 20 seconds instead of remaining indefinitely on "Loading workspace…".

`EPIJudge.Web.slnx` is the single application solution. Its shared **Website**
launch configuration starts the server; the server starts the client
automatically. Each server owns a Vite process on a private port with its own
dependency cache, so an overlapping restart cannot shut down the new frontend.

Prerequisites are the **.NET 10 SDK**, **Node.js 24 LTS with npm**, and Visual
Studio's **ASP.NET and web development** workload. Node/npm build and develop
the frontend. The API and worker are C#; submissions run in their selected language.

Use the repository's `scripts/Setup.ps1` on a fresh clone to check all five
language toolchains, restore dependencies, and build; then run `Start.ps1`.
The launcher finds Node from PATH, including the current Windows user PATH.
It launches Vite directly with Node. Portable tool locations can be specified
in the ignored `.epijudge-tools.json` file using the supplied example.

The first project build restores .NET and npm dependencies. Subsequent builds
reuse them. The npm dependency versions are recorded in `package-lock.json`.

## Use the website

Click **Problem list** in the top toolbar to open the searchable problem drawer.
Selecting a problem closes it; the close button, Escape, and backdrop also close
it. Previous/next buttons step through the catalog without opening the drawer.
The description and editor share the main workspace. Choose a language above
the editor, and use **Run** or **Submit** in the top toolbar. Test results start
collapsed, open when code runs, and can be expanded or collapsed from their header.

For EPI exercises, choose a language in the editor. C++ and Java provide the original EPI source
scaffold: implement its TODO methods while retaining the wrappers and main
function (and Java's `package epi` and class name). Their native signatures can
differ from the C# contracts described below. Accepted native cases display
validator confirmation; failing cases show the actual value when available.

Blind 75 uses the typed scaffold displayed for the selected language, including
its `Solution`, `Codec`, `Trie`, `WordDictionary`, or `MedianFinder` class when
applicable. Its supplied node types use `val`, `next`, `left`, `right`, and
`neighbors`. Implement the displayed methods and keep those definitions;
C++ and Java harness entry points are supplied by the runner. Existing EPI
node types and wrapper contracts remain unchanged.

For C++ install Visual Studio's C++ build tools on Windows, or put `g++` or
`clang++` on PATH. Windows builds automatically locate `vcvars64.bat`.
`EPI_CPP_COMPILER` can select a GCC/Clang executable; `EPI_VCVARS64` can select
the Visual Studio setup script. C++ submissions use C++17 and have a 60-second
compile limit and a separate 60-second execution limit.

Java requires JDK 21 or newer. Set `EPI_JAVA_HOME` or `JAVA_HOME` if it is not
on PATH. Java compiles for Java 21 with a 45-second compile limit and a separate
60-second execution limit. Python requires Python 3.10+ on PATH or
`EPI_PYTHON_PATH`. No machine-specific installation paths are built into the runner.

1. Select a problem from the library. Search by title or ID, or filter by topic.
2. Implement the method inside the supplied `Solution` class. Keep its name,
   parameters, and return type so the harness can call it.
3. Click **Run** (Ctrl+Enter) for the first three visible cases in that problem's TSV.
4. Click **Submit** (Ctrl+Shift+Enter) to check every row in the TSV.

Run results include the input, expected value, actual value, and any runtime
exception. Submit returns totals and a status without revealing hidden case
contents. Compiler diagnostics appear in the results panel.

Drafts, exact Run/Submit source snapshots, verdicts, and progress are saved in
SQLite for one local profile. On Windows the default file is
`%LOCALAPPDATA%\EPIJudge\practice.db`, outside this checkout. Set `EPI_DATA_DIR`
or `Practice:DataDirectory` to choose another directory. No separate database
installation is needed. This is local persistence, not automatic cloud sync.

The editor autosaves after a short typing pause and keeps browser recovery
copies until the server confirms a save. Each problem and language has its own
draft. Revision checks prevent another tab from silently overwriting it; the
editor offers **Use saved version** or **Keep my version** if a conflict occurs.
Green marks an accepted full Submit; orange marks attempts without an accepted
Submit. Later failures do not remove solved status. Editing alone does not mark
a problem attempted.

**History** lists saved attempts with language, verdict, and time, with older
entries available through pagination. **View answer** shows the original code;
**Restore to editor** copies it to the corresponding language draft. Reset
changes only the draft and never deletes history or solved status.

Existing browser drafts, solved flags, and history are imported automatically
and idempotently. Old summaries do not have recoverable code or language and
are labeled **Legacy summary**. Original browser data is retained.

Use **Export answers** in the problem drawer to download a JSON backup, then
**Import answers** on another machine. Import merges history and missing drafts,
preserving existing drafts. Keep backups private: they contain your source code.
Import supports version 1 backups up to 64 MB. Copying the Git repository alone
does not copy personal answers. The SQLite database and its WAL files should
stay together; use Export for a portable, consistent backup while the app runs.

`scripts/Verify-Practice.ps1` tests persistence with temporary isolated databases,
including restarts, concurrency, colors' underlying status rules, migration,
pagination, and backup restore. The other HTTP suites also isolate their data
when invoked with `-StartServer`, so tests do not change personal progress.

## Project layout

| Project | Purpose |
| --- | --- |
| `epijudge.client` | React, TypeScript, Vite, and the Monaco C# editor |
| `EpiJudge.Web` | ASP.NET Core endpoints, frontend startup, and same-origin development proxy |
| `EpiJudge.Runner` | Problem descriptions, TSV adapter, compilation, execution, comparison |
| `EpiJudge.TestFramework` | Shared C# nodes, serialization, and grading support |
| `test_data` | Existing EPI test corpus |

`ProblemCatalog.cs` keeps the original three APIs compatible with saved code.
The other entries are embedded from `EpiJudge.Runner/catalog.json`. Regenerate
that file after editing descriptions or signatures in
`scripts/generate_web_catalog.py`:

```powershell
python scripts/generate_web_catalog.py
```

Each exercise includes a statement, C# starter, and examples. Statements are
source-backed paraphrases for the displayed C# API, not verbatim book text.
Examples use TSV cases or explicitly labeled, verified illustrations. Custom
examples show the actual C# return value or required mutation rather than the
test wrapper's internal boolean, height, or interval length.

All exercises are marked **Unrated** because the repository does not supply
difficulty ratings. These are practice stubs for you to solve, not prefilled solutions.
The wording review and source references are recorded in
`docs/problem-wording-review.md` and `docs/problem-wording-sources.json`.

### C# contracts and grading

- Lists and arrays use `List<T>`; record-like values use value tuples.
- `using EpiJudge.TestFramework;` supplies `ListNode<T>`, `BinaryTreeNode<T>`,
  `PostingListNode`, and `GraphVertex`. Their members are documented in the
  exercise's constraints. Keep the namespace import in the starter.
- Several APIs return the normalized value used by the original test wrapper:
  for example, closest stars returns distances, and tree traversal exercises
  return values. Follow the displayed C# signature and description.
- In-place partitioning and Sudoku are checked after mutation. Shared-list,
  graph-copy, and posting-list exercises check object identity and links.
- Queue, stack, cache, and credit exercises expose multiple methods on
  `Solution`. `Initialize` resets the state for the next command sequence;
  operation results are checked against the recorded commands.
- Problems with multiple valid outputs have dedicated validators. Their visible
  expected output may be a property such as `true`, a shortest interval's length,
  or a tree's height, rather than the object your method returns.
- Randomized exercises draw 100,000 samples per batch and check legal values,
  frequencies, and (for uniform distributions) pairs and triples. Up to three
  batches allow for rare statistical failures. These checks are statistical,
  not a proof of randomness, and can take longer than ordinary exercises.
- Floating-point results use relative tolerance `1e-9` with an absolute floor of
  `1e-9`. Order is ignored only for exercises that permit it; sequence order
  remains significant inside permutations and word decompositions.

The website's C# starters and invocation contracts are maintained in
`EpiJudge.Runner`. Adding a source file alone does not register a web exercise.

## Terminal workflow

From the repository root:

```powershell
dotnet run --project EpiJudge.Web --launch-profile Website
```

Open `http://localhost:5178` if the terminal does not open a browser. To run the
two processes separately, use two terminals:

```powershell
# Terminal 1: API without automatically starting Vite
dotnet run --project EpiJudge.Web --launch-profile "API only"

# Terminal 2
cd epijudge.client
npm ci
npm run dev
```

Build the backend and type-check/build the frontend with:

```powershell
dotnet build EPIJudge.Web.slnx
cd epijudge.client
npm run build
```

With the API running, `scripts/Verify-Web.ps1` checks real accepted submissions,
wrong answers, compiler errors, runtime errors, timeouts, and hidden-case
redaction against the local API.
Add `-CheckFrontend` when running the Website profile to also check that React
and hot reload are served directly without a redirect.

### Catalog and adapter audit

From the repository root, run:

```powershell
dotnet build scripts/WebAudit/WebAudit.csproj --configuration Release --maxcpucount:1
dotnet scripts/WebAudit/bin/Release/net10.0/WebAudit.dll
```

This checks all catalog IDs and counts, deserializes every corpus argument,
round-trips the expected result types, exercises every custom adapter against
reference fixtures, rejects selected broken implementations, compiles all 218
real starters with their generated harnesses, and runs a regression through the
actual submission worker. The fixtures do not implement every ordinary problem;
this is an audit of catalog wiring and grading, not proof that every conceivable
incorrect solution will be rejected.

With Website running, the HTTP regression suite also checks real submissions
covering primitive values, tuples, mutable arrays, trees, graph copies, posting
lists, caches, randomness, and floating-point results:

```powershell
./scripts/Verify-Web.ps1 -BaseUrl http://localhost:5178 -CheckFrontend
```

The intentional infinite-loop check takes 60 seconds. Use `-SkipTimeout` for a
faster repeat after already checking process termination.

For the wording, source hashes, translated examples, and sensitive conventions:

```powershell
python scripts/generate_web_catalog.py
python scripts/verify_problem_wording.py
```

The wording checks compare selected sensitive conventions against the original
Python reference functions and corpus. The source manifest covers all 218 IDs
and normalizes line endings when hashing files. Regenerate it after changing
statements or the referenced sources.

## Execution scope

Native website regression checks, including full corpus submissions for
representative custom wrappers, compiler/runtime errors, hidden-case redaction,
and process timeouts, are available with:

```powershell
./scripts/Verify-NativeWeb.ps1 -StartServer
```

This uses focused fixtures in `scripts/NativeWebFixtures`, not the full native
solution trees. It checks representative grading paths, not all 218 solutions
in both native languages.

This release is for **your own trusted code on your local machine**. It binds
to localhost, rejects remote API callers, and enables compilation only in the
Development environment. Each attempt compiles a temporary .NET project,
executes it as a separate process, and removes its temporary directory.

The runner allows one attempt at a time, limits compilation to 45 seconds,
limits execution to 60 seconds for the complete test run, caps captured output
at 16 million characters per output stream,
and kills timed-out process trees. These process controls are not an operating
system sandbox: submitted C# has your user's file and network permissions.
Public submissions require an isolated worker with resource and network
controls before this can be hosted for other people.

The repository's existing LICENSE applies to its test data and other material;
review those terms before publishing or distributing a hosted problem library.

## Troubleshooting

- **npm is not recognized:** reopen Visual Studio after installing Node; check
  `node --version` and `npm --version` in a new terminal.
- **Port 5173 is in use:** stop an old Vite process or previous debugging session.
- **The library cannot load:** check server output and confirm the API is
  listening on port 5178.
- **Compilation cannot start:** confirm the .NET 10 SDK is installed and the app
  is running inside this repository with `test_data` present.
- **F5 opens the console judge:** choose EpiJudge.Web as the startup project and
  select its Website launch profile.
- **An old SPA proxy page is still open:** stop the previous debugging session,
  rebuild, and press F5. The current Website profile opens the app directly on
  port 5178; the Microsoft SPA proxy package is no longer used.
- **React fails to start:** the server reports the failure in Visual Studio's
  output instead of serving a waiting page. Check whether another process is
  using port 5173. You can set `Frontend:NodePath` to an explicit Node executable
  or `Frontend:Port` to a different internal development port if needed.
