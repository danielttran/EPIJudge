# EPI Practice

A local practice website with separate collections for **218 EPI problems**,
**Blind 75** in the exact [Crackr order](https://www.crackr.dev/blind75), and
**41 Interview Cake coding tasks**. Solve problems in **C#, JavaScript, Python, C++17, or Java 21**
using the browser editor, Run, and Submit.

Every coding question has a **Solution** tab with complete implementations in C#, JavaScript, Python, C++ and Java,
with explanations, complexity bounds and attribution. C# explanations also include
correctness arguments, original walkthroughs and edge cases. Reading a solution
leaves your editor draft and selected programming language intact. All solution
content is stored locally; see [coverage and validation](solutions/README.md).

The editor and Solution tab show the callable algorithm, with only the required
data structures available in a collapsed, read-only reference. Judge drivers and
test infrastructure stay outside the editor. Existing full-program drafts and
backups keep their original format. See [displayed code and compatibility](workspace-code/README.md).

## Start the website

On a new Windows machine, install the .NET 10 SDK, Node.js 24 LTS, Python
3.10+, JDK 21+, and a C++17 compiler (Visual Studio's Desktop development with
C++ workload, or GCC/Clang on PATH). Visual Studio is optional for running the
website. Then clone this repository and run from its root:

```powershell
./scripts/Setup.ps1
./Start.ps1
```

Setup checks every language toolchain, restores locked dependencies, and builds
the website. `./scripts/Setup.ps1 -CheckOnly` checks prerequisites without
building. Start opens the server at http://localhost:5178. No generated files,
personal tool paths, or existing dependency caches are required in the clone.
For portable tool installations, copy `.epijudge-tools.example.json` to
`.epijudge-tools.json` and fill in the relevant paths; that local file is ignored
by Git. Standard PATH and JAVA_HOME installations work without this file.

Open **EPIJudge.Web.slnx** in Visual Studio 2026. Select **EpiJudge.Web** and
its **Website** launch profile, then press F5. The app opens at
http://localhost:5178. The server starts the React client automatically.

From a terminal:

```powershell
dotnet run --project EpiJudge.Web --launch-profile Website
```

See the [website guide](EpiJudge.Web/README.md) for prerequisites, language
contracts, compiler setup, and troubleshooting. The site runs trusted local
code; accounts and a public submission service are outside this local app.
Answers, submission history, and progress are saved in a local SQLite database
outside the repository. The editor autosaves each problem/language separately;
green means solved by an accepted Submit, orange means attempted without an
accepted Submit. Browser recovery copies protect edits during connection issues.
Open the problem list to export/import answers for another machine.

The problem list has separate **EPI — 218 problems** and **Blind 75 — Crackr order**
filters, plus **Interview Cake — 41 coding tasks**. Blind entries have `B01` through `B75` labels and independent IDs, drafts,
and history. Their original statements, examples, corpora, and 35 local SVGs run
without LeetCode or external image requests. Similar EPI titles retain their
existing contracts. See [Blind 75 contracts and validation](blind75/README.md) and
[solution coverage, provenance and validation](solutions/README.md).

## Repository layout

| Location | Purpose |
| --- | --- |
| `epijudge.client/` | React, Monaco editor, and browser interface |
| `EpiJudge.Web/` | ASP.NET Core API and frontend startup |
| `EpiJudge.Runner/` | Submission execution, grading adapters, and web catalog |
| `EpiJudge.TestFramework/` | Shared C# data structures and serialization |
| `test_data/` | Shared TSV test corpus |
| `epi_judge_cpp/`, `epi_judge_java/`, `epi_judge_python/` | Native starters, wrappers, and language frameworks used by the website |
| `epi_judge_*_solutions/` | Completed reference answers retained for study and verification; these are not websites |
| `scripts/` | Catalog maintenance and website regression tools |
| `workspace-code/` | Generated callable starters, displayed solutions, required references, and complete artifact coverage |

**EPIJudge.Web.slnx is the only application solution.** The old root Vue
progress dashboard and standalone C# console project are retired. The shared
framework and reference-answer source code remain. Historical mapping/progress
metadata is preserved in `scripts/problem-mapping.json` for catalog tooling.

## Build and verify

Run the fast backend and frontend tests from the repository root. The website
can stay running because test builds use a separate output folder:

```powershell
./Test.ps1
# Or include coverage reports and coverage thresholds:
./Test.ps1 -Coverage
```

For a full rebuild and grading checks, first stop the website with Ctrl+C in
its terminal or Stop Debugging in Visual Studio, then run:

```powershell
cd epijudge.client
npm ci
npm run build
cd ..
dotnet build EPIJudge.Web.slnx
dotnet run --project scripts/WebAudit/WebAudit.csproj
python scripts/verify_problem_wording.py
./scripts/Verify-Web.ps1 -StartServer
./scripts/Verify-NativeWeb.ps1 -StartServer
./scripts/Verify-Practice.ps1
```

The HTTP checks start and stop their own hidden local test servers. Add
`-CheckFrontend` to the C# HTTP suite to check the direct React development
launch. Both HTTP suites include intentional 60-second timeout checks;
`-SkipTimeout` skips them on a repeat run.

See [TESTING.md](TESTING.md) for the test layers, coverage scope, and code boundaries.

The problem dropdown also includes 3-day, 7-day, 1-month, and 4-month study plans
from a linked study-guide transcription. See [BOOK-COVERAGE.md](BOOK-COVERAGE.md)
for sources, plan ordering, unavailable references, and book-versus-judge counts.

Choose **Learn** in the top navigation for twelve original study companions,
grouped by topic with search, source filters, article contents, and related practice.
The articles retain interactive checkpoints and quizzes, a concurrency simulator, and a notes panel.
Notes and review progress autosave to SQLite and travel with Export/Import answers.
Purple **Reviewed** is separate from green coding acceptance. See [READING.md](READING.md).

To regenerate catalogs:

```powershell
python scripts/generate_problem_catalog.py
python scripts/generate_web_catalog.py
python scripts/verify_problem_wording.py
```

The GitHub `Website checks` workflow builds the app and runs catalog, grading,
wording, and native submission checks. See
[the cleanup record](docs/web-only-cleanup-proposal.md) for what was retired
and what the website still requires.

## Repository contribution policy

This repository is maintained through the owner's fork. **Never push branches,
commits, or tags to `adnanaziz/EPIJudge`, and never open a pull request against
that upstream repository.** Push changes only to the owner's fork. Pull requests
from other contributors may be reviewed and tested locally, but validated fixes
must be merged and pushed only to the owner's fork.

## Source and license

EPI Judge accompanies *Elements of Programming Interviews*. The repository's
[LICENSE](LICENSE) applies to its source, reference answers, and test data.
The website statements are source-backed paraphrases for the displayed APIs,
not quotations verified against a particular book edition.

Thanks to the original EPI Judge authors and contributors, including
Viacheslav Kroilov, for the test frameworks and exercise corpus.
