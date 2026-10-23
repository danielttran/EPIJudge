# Cracking the Coding Interview, sixth edition

All **189 numbered references** are accounted for in `inventory.json` and
`inventory-reconciliation.json`. They are not 189 runnable exercises:

- **131 independently authored coding exercises** are registered locally, with
  **655 language solutions** and starters (C#, JavaScript, Python, C++, Java).
- **33 conceptual** and **17 design** references remain outside callable practice.
  Individual classification evidence is in `classification-review.json`.
- **8 coding candidates** remain outside practice: **12.2, 12.8, 12.9, 12.10,
  12.11, 14.1, 14.2, 14.3**. Their numbered titles are established, but a title
  does not establish detailed input/output, ownership, schema or error contracts.
  Native allocation/lifetime tasks and SQL queries must retain their actual
  technical task; managed simulations or array-processing substitutes would
  not complete those exercises. These are explicit remaining work, not excluded
  conceptual questions or completed implementations.

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

At the current checkpoint, native standalone and separate-module runs each cover
**655 solutions / 993,970 solution case executions**, with **655 rejected starters**
and the same number of starter case observations. This is actual execution.
Structural inventory/catalog checks do not grant semantic review or execution
credit. Receipt reuse requires matching submitted source, harness, cases, actual
grader and toolchain fingerprints. The final application-callable run is tracked
separately in `.epi-runs/ctci6-callable-final131/`; its results must be reconciled
against final source before publication. Original-bank receipts are reused only
where current per-pair fingerprints match; changed cases are reexecuted.

Last K Lines (12.1) reads an actual native temporary file in every language. Blank
lines are records, EOF is separate, and the final LF is not an extra blank line.
Fifteen compiled regressions reject blank-line sentinels, reversed suffixes and
file mutation; all five HTTP submissions pass 537 cases each. Tail memory bounds
come from reviewing actual streaming code, not a claim of measured process heap.
Other resource, identity, randomness and native-worker observers have separate
regression receipts and explain their measured scope.

All 329 backend tests pass at this checkpoint. Frontend/build/browser results and
final whole-bank application runs are tracked in `checkpoint.json` as they finish.
The Solution tab's independent language dropdown is immediately above the code;
code, explanation and trace switch together while editable drafts remain intact.
The existing theme and local formatter features remain integrated.

Reproduction uses `scripts/ctci6/audit.py` for evidence integrity,
`verify_runtime.py --starters` for fingerprinted submitted modules, the chapter
verifiers for standalone authoring, targeted `test_*` grader regressions, and
`scripts/SolutionsAudit` for actual displayed application-callable corpus runs.
The audit's publication gate remains closed while the eight candidate contracts
and final integrated acceptance are incomplete. No CTCI changes have been pushed.
