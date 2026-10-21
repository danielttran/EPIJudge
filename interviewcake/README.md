# Interview Cake coding collection

This collection contains 41 independently authored runnable exercises, separate from the 218 EPI and 75 Blind 75 exercises. Stable IDs begin with `interviewcake_`. Each has a typed starter and an actual reference algorithm in C#, JavaScript, Python, C++ and Java. The five conceptual, JavaScript-specific, design and puzzle entries from the supplied inventory are excluded.

Interview Cake is credited for task identity and inspected technical compatibility facts. The bank contains newly written statements, examples, algorithms, explanations, tests and three original diagrams. It does not import course narratives, hints, examples, solution code or artwork, and does not imply affiliation. The sanitized provenance records all seven technical-fact transfers and the inspected archive's SHA-256; private archive paths are absent.

## Explicit compatibility choices

Each question's constraints disclose its bounded valid domain and any added bank convention. Reference implementation quirks do not automatically become requirements. In particular:

- Tree balance measures the global spread of leaf depths; a one-leaf chain passes.
- A stock trade requires a purchase and a later sale, including a negative best profit on declining prices.
- Duplicate finders, shortest routes, graph colors and tied temperature modes accept any valid answer.
- List deletion checks target and successor aliases; reversal and node selection check original object identities. Read-only objects, links and nested containers must remain unchanged.
- Duplicate-file detection uses actual controlled filesystem directories and bounded three-position sampling. Sample collisions are accepted as suspected duplicates; timestamps are a fallible orientation heuristic. All files and directories are checked for unintended changes.
- Shuffle and dice use injected source randomness. Small distinct shuffles have exact finite decision-tree probability checks and repeated-permutation histograms. Dice have bounded rejection-tree checks, forced source prefixes, seeded marginal/pair/triple distribution checks and repeated calls on one instance. These tests detect the supplied biased, cached and correlated implementations; finite testing does not prove every possible randomized program correct.
- The word-cloud token and capitalization grammar is an explicit deterministic ASCII bank policy. The trie is a disclosed runnable adapter for a storage-design task.

The JSON examples describe adapter inputs and observed outputs. Some methods return `void` or node references: their example explanations distinguish observed mutations, identity indices and property-check outcomes from actual return types. Filesystem descriptors and random-source prefixes are judge inputs; the corresponding submitted APIs receive a directory path or no value arguments.

## Validation and reproduction

There are 883 corpus cases, including 123 published examples, plus executable walkthrough cases and structural/stateful/randomized checks inside the adapters. `coverage.json` is an explicit manifest of all 205 question/language solutions; execution acceptance is recorded separately in the repository-wide solution evidence and hash-matched audit reports.

```sh
python3 scripts/interviewcake/generate.py --check
python3 scripts/interviewcake/validate.py
dotnet run --project scripts/interviewcake/Audit -- csharp all
```

Run the last command with `javascript`, `python`, `cpp` or `java`, or omit arguments for all five. Each language checks 41 starters, 41 exact displayed algorithms and 41 meaningful incorrect algorithms: 615 executions across all languages. Starters deliberately report unimplemented methods; the audit still requires a complete execution report for every case, rather than counting compilation or a process failure as scaffold success. Wrong fixtures must compile and execute, then fail at least one case.

The audit hashes the actual embedded catalog, typed harness and runner source, checks them against current sources, and records code/corpus hashes and complete-report row counts/hashes. Reports use unique run IDs under `.epi-runs`; raw execution reports are archived there before temporary build directories are removed. Final acceptance requires current hashes, not earlier authoring runs.

Local authoring checks used Python 3.12.14. Python 3.14.8 parity was also verified in the cloud; Windows execution remains a CI check. Other expected toolchains are .NET 10, Node 24+, C++17 and JDK 21. The runner also retains the existing Windows Visual C++ fallback; Linux checks alone do not establish Windows execution parity.
