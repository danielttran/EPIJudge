# EPI book coverage and study plans

The website currently exposes **218 distinct test corpora**, not a complete
inventory of every exercise in the book. Run `python scripts/audit_book_coverage.py`
to reproduce the repository counts and missing study-guide references.

## What the numbers mean

The publisher's [Python listing](https://books.google.com/books/about/Elements_of_Programming_Interviews_in_Py.html?id=eErBDwAAQBAJ)
describes over 250 problems, 300 tested programs, and 150 additional variants.
The authors' [older overview](https://elementsofprogramminginterviews.com/2014/04/08/2014-04-08-epi-features/)
describes over 300 problems and includes design questions. These edition-specific
figures do not all count the same thing. Neither figure means that this judge
repository must contain 300 independent auto-graded exercises.

The current repository has:

- 218 TSV test corpora, all represented by the website.
- 221 Python judge entrypoints referencing those corpora.
- 223 headings in the historical index, including bootcamps and additional items.
- Three LCA entrypoints sharing `lowest_common_ancestor.tsv`: root-based,
  parent-pointer, and close-ancestor formulations.
- Two GCD entrypoints sharing `gcd.tsv`: a bootcamp and an honors presentation.

The current one-corpus/one-web-entry model hides the two distinct parent-pointer
LCA formulations. Those should get their own exercise identities and contracts;
they must not be silently replaced by the root-based LCA problem. The duplicate
GCD presentation does not by itself justify claiming another distinct algorithm.

## Study guide

`epijudge.client/src/studyGuide.json` stores C0–C4 in the order shown by this
[public transcription](https://github.com/slgriff/EPI-to-LC#study-guides-for-shortened-time-frames).
**The transcription has not been independently certified against a particular
printing.** Its source and this limitation are retained in the data and this document.
Each plan is one focused list using columns C0 through C(i−1). Entries retain
priority, chapter, and within-cell order; repeated references appear once.
Previous/Next follows that single list. These are application subsets, not the
book's complete coding-plus-pseudocode workload or an exact daily calendar.

The Review mode and its saved tab preference have been removed. Its additional
assignments are not merged into the plans. Those coding exercises and reading
companions remain available through All topics, Coding, and Reading & Design.

| Plan | Items | Graded coding | Reading/design |
| --- | ---: | ---: | ---: |
| 3 days | 18 | 16 | 2 |
| 7 days | 41 | 36 | 5 |
| 1 month | 65 | 58 | 7 |
| 4 months | 92 | 82 | 10 |

The twelve ungraded references now open original reading companions in place,
including the two LCA formulations, concurrency, and system design. Companion
titles describe the new material; they are not certified exercise titles.
The selected plan also determines Previous/Next order, including companions.
Coding identities and accepted progress do not change when selecting a plan.

## Reading and design companions

Choose **Reading & Design** in the existing topic/plan dropdown, or open a
companion directly from a study plan. The initial twelve lessons contain original
Markdown explanations rendered as HTML, expandable prompts, checkpoints, a quiz,
and a notes/design-response panel. The shared-state lesson also contains an
interactive read/compute/write thread simulator with an optional lock.

Notes, answers, checkpoints, and manual review status autosave to SQLite using the
existing revisioned draft pipeline. Browser recovery, conflict handling, and answer
export/import also apply. **Reviewed** is purple and does not count as a green
accepted coding submission. There is no automated assessment of a design response.
These companions do not restore the two missing graded LCA contracts, reproduce
book chapters, or establish complete coverage of every exercise or variant.

Content is in `epijudge.client/src/reading/content/*.md`; metadata and interaction
definitions are in the adjacent `lessons.json`. See [READING.md](READING.md) for
authoring and storage details.

## Next steps toward the authors' intent

1. Verify the transcribed C0–C4 cells against the user's original guide page.
2. Model book exercise identity separately from the test corpus and retain
   edition-specific references. Restore the two parent-pointer LCA exercises
   across all five languages, sharing data but using their distinct APIs.
3. Audit numbered book exercises against the same edition's complete contents.
   Classify each as graded, code exercise without a grader, discussion/design,
   language/tooling review, or variant. Publish those counts separately.
4. Extend the implemented reading/design workflow after verifying the edition's
   complete inventory. Keep manual review distinct from automated acceptance.
5. Prioritize gaps selected by the study guide before adding optional variants.
   Keep chapter introductions and coding available without padding the problem
   count to match a marketing figure.
