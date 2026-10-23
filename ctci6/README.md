# Cracking the Coding Interview, sixth edition

This collection is being authored. **124 verified coding exercises are registered in the local website; the collection has not been pushed.**
The advertised 189 is a book question count, not a count of executable exercises.

`inventory.json` records numbered references established from the author's public
solution repository and its linked community repositories. Source paths and
commits are provenance, not permission to reuse source code. No reuse license was
established for the examined repositories. Statements, examples, implementations,
tests, and explanations must therefore be independently authored. No book PDF or
translated book transcription is used as an authoring source.

The Java inventory contains 145 numbered directories. The author-linked JavaScript
inventory establishes 160 distinct references after reconciliation. In particular,
Java's `Q6_05_Egg_Drop` conflicts with the JavaScript inventory: Egg Drop is 6.8,
and Jugs of Water is 6.5. Both sources are retained rather than silently assigning
two different exercises to 6.5. Twenty-nine advertised references remain
unlocated in these sources; their titles and specifications must not be invented.

The author's linked full table-of-contents image could not be fetched: the
executor request to `https://i.imgur.com/3afl3Kl.png` was rejected by the network
tunnel with HTTP 403. No alternate proxy, permission change, or unofficial book
download is used to bypass that result. Public repository research can continue.

For each exercise, publication requires a source-established technical task, an
explicit callable contract, independent wording and examples, applicable language
starters and implementations, algorithm-specific explanations and worked traces,
and executions against independent positive, boundary, and negative checks.
Thread, memory-management, SQL, Java-specific, design, and conceptual exercises
need individual classification. They must not be relabeled as generic algorithm
functions merely to produce five language rows. Noncoding exercises remain out
of the callable collection.

Existing problems may be linked only after comparing domain, return values,
mutation and identity requirements, empty cases, tie handling, and restrictions.
A shared title or familiar algorithm is insufficient evidence of equivalence.
Existing problem IDs, progress, and drafts must be preserved.

Structural inventory validation proves numbering and source-record consistency.
It does **not** prove statement clarity, solution correctness, test adequacy, or
completed semantic review. Those are separately recorded and executed before the
collection is published.

The current local checkpoint stages 124 coding exercises: all references in
chapters 1–4, seven coding tasks from chapter 5, generic Circular Array/Hash Table 7.9/7.12, all fourteen chapter-8 tasks,
all eleven chapter-10 tasks, both functional tasks 13.7–13.8, and all twenty-six tasks in each of chapters 16 and 17.
Their 620 actual language solutions pass standalone and separate-submission runs,
with 976,710 solution case executions per layer and the same number of starter
observations. Each starter is rejected by at least one case; it need not fail
every case. Random Node additionally has fifteen compiled alternative/negative
programs covering twenty-five fixtures, including physical duplicate identities,
clone returns, missing mutations and the generic random source's signed bounds.
All five current Random Node HTTP submissions pass all 1,604 cases, and the
current backend suite passes 324 tests.

The 160 located references currently comprise 124 coding exercises, two known
coding candidates (Othello and Minesweeper), four concurrency references awaiting individual classification, fifteen
conceptual references and fifteen design references. The ten chapter-6
reasoning puzzles now have explicit individual classification and source-clarity
findings. Another twenty-nine advertised references remain unlocated; neither
unresolved group is counted as completed. Noncoding material is not added to the
callable product UI. The new aggregation also passes all five HTTP submissions (577 cases each), and ten compiled wrong-result/mutation regressions are rejected. The variable-size subset also passes all five HTTP submissions (145 cases each). Its separate audit records twenty-five compiled programs and fifty fixture executions with final source/model/harness fingerprints: biased/shared decisions, deduplication and mutation are rejected; inverted coins and longer two-coin XOR filters are accepted. Circular Array also passes all five HTTP submissions (1,535 integer/string trace cases each). Its twenty distinct compiled variant implementations exercise forty typed fixtures: caller aliasing, skipped negative bounds and shared iterator cursors are rejected; inverse-offset storage is accepted. Hash Table passes all five HTTP submissions (5,035 cases each); twenty compiled audit programs batch forty generic fixtures, rejecting key-match/duplicate-entry/removal bugs and accepting tail insertion. Final whole-bank and rendered checks remain pending.

The `review*.json` files record actual algorithms, bindings and semantic review
scope. Independent case oracles live under `scripts/ctci6/corpus*.py`.
`classification-review.json` records the evidence for noncallable classifications.
Inventory/evidence integrity is checked by `python3 scripts/ctci6/audit.py`;
`--publication` intentionally fails while full acceptance remains incomplete.
Structural checks are not semantic review or execution credit.

Application evidence is preserved in separate source/build scopes: the first 23
exercises, three initial bit exercises, four further bit exercises, three initial
recursion/DP exercises, and four combinatorial generation exercises. Each batch passed both submission formats. The individual
reports under `runtime/application-validation*.json` and `checkpoint.json` retain
these scopes. They are not one final combined current-build acceptance run.
The verified 104-exercise subset is integrated locally into a 438-problem bank.
Remaining known content/classifications, final whole-bank runs and publication
remain pending. Local integration preserves existing progress and drafts.
See `workflow-review.md` for the measured workflow diagnosis and next batch gates.

External-file checkpoint: 10.6 now executes genuine disk-backed external merging through opaque leased-record/file APIs in all five languages. All 615 staged solutions passed 975,120 cases per layer; 615 starters were rejected. Fifty compiled resource/ownership and valid-alternative programs passed sixty audit fixtures. All 323 backend tests pass; five HTTP submissions each passed 298 external-sort cases. These are local results, not publication or whole-bank final acceptance.

Jigsaw 7.6 checkpoint: all five HTTP submissions pass 318 fixtures each. A property grader accepts any valid assembly without forcing original hidden coordinates; fifteen compiled negative/alternative programs pass. Current source-bound receipts cover 620 solutions and 976,710 cases per layer, with all starters rejected. This remains local and does not complete the outstanding inventory or final whole-bank gates.
