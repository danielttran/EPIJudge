# Cracking the Coding Interview, sixth edition

This collection is being authored. **It is not yet part of the runnable website.**
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

The current local checkpoint stages 26 exercises (chapters 1–3 plus 5.1, 5.6 and
5.7), with 130 language implementations. Their standalone and separate-submission
runs each cover 20,430 positive cases and the same number of starter observations.
A starter passes its negative check only when at least one case rejects it; this
is not a claim that every starter fails every case.

`review01.json`, `review02.json`, `review03.json` and `review05.json` record the
specific algorithms, bindings and semantic review scope. The independently
computed case oracles are under `scripts/ctci6/corpus*.py`. Inventory/evidence
integrity is checked by `python3 scripts/ctci6/audit.py`; its `--publication` mode
intentionally fails until full acceptance is complete.

Application-runner evidence is scoped by compiled source fingerprint. The first
23 exercises passed both submission formats at checkpoint `d0c604a8`, recorded in
`runtime/application-validation-through03.json`. The three new bit exercises
passed both formats on the later runner build in `runtime/application-validation.json`.
These historical/current batches must not be described as one final combined
current-build acceptance run. Full final collection integration, whole-bank runs,
rendered checks and publication remain pending. Nothing in staging changes the
live library, progress or drafts.
