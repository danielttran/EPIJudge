# Displayed code

The practice workspace has 334 runnable questions: 218 EPI, 75 Blind 75, and
41 Interview Cake. Each has a starter and a displayed solution in C#, JavaScript,
Python, C++17, and Java 21: **3,340 visible code artifacts**. The generated
[coverage manifest](coverage.json) identifies every artifact by stable question
ID, language, and role, with source hashes and required-reference decisions.

`catalog.json` contains the callable code and execution envelopes. The three
files in `parts/` are generated independently from the existing bank sources.
The original source files and legacy submission contracts remain available;
these generated files do not edit a user's draft.

Every source was compared with the previous displayed source, rather than merely
counted. The audit found 3,304 changed strings and 36 already identical strings:

| Language | Audited | Changed | Already identical |
| --- | ---: | ---: | ---: |
| C# | 668 | 640 | 28 |
| JavaScript | 668 | 668 | 0 |
| Python | 668 | 660 | 8 |
| C++ | 668 | 668 | 0 |
| Java | 668 | 668 | 0 |

These counts include formatting and removal of visible judge infrastructure;
they do not mean that 3,304 algorithms had incorrect behavior.

## What the workspace shows

Starters and solutions contain the callable algorithm and any helper algorithms
it actually needs. They do not show test drivers, comparison functions, serializer
scaffolding, unrelated model types, or other questions' reference algorithms.
Normal formatting is applied to every artifact. Required data structures and
supplied APIs appear separately in a collapsed, read-only reference. Reading or
copying a solution does not replace the editor. Loading code into an edited
draft requires an explicit action and preserves the draft through the existing
history and recovery flows.

Some EPI Java contracts use methods inside a judge-owned outer class. Their
editor contains those class members; it does not need the outer class or `main`.
Problem-specific helper classes belonging to the algorithm remain visible.

## Submission compatibility

`callable-v1` identifies the function/class snippets. The server assembles an
execution copy with the recorded envelope. Stored drafts, submission snapshots,
history, and backups retain the original editor bytes and their code format.
There is no source-based format guessing or stripping of user declarations.

`legacy-v1`, including an absent format in older records, retains the original
full-program path without inserting this new envelope. The format selector lets
the user choose a full program explicitly. Backup version 2 records formats;
version 1 backups remain importable as legacy code. Viewing a solution does not
migrate a draft to another format.

C# and C++ use compiler line directives. Python compiles the exact UTF-8 editor
source as a separate code object, so future imports and traceback lines work.
Java leading imports are read lexically and moved into the execution envelope;
their original editor positions remain blank lines in that execution copy.
JavaScript declarations have their own lexical scope, allowing ordinary `require`
bindings to shadow judge-only bindings. Java and JavaScript diagnostics map back
to editor line numbers; hidden support errors keep their support locations.

## Regeneration and acceptance

Use the repository's locked Node dependencies and the pinned formatter/parser
requirements. The runtime toolchains match the normal practice website.

```sh
npm --prefix epijudge.client ci
python -m pip install -r scripts/code_workspace/requirements.txt
python scripts/code_workspace/native.py
python scripts/code_workspace/managed.py
python scripts/code_workspace/isolated.py
python scripts/code_workspace/build.py --check
python scripts/code_workspace/audit.py
python -m unittest discover -s scripts/code_workspace -p 'test_*.py' -v
```

Use `build.py` without `--check` to update the combined catalog and coverage
manifest after changing a producer. The audit checks every visible artifact and
required reference for syntax, formatting, hidden infrastructure, unrelated
helpers, dependency closure, provenance, and reproducibility. Parser limitations
are reported explicitly and checked with the actual language compiler where
needed; parsing does not replace execution.

```sh
dotnet run --project scripts/SolutionsAudit -c Release -- --callable --language=csharp
dotnet run --project scripts/SolutionsAudit -c Release -- --callable --starters --language=csharp
dotnet run --project scripts/SolutionsAudit -c Release -- boundaries --callable --language=csharp
dotnet run --project scripts/SolutionsAudit -c Release -- walkthroughs --callable --language=csharp
dotnet run --project scripts/interviewcake/Audit -c Release -- csharp all --callable
dotnet run --project scripts/SolutionsAudit -c Release -- describe --callable
```

Repeat the language-specific commands for `javascript`, `python`, `cpp`, and
`java`. Correct solutions must pass their complete applicable corpus. Starters
must compile and reach the real judge; an intentional starter failure is recorded
separately from a correct solution. The Interview Cake audit additionally checks
all 615 starter/correct/incorrect fixtures, including state, identity, filesystem,
and randomized contracts. Boundary evaluations and all 1,670 language-specific walkthroughs remain
separate checks.

```sh
python scripts/code_workspace/verify_http.py --dll EpiJudge.Web/bin/Release/net10.0/EpiJudge.Web.dll --browser
python scripts/code_workspace/evidence.py
```

The HTTP/browser checks inspect all 3,340 API artifacts and exercise real
submissions, diagnostics, invalid input, five timeouts, concurrent submissions,
drafts, history, recovery, backups, offline resources, and desktop/mobile views.
The evidence gate requires current code, composed-program, corpus, and harness
hashes for every required execution. A later current failure supersedes a pass.
It does not treat missing, skipped, stale, or unavailable execution as success.

CI runs these gates in the **Callable code checks** workflow alongside the
existing Website, Blind 75, and Solutions/collections workflows. Raw results and
browser screenshots are retained as workflow artifacts. Algorithm attribution
and licenses remain in the original source and collection documentation.
