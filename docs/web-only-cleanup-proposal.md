# Completed website cleanup

Completed October 17, 2026. The repository now has one application solution,
`EPIJudge.Web.slnx`, for the current React website.

## Removed

| Removed item | Reason |
| --- | --- |
| Root `index.html` and `html/` | Obsolete Vue progress dashboard; replaced by the React website. The current `epijudge.client/index.html` stays. |
| Root `problem_mapping.js` | Old dashboard asset. All its data, including historical progress counters, is preserved as `scripts/problem-mapping.json` for catalog maintenance. |
| `EPIJudge.slnx` and `EPIJudge.slnLaunch` | Duplicate solution containing retired console applications. Repository discovery now recognizes the retained web solution. |
| Old `epi_judge_csharp/` console app and 218 TODO exercise stubs | Browser starters and submission grading replace this console workflow. Required shared code and catalog tools were moved out first. |
| C# reference folder's executable `.csproj` and `Program.cs` | Retired console launcher. `CountBits.cs` and `Anagrams.cs` reference answers remain. |
| Four old console CI workflows and `epijudge_ci_test_tool.py` | Replaced by `.github/workflows/test_web.yml`, which builds and checks the website. |
| C++ console CMake/Make files and Java console Makefiles | Website submissions compile directly through the web runner. Source and grading frameworks remain. |

The 218 retired C# exercise files were checked for TODOs before removal.
Uncommitted/untracked changes in that exercise tree were checked. The selected
300 files were copied to a recovery directory and SHA-256 verified before
removal, including generated console output that was inside the retired tree.

Recovery copies and their manifest are at:
`C:\Dev\EPIJudge-cleanup-recovery-20261017`.

## Preserved and organized

- `EpiJudge.Web`, `epijudge.client`, and `EpiJudge.Runner`: the current website,
  API, and grading worker.
- `EpiJudge.TestFramework`: shared C# nodes and serialization, moved out of the
  retired console folder and explicitly included in the web solution.
- `test_data`: the real exercise cases.
- `epi_judge_cpp`, `epi_judge_java`, and `epi_judge_python`: website starters,
  problem wrappers, shared types, and language grading frameworks.
- All four `epi_judge_*_solutions` folders: completed reference answers for
  study and validation. These are source-code collections, not old websites.
- Catalog metadata, generation, shared type helpers, and wording verification
  under `scripts/`. Their references were updated to the new paths.
- Website regression scripts and focused native fixtures.
- Browser-saved code, attempt history, and solved status. Cleanup does not
  alter browser storage.

The maintenance checks also exposed a missing Python `reverse_list.py` stub.
It was added so catalog regeneration and Python's existing reverse-list web
entry have their required source wrapper.

## Current application

Open `EPIJudge.Web.slnx`, select `EpiJudge.Web` / `Website`, and press F5.
The app supports C#, JavaScript, Python, C++17, and Java 21. The original native
scaffolds are kept because their wrappers implement the exercise contracts;
they are dependencies of the current website rather than separate websites.

See the root README and `EpiJudge.Web/README.md` for the current workflow.

## Verification after cleanup

- The retained web solution builds successfully using the relocated framework.
- Catalog regeneration and wording/provenance checks pass for all 218 problems.
- WebAudit reports zero failures, including compilation of every C# starter and
  generated harness and checks of custom validators.
- The React site returns HTTP 200 directly with same-origin hot reload.
- The HTTP suite passes real C# submissions, custom types, compiler/runtime
  errors, hidden-case redaction, JavaScript/Python smoke checks, and the full
  507-case Python reverse-list corpus.
- Revalidated October 18, 2026: C++ and Java each retain 218 starters, and all
  24 native submission checks pass against the cleaned repository. These cover
  Run/Submit, full-corpus reference submissions, custom validators, rejection
  of broken mutations, compiler/runtime failures, hidden-case redaction, and
  timeout termination. The temporary test server shut down successfully.
- The replacement GitHub workflow is configured; it has not been run remotely
  from this local session.
