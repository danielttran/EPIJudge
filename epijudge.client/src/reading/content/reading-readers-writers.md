Choose an explicit access and fairness policy for shared data.

## Core idea

Readers may overlap only while the protected data is stable. Writers need exclusive access. Track active readers, an active writer, and waiting writers under a single coordination mechanism. Wait on predicates in a loop because waking does not guarantee that access is currently allowed.

## Try the boundaries

A continuous stream of readers; a waiting writer; cancellation while waiting; a writer that raises an exception.

For each case, write down the expected behavior before choosing an implementation. State whether invalid input is rejected or is outside the contract.

## Tradeoffs

Reader preference can starve writers. Writer preference can delay readers. A fair queue improves predictability but adds bookkeeping and may reduce throughput. Describe the policy before choosing a primitive, and release access in a finally block.

## Your design exercise

Write the admission predicates and explain whether a waiting writer can starve.

Use the notes panel to record your assumptions, a worked example, and a failure case. Then explain how you would test the result. Reviewing this companion is a self-assessment; it does not grade the corresponding book exercise.
