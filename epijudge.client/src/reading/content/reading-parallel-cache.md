Avoid duplicate expensive work without holding one global lock during computation.

## Core idea

A cache entry can represent an in-flight computation as well as a completed value. Under a short lock, either install a promise for a missing key or join the existing promise. Perform the expensive work outside the lock and complete the promise for every waiter.

## Try the boundaries

The computation fails; a caller cancels; a value expires; the cache fills; one key becomes very popular.

For each case, write down the expected behavior before choosing an implementation. State whether invalid input is rejected or is outside the contract.

## Tradeoffs

Choose whether failures are cached and whether one caller’s cancellation can cancel shared work. Eviction must distinguish a completed value from an in-flight computation. Bound memory and work queues separately; caching alone is not overload control.

## Your design exercise

Draw the state transitions for missing, in-flight, completed, expired, and failed entries.

Use the notes panel to record your assumptions, a worked example, and a failure case. Then explain how you would test the result. Reviewing this companion is a self-assessment; it does not grade the corresponding book exercise.
