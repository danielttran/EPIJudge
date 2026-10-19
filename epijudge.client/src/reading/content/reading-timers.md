Separate the time a task becomes ready from the time it actually executes.

## Core idea

Keep pending tasks in a min-heap ordered by a monotonic deadline and a sequence number for ties. A scheduler waits until the earliest deadline, removes ready tasks, and hands their work to an executor. Inserting an earlier deadline must wake the scheduler so it can recompute its wait.

## Try the boundaries

A new earliest task; cancellation during dispatch; a slow callback; clock adjustments; shutdown with pending tasks.

For each case, write down the expected behavior before choosing an implementation. State whether invalid input is rejected or is outside the contract.

## Tradeoffs

Do not run an arbitrary callback while holding the heap lock. Define whether recurring tasks use fixed delays after completion or fixed target times, and decide what happens when work falls behind. Real-time execution guarantees require more than an ordinary application timer.

## Your design exercise

Trace insertion, cancellation, wakeup, and dispatch for three tasks.

Use the notes panel to record your assumptions, a worked example, and a failure case. Then explain how you would test the result. Reviewing this companion is a self-assessment; it does not grade the corresponding book exercise.
