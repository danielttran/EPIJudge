# EPI Practice

A local LeetCode-style practice website for the 218 EPI problems in this
repository. Solve problems in **C#, JavaScript, Python, C++17, or Java 21**
using the browser editor, Run, and Submit.

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

**EPIJudge.Web.slnx is the only application solution.** The old root Vue
progress dashboard and standalone C# console project are retired. The shared
framework and reference-answer source code remain. Historical mapping/progress
metadata is preserved in `scripts/problem-mapping.json` for catalog tooling.

## Build and verify

```powershell
dotnet build EPIJudge.Web.slnx
cd epijudge.client
npm ci
npm run build
cd ..
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
