Observe how two correct-looking increments can lose an update.

## Core idea

An increment can consist of a read, local arithmetic, and a write. If two threads read the same old value, each can compute the same new value and overwrite the other’s contribution. A lock must cover the entire read-modify-write sequence to protect this invariant.

## Try the boundaries

A thread pauses after reading; writes occur in reverse order; a lock protects only the final assignment.

For each case, write down the expected behavior before choosing an implementation. State whether invalid input is rejected or is outside the contract.

## Tradeoffs

Mutual exclusion prevents this particular race, but it does not automatically solve deadlock, starvation, or visibility for unrelated state. Define which invariant each lock protects and use a consistent acquisition order when several locks are involved.

## Your design exercise

Use the simulator to produce a final counter of one, then repeat with the lock enabled.

Use the notes panel to record your assumptions, a worked example, and a failure case. Then explain how you would test the result. Reviewing this companion is a self-assessment; it does not grade the corresponding book exercise.
