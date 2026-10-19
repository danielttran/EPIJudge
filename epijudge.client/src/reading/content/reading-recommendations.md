Connect candidate retrieval, ranking, and product evaluation.

## Core idea

Retrieve a manageable candidate set using user history, item relationships, or broad popularity. Score candidates for the current context, then rerank for diversity, policy, freshness, and availability. Return explanations and a safe fallback when personalization has too little evidence.

## Try the boundaries

A new user; a new item; stale inventory; a popular item dominating results; delayed feedback.

For each case, write down the expected behavior before choosing an implementation. State whether invalid input is rejected or is outside the contract.

## Tradeoffs

Offline ranking metrics are useful diagnostics but do not establish user benefit. Define an online experiment and guardrails such as latency, coverage, and unwanted repetition. Avoid training on information that would not have existed at the time of prediction.

## Your design exercise

Sketch a cold-start fallback and an experiment that could falsify your design.

Use the notes panel to record your assumptions, a worked example, and a failure case. Then explain how you would test the result. Reviewing this companion is a self-assessment; it does not grade the corresponding book exercise.
