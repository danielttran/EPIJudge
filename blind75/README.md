# Blind 75 collection

This collection contains exactly the 75 entries, in order, from
[Crackr's Blind 75 page](https://www.crackr.dev/blind75), checked on 20 October 2026.
It includes both **Combination Sum** and **Combination Sum IV**, and excludes
**Longest Common Subsequence**. The frozen titles are in [source-order.txt](source-order.txt).
All 218 existing EPI problems retain their IDs, statements, test data and contracts.

Use **Blind 75 — Crackr order** in the problem drawer. Entries are numbered B01–B75,
with separate `blind75_…` IDs so similar EPI titles never share answers or grading.
All five languages have typed, executable scaffolds. Stateful exercises use the
supplied `Codec`, `Trie`, `WordDictionary`, or `MedianFinder` class; other exercises
use the displayed function or `Solution` method. Node fields are supplied in each
starter. C++ and Java entry points come from the runner.

The descriptions, examples, explanations, constraints, test corpora and SVGs were
authored for this repository. Crackr supplies collection membership and ordering;
LeetCode is not used at runtime. The C++ and Java harnesses use the repository's
existing local JSON parsers. The 35 original diagrams live under
[`EpiJudge.Web/wwwroot/blind75`](../EpiJudge.Web/wwwroot/blind75).

## Contracts

The displayed wording defines each contract, including empty-input conventions,
interval endpoints, duplicate handling, index and coordinate order, and tie rules.
For example, Blind Two Sum returns two distinct indices in an unsorted array;
EPI Two Sum retains its sorted-array boolean contract and permits element reuse.
Blind Group Anagrams includes singleton groups; the EPI exercise retains its
existing omission rule.

In-place matrix problems preserve the supplied rows. Linked-list problems check
original node identity, values and membership. Tree inversion and BST ancestor
queries check original nodes. Graph cloning rejects shared original nodes and
changes to the input graph. Codec encoding and decoding run in separate processes
within the existing total execution budget, preventing instance fields, static
fields or module globals from substituting for a self-contained encoding.

## Sources and regeneration

| File | Purpose |
| --- | --- |
| [`scripts/blind75/specs.py`](../scripts/blind75/specs.py) | Original wording, constraints and authored examples |
| [`scripts/blind75/corpus.py`](../scripts/blind75/corpus.py) | Deterministic random cases and explicit boundary cases |
| [`scripts/blind75/oracle.py`](../scripts/blind75/oracle.py) | Independent mathematical oracle |
| [`scripts/blind75/validate.py`](../scripts/blind75/validate.py) | Input-precondition checks separate from answer calculation |
| [`scripts/blind75/fixtures`](../scripts/blind75/fixtures) | Actual correct algorithms and nonconstant incorrect/adversarial algorithms |
| [`scripts/blind75/diagrams.py`](../scripts/blind75/diagrams.py) | Original SVG generation tied to example 1 |
| [`scripts/Blind75Audit`](../scripts/Blind75Audit) | Real five-language compilation and execution audit |

```sh
python scripts/blind75/generate.py
python scripts/blind75/fixtures.py
python scripts/blind75/diagrams.py
python scripts/blind75/generate.py
python scripts/blind75/validate.py
```

The final generation step incorporates the diagram manifest into the catalog.
No network access is used by generation or grading. Full test commands and
report locations are documented in [TESTING.md](../TESTING.md).

## Review and validation

Every authored example was checked against the mathematical oracle and input
preconditions. A separate wording review found and corrected an initial Two Sum
example with two valid pairs despite its uniqueness promise. The 35 SVGs were
rendered in Chromium on nine review sheets and visually inspected against their
first examples. Node colors were corrected to follow original list nodes, and
the cycle arrow was moved clear of index labels.

The [validation record](VALIDATION.md) distinguishes completed local checks from
platform checks delegated to CI. The added workflow runs all five languages and
HTTP/browser checks on Linux with Python 3.14; the existing Windows workflow remains.
