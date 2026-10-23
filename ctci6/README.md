# Cracking the Coding Interview, sixth edition

This collection is being authored. **118 verified coding exercises are registered in the local website; the collection has not been pushed.**
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

The current local checkpoint stages 118 coding exercises: all references in
chapters 1–4, seven coding tasks from chapter 5, all fourteen chapter-8 tasks,
ten chapter-10 tasks and all twenty-six tasks in each of chapters 16 and 17.
Their 590 actual language solutions pass standalone and separate-submission runs,
with 937,170 solution case executions per layer and the same number of starter
observations. Each starter is rejected by at least one case; it need not fail
every case. Random Node additionally has fifteen compiled alternative/negative
programs covering twenty-five fixtures, including physical duplicate identities,
clone returns, missing mutations and the generic random source's signed bounds.
All five current Random Node HTTP submissions pass all 1,604 cases, and the
current backend suite passes 318 tests.

The 160 located references currently comprise 118 coding exercises, five known
coding candidates, fourteen awaiting individual classification, fifteen
conceptual references and eight system-design references. The ten chapter-6
reasoning puzzles now have explicit individual classification and source-clarity
findings. Another twenty-nine advertised references remain unlocated; neither
unresolved group is counted as completed. Noncoding material is not added to the
callable product UI. Final whole-bank and rendered checks remain pending.

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
