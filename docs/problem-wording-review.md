# Problem wording review — October 17, 2026

## Scope and evidence

Reviewed all **218** website entries against the repository's Python reference
implementations, tester wrappers, TSV headers and expected results, and the C#
adapter contracts. Also checked the C++ RPN implementation to resolve the
integer-division convention. The actual book text was not supplied: these are
source-backed C# paraphrases, not verified quotations from a particular edition.

[The source manifest](problem-wording-sources.json) lists reference files and
test data for every ID, with hashes of the source text and statement files.
Hashes normalize CRLF/LF line endings. The parent-pointer LCA variant is selected
explicitly because multiple variants share the same TSV.

## Changes

- Clarified or corrected **45 descriptions** and disambiguated **10 titles**
  that shared generic bootcamp or submatrix headings.
- Rewrote **73 custom-adapter examples** to show the public C# result or required
  mutation. Trees, paths, and index pairs no longer appear to return the
  checker's internal height, boolean, or interval length.
- Explained shared-tail/cycle construction, graph input setup, stateful command
  sequences, and the distinction between return values and in-place mutations.
- Labeled and checked illustrative examples rather than implying they were
  quoted from the book or copied from a TSV row.
- Removed the three manually assigned difficulty ratings. All entries are now
  **Unrated** because the source repository provides no difficulty scale.
- Renamed the UI labels to **Your C# API** and **Expected result**, covering both
  single methods and stateful APIs, including methods that return void.

### Material corrections and clarifications

| Problem | Source-backed behavior |
| --- | --- |
| Huffman coding | Return `sum(frequency × codewordLength) / 100`. Do not renormalize by the frequency sum; some corpus rows sum near 1 rather than 100. A single symbol can have a zero-length code. |
| Merge BSTs | Expected output includes tree shape. Choose the upper middle element of each half-open sorted range, matching the reference construction. |
| Text justification | Pack lines greedily; distribute internal padding evenly with excess spaces on the left; left-justify the last line. |
| Salary cap | Return the smallest cap achieving the target. At the existing payroll total, this is the largest salary. |
| Sequential keyword coverage | The corpus uses distinct keywords. Removed the unsupported claim that repeated keywords are part of the source exercise. Return inclusive indices, not the checker's length. |
| Equal-to-index and unknown-length search | Arrays are strictly increasing; array indices are zero-based. |
| Linked-list deletion | The two deletion exercises have different access models. Delete-after selects a non-head position; deletion using only a selected node excludes the tail. |
| Phone mnemonics | Outputs use uppercase mappings, with 0 and 1 mapping to themselves. |
| Substring search | `t` is the text; `s` is the pattern. Comparisons are case-sensitive. |
| Reverse words | Do not trim or collapse spaces. Reverse the ordering of the space runs along with the words. |
| Roman numerals | Apply the adjacent-value subtraction rule without adding a canonical-spelling validator. |
| Road proposals | Highways are undirected; compare all-pairs distance savings. Break ties by proposal order; an empty proposal list returns `(-1,-1,0)`. |
| Sliding window | Consider current and previously processed chronological readings in inclusive `[t-w,t]`. |
| Right-sibling links | `Next` reaches the immediate node on the right at the same level, including nodes with different parents. |
| Random examples | Examples are possible outcomes, not fixed answers. A degenerate case with only one subset or permutation is allowed to be deterministic. |
| RPN division | The C# statement uses truncation toward zero, as in the repository's C++ implementation. Python uses floor division; existing corpus divisions do not distinguish the two rules. |

Other edits make tuple ordering, index bases, C# return types, buffer capacity,
letter case, and practice goals explicit. Algorithm-technique goals are not
presented as checks that the grader can enforce.

## Verification

```powershell
python scripts/generate_web_catalog.py
python scripts/verify_problem_wording.py
dotnet build EPIJudge.Web.slnx --configuration Release --no-restore --maxcpucount:1
cd epijudge.client
npm run build
```

The wording checks passed for all 218 source entries, all 73 translated custom
examples, and **8,850 wording-sensitive corpus cases**. They execute selected
original reference functions and check the preconditions underlying the revised
statements. The four compact illustrative examples and the curated examples
also pass their checks.

All 215 generated method signatures, starter templates, grading invocations,
comparisons, argument counts, and test counts remain unchanged. The three
curated APIs are also unchanged. This review changes wording and examples,
not algorithm implementations or the original test data.

These checks establish the documented conventions for the repository and its
C# API. They do not certify every possible input or repair defects in every
upstream language implementation.
