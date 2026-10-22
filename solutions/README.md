# Local solutions

The three runnable collections contain 218 EPI, 75 Blind 75 and 41 independently
authored Interview Cake tasks: 334 questions. Each has C#, JavaScript, Python,
C++ and Java solutions, for 1,670 explicit question/language entries. Stable IDs
preserve each contract. EPI Two Sum permits element reuse and returns a boolean;
Blind 75 Two Sum returns distinct indices. Interview Cake's Balanced Binary Tree
checks the global spread of leaf depths, unlike the Blind 75 height-balance task.
The 12 reading companions retain their separate notes, quizzes and simulations.

`coverage.json` lists every live ID, collection, language, case count and source
path. Complete code lives in `<language>/<id>.<extension>`. C# metadata lives in
`notes/<id>.json`; other language metadata lives in `notes/<language>/<id>.json`.
`scripts/solutions/build_catalog.py` rejects coverage gaps, extra files,
unsupported languages and incomplete explanations before generating the embedded
`catalog.json`. Every language’s notes include an approach, correctness argument,
worked walkthrough, justified complexity and edge cases. Each walkthrough has an
executable case, allowing its arithmetic and observable result to be checked.

The adjacent **Problem** and **Solution** tabs share the left pane while the
editor stays visible on the right. The solution follows the selected language.
Its locally highlighted code is read-only; Copy writes only to the clipboard.
Viewing an answer never restores or overwrites a draft, submits code, updates
progress or changes history. Stale requests are discarded, and failed loads
show a retry. Browser checks cover desktop and narrow layouts.

C# EPI answers and their JavaScript ports are independently authored. Python,
C++ and Java answers retain attribution to their exact reference paths and the
[repository license](../LICENSE). Displayed copies identify local contract or
boundary corrections where required; other answers use independent implementations.
Upstream reference directories remain intact. Blind 75 answers reuse the
repository's original algorithm fixtures and retain its corpora and local diagrams.
Every answer displays provenance.

Interview Cake task identities and technical facts are attributed by source URL.
The bank independently authors statements, examples, algorithms, tests and art;
no course narrative, hints, solution expression or artwork is imported. The
[technical provenance](../interviewcake/provenance/contracts.json) distinguishes
source observations, unresolved behavior and explicit bounded bank conventions.
Those conventions cover randomized-source injection, approximate file sampling,
identity serialization and the deliberately flexible Word Cloud lexical policy.
They do not imply affiliation. The five noncoding/conceptual archive entries are
outside this collection.

`SolutionsAudit` executes the exact displayed embedded source through the same
runner used by the editor, against each complete local corpus. Additive boundary
and walkthrough audits create isolated corpora and retain original test files.
Reports record outcomes and code, notes, corpus and compiled-harness hashes.
`validation-results.json` is accepted only when every question/language pair has
current full-corpus evidence, plus current boundary and five-language walkthrough evidence.
The checked-in legacy report retains baseline history; current callable acceptance
is recorded in [workspace-code/validation-results.json](../workspace-code/validation-results.json).
CI regenerates the legacy report for each commit and publishes it as an artifact.
The separate Interview Cake audit executes all starters, correct algorithms and
meaningfully incorrect fixtures. [TESTING.md](../TESTING.md) contains commands
and the HTTP, offline/browser and clean-checkout validation requirements.

The [clarity review ledger](../scripts/clarity/review.json) records separate
per-question and per-language semantic decisions and fingerprints. Authored
question shards in `scripts/clarity/parts/` drive statements, callable contracts
and executable examples. Field presence and passing fixtures cannot prove that
a proof or complexity explanation is correct; see the review procedure in
[TESTING.md](../TESTING.md#question-and-explanation-clarity).
