Explain eligibility, selection, delivery, and accounting as separate decisions.

## Core idea

First filter campaigns by targeting rules, policy, and availability. Rank eligible candidates with an explicit objective and budget constraints. Delivery produces an impression event; later events may represent clicks or conversions. Assign event identifiers so retries do not multiply charges.

## Try the boundaries

A retry delivers the same event twice; a campaign exhausts its budget; a click arrives late; an event is fraudulent.

For each case, write down the expected behavior before choosing an implementation. State whether invalid input is rejected or is outside the contract.

## Tradeoffs

Low-latency selection and exact global accounting have different needs. Define acceptable budget overshoot, deduplication windows, privacy constraints, and attribution rules. Compare predicted performance with actual outcomes and account for feedback that can bias the training data.

## Your design exercise

Draw the selection path and the asynchronous accounting path with failure cases.

Use the notes panel to record your assumptions, a worked example, and a failure case. Then explain how you would test the result. Reviewing this companion is a self-assessment; it does not grade the corresponding book exercise.
