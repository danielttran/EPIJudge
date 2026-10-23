# Cracking the Coding Interview, sixth edition

All **189 numbered references** are accounted for in `inventory.json` and
`inventory-reconciliation.json`. They are not 189 runnable exercises:

- **131 independently authored coding exercises** are registered locally, with
  **655 language solutions** and starters (C#, JavaScript, Python, C++, Java).
- **33 conceptual** and **17 design** references remain outside callable practice.
  Individual classification evidence is in `classification-review.json`.
- **8 unimplemented coding references** are explicitly excluded from this supported
  publication: **12.2, 12.8–12.11, 14.1–14.3**. `exclusions.json` records each
  source, compatibility finding and exact limitation. Reverse String and Copy
  Node remain specification-unverified rather than being replaced with similar
  problems. The native ownership/allocation and SQL tasks receive no misleading
  managed/array equivalents. This publication adds no new runtime infrastructure.


The author repository and official contents page are the primary references.
Pinned author-linked language ports support implementation-interface research.
The remaining numbering was reconciled with a pinned independently authored
Java checklist and the independent SDE Skills practice course index. Provenance,
source scope and licensing observations are recorded per reference. Supplemental
indexes establish titles/numbering, not full executable specifications.
No book PDF, statement transcription or third-party solution is copied.
Statements, code, examples, explanations and tests here are independently authored.

Each registered problem has explicit callable contracts, a concrete example,
mutation/identity rules, admitted bounds, five actual language implementations,
WHY-focused explanation, correctness argument, worked trace and justified time
and space costs. `review*.json` records per-question and per-language semantic
review. Language-specific algorithms are explained individually. Existing similar
bank questions retain separate collection references rather than silently replacing
these tasks.

Native standalone and separate-module runs each cover **655 solutions /
993,970 solution case executions**, with **655 rejected starters** and the same
number of starter case observations. Final application-callable acceptance covers
**all 2,325 solutions and 2,325 rejected starters in the 465-problem bank**, with
**3,042,305 case observations per role**. `whole-bank-validation.json` joins actual
receipts to current code, composed source, notes, corpus and harness fingerprints.
Original unchanged receipts are reused; the changed overlap wrapper/notes and
corrected boundary fixtures have fresh runs. All 655 CTCI pairs execute through
application wrappers. Two Tail snippets changed during visual review and have
fresh replacement receipts rather than restarting unchanged completed work.

All 1,670 original-bank worked examples and 1,670 original-bank boundary groups
pass separately (3,815 boundary cases). Every CTCI worked example belongs to its
actually executed complete corpus, which includes its authored boundary coverage.
The receipt correlator preserves JSON types and input arguments while allowing a
double output to be displayed as `5` or `5.0`; five regressions protect that check.
Structural inventory/catalog checks never grant semantic review or execution
credit. Native/module receipt reuse also binds the actual grader and toolchain.

Last K Lines (12.1) reads an actual native temporary file in every language. Blank
lines are records, EOF is separate, and the final LF is not an extra blank line.
Fifteen compiled regressions reject blank-line sentinels, reversed suffixes and
file mutation; all five HTTP submissions pass 537 cases each. Tail memory bounds
come from reviewing actual streaming code, not a claim of measured process heap.
Other resource, identity, randomness and native-worker observers have separate
regression receipts and explain their measured scope.

All **329 backend tests**, **247 frontend tests**, production frontend and web
builds pass. The browser audit covers **365 scenes / 929 checks**, both themes,
all five languages, desktop/mobile and 200% zoom. `integration-validation.json`
records exact sources and the limited Tail metadata delta reaudited after the
initial generic run; earlier receipt hashes are retained rather than rewritten.
Manual visual inspection found and fixed Python's close/materialize explanation,
then confirmed readable code, focus, scrolling and unclipped controls.
The independent Solution language dropdown sits immediately above code; code,
explanation and trace switch together while editable drafts remain intact.

Reproduction uses `scripts/ctci6/audit.py` for evidence integrity,
`verify_runtime.py --starters` for fingerprinted submitted modules, the chapter
verifiers for standalone authoring, targeted `test_*` grader regressions, and
`scripts/SolutionsAudit` for actual displayed application-callable corpus runs.
The supported-publication gate requires current execution/integration evidence
and explicit disposition of all eight excluded coding references. The authoring
export's `collectionPublicationReady` flag does not grant publication acceptance;
`scripts/ctci6/audit.py --publication` is the final supported-scope integrity gate.
Full book coding coverage remains incomplete. Publication and exact-commit CI
are tracked separately in `checkpoint.json`.

The final integration audit also replaced POSIX-only temporary-file calls in the
C++ file-tail observer with atomically created standard C++ filesystem directories.
The Windows native HTTP check now covers the actual CTCI file exercise. Catalog
checks require the original 334 problems plus the registered CTCI collection,
with the original collection counts and IDs still checked.
