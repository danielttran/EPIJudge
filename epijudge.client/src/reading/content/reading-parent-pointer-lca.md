Walk upward from two nodes without traversing their entire tree.

## Core idea

Count the parent links from each node to its root. Lift the deeper node until both depths match, then move both pointers upward together. Their first shared node is the lowest common ancestor. Compare node identity, not stored values: distinct nodes can contain equal values.

## Try the boundaries

One node is the other’s ancestor; the nodes are identical; the nodes belong to different trees.

For each case, write down the expected behavior before choosing an implementation. State whether invalid input is rejected or is outside the contract.

## Tradeoffs

Time is proportional to the tree height and auxiliary space is constant. First compare roots if disconnected trees are possible. A contract that assumes a shared root should state that assumption.

## Your design exercise

Draw two paths with different lengths and trace their meeting point.

Use the notes panel to record your assumptions, a worked example, and a failure case. Then explain how you would test the result. Reviewing this companion is a self-assessment; it does not grade the corresponding book exercise.
