# Workflow review, 2026-10-23

## Current evidence and time accounting

37 reviewed coding exercises, 185 language implementations, and 34,835 correct
case evaluations at each of the standalone and separate-module layers. The local
website contains 371 problems. Four additional chapter-eight implementations are
drafts, not counted. Nothing in this collection has been pushed.

Logs in `/tmp/ctci6*.log` span 08:04:25–11:10:02 UTC (3h 5m 37s).
This is a log observation window, not an activity stopwatch. The first authoring
checkpoint is at 08:09 and the theme/formatter commit predates that at 05:56.

Measured samples, including repeated invocations:

| Activity | Evidence | Recorded duration |
| --- | --- | --- |
| Standalone compile/run | 18 logs with elapsedSeconds | 203.07 seconds |
| Separate submitted-module invocations | 13 Invocation elapsed records | 440.52 seconds |
| Backend test bodies | 8 test-run duration records | 27 seconds |
| Frontend test invocations | 2 Duration records | 20.75 seconds |
| Frontend production builds | 2 built-in records | 14.50 seconds |
| Eight explicit audit/runner builds | Time Elapsed records | 16.30 seconds |
| Authoring / source research / infrastructure editing | No separate timers retained | Unmeasured |
| Application-per-pair compile/run and browser wall time | Incomplete wall-time records | Unmeasured |
| Idle or CI waiting during this window | No interval evidence; no collection push | Unmeasured; cannot infer idle from log gaps |

These samples are not a complete mutually exclusive allocation of elapsed time.
In particular, generated harnesses measure algorithm case time but historically
did not record each compiler process's wall time. The workflow now records
compile-and-execute wall seconds per newly executed module packet. No ETA is
inferred from these incomplete measurements.

## Findings

* Standalone validation was repeated 18 times, including final source-hash
  refreshes for seven-exercise batches. Compiling a whole chapter again for prose
  or authoring metadata changes is avoidable. Runtime fingerprints correctly
  reused unchanged packets (a 185-pair cached invocation took 0.37 seconds).
* Small batches repeatedly rebuilt application audit binaries, regenerated
  catalogs, and exercised both legacy and callable application entry points.
  Those are necessary final integration gates, but need not all repeat after
  each independent exercise when the adapter is unchanged.
* The initial staging/export/corpus/grader work was substantial. Separate child
  modules remain necessary to prove the submission boundary and prevent expected
  answers leaking into tested code. Further independent application runners or
  a new optimization framework are unnecessary: use SubmissionRunner,
  CtciStagingRunner, SolutionsAudit, and the existing HTTP/browser tools.
* A browser check repeated because its unscoped text locator matched both the
  statement and solution trace. Another repeat followed a real public-Java-class
  filename correction. Keep those focused regression checks; do not treat the
  first failure as an algorithm failure or rerun unrelated algorithms.
* Inventory research reached diminishing returns. Record the 29 unlocated
  references and access denial. Do not spend further inventory time while known
  coding candidates remain.

## Revised batch pipeline

1. Finish four known drafts together: 8.3, 8.12, 8.13, 8.14. Freeze contracts,
   independent oracles, and tests before final generation. Review wording,
   language-specific algorithms, correctness, traces, and complexity explicitly.
2. Preflight every batch's cases/examples before generation writes anything.
   Generate once after that preflight. Retain old passing artifacts if preflight
   fails; never register an unverified draft.
3. Compile the standalone batch once per language/variant. Then execute each new
   submitted module against its complete independent corpus and reject starters.
   Reuse receipts only when source, harness, cases, grader and toolchain match.
   Prose changes require semantic review and regeneration checks, not recompiling
   byte-identical submitted source. Grader changes invalidate affected receipts.
4. Use two concurrent language process lanes where independent and measured to
   help. Each lane owns separate output directories; keep catalog generation,
   evidence writes, .NET shared-project builds, and integration serial. This is
   process concurrency inside one AI agent, not additional agents. Start serial
   if shared output ownership cannot be proved; do not add a concurrency system.
5. Export only reviewed, executed pairs into the local bank. Run affected grader,
   contract and backend tests; check actual HTTP execution for new adapter shapes.
   Reuse established generic UI checks until UI code or metadata shape changes.
6. At final complete integration, run whole-bank corpus/boundary/starter and
   walkthrough/fixture acceptance, frontend/backend/build/browser accessibility
   checks against final fingerprints. Then review remote concurrency, push
   without force, and monitor exact-commit CI. Structural coverage is never
   semantic review or execution credit.

Next measurable checkpoint: 41 approved local coding exercises / 205 language
pairs, with the four new exercises' actual case totals, starter rejection counts,
per-packet wall times and unchanged-pair cache reuse reported. If a new exercise
fails, report it separately; do not count a draft or weaken its technical task.

## First optimized batch result

8.3, 8.12, 8.13 and 8.14 passed all five languages. Coverage is now
41 exercises / 205 language pairs / 52,645 correct cases at each execution
layer, with 205 rejected starters. Separate-module invocation: 72.68 seconds,
with unaffected matching receipts reused. Standalone eleven-exercise chapter
run: 15.17 seconds; final verifier-input reconciliation run: 13.78 seconds.
262 backend tests pass. Five real HTTP submissions across all five languages
accepted the new API shapes; local bank registration is 375 problems.
A new C# grader local-variable name collision was caught at compile time and
fixed before integration. Final whole-bank acceptance remains pending.

## Immediate implementation results

The requested plan was applied without waiting for approval. The known-exercise
batches progressed from 37 to 41, 44, 50 and 54 reviewed/local coding problems.
The corresponding submitted-module invocations took 72.68, 85.85, 60.82 and
41.13 seconds. The last batch reused unchanged earlier receipts and tested only
new/changed packets. Current coverage is 270 solutions / 270 rejected starters /
235,700 correct cases per execution layer. All 263 backend tests pass; the local
bank contains 388 problems and the current semantic ledger has 388 statements
and 1,940 solutions. Whole-bank final acceptance and publication are still pending.

The batch-four module runner reused earlier adapters and ran to completion before
this diagnostic handoff. There is no startup/usage/permission blocker. Progress
commentary was emitted; why the parent read view omitted it is uncertain. Current
artifacts and local commits provide independent, timestamped execution evidence.

Small changes made: all-example/corpus preflight before chapter-eight writes,
per-module compilation/execution wall time, shared typed adapter and standalone
loop for chapter sixteen, and receipt-preserving batches. No extra AI agents,
new optimization framework, denied-source retry or discarded test requirement.
No further inventory-gap research was done while known candidates remained.

Next bounded batch: six known chapter-17 candidates (17.1, 17.6, 17.9, 17.10,
17.16, 17.21), after checking their legitimate source contracts. Reuse current
primitive/array adapters. Checkpoint target is 60 approved local coding problems /
300 executed language pairs, actual case counts and packet wall times. If any
candidate needs a distinct model or cannot preserve its original task, keep it
explicitly pending and substitute another already established coding candidate;
do not invent a replacement exercise. No calendar ETA is supported by the logs.
