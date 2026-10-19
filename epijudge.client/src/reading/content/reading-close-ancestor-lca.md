Optimize for an ancestor that lies close to the queried nodes.

## Core idea

Alternate upward steps from the two starting nodes. Record each visited node by identity in a set. Stop when a step reaches an identity already visited. With acyclic parent links and a common root, the first repeat identifies the lowest common ancestor.

## Try the boundaries

Identical starting nodes; an immediate parent-child pair; disconnected roots; repeated values in different nodes.

For each case, write down the expected behavior before choosing an implementation. State whether invalid input is rejected or is outside the contract.

## Tradeoffs

Depth alignment needs constant extra space but may walk to a distant root first. Alternating search spends space on visited ancestors and can stop early when the answer is nearby. Neither method should assume values uniquely identify nodes.

## Your design exercise

Compare the number of parent steps for a close ancestor beneath a very distant root.

Use the notes panel to record your assumptions, a worked example, and a failure case. Then explain how you would test the result. Reviewing this companion is a self-assessment; it does not grade the corresponding book exercise.
