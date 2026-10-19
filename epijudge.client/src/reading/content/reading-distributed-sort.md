Produce globally ordered output from partitions that can be processed independently.

## Core idea

Sample keys to choose range boundaries. Assign each record to a range partition, sort each partition, and publish the partition order with a manifest. All keys in an earlier range must compare no greater than keys in a later range. Local sorting alone does not establish global order.

## Try the boundaries

Many duplicate keys; a heavily skewed range; a failed worker; partial output; records too large for memory.

For each case, write down the expected behavior before choosing an implementation. State whether invalid input is rejected or is outside the contract.

## Tradeoffs

Use external merge sorting when a partition exceeds memory. Publish completed output atomically and make retries idempotent. Define stable tie handling if equal keys must preserve an input order. Hash partitioning balances some workloads but cannot simply be concatenated into globally sorted output.

## Your design exercise

Specify the partition invariant, retry protocol, and a skew mitigation strategy.

Use the notes panel to record your assumptions, a worked example, and a failure case. Then explain how you would test the result. Reviewing this companion is a self-assessment; it does not grade the corresponding book exercise.
