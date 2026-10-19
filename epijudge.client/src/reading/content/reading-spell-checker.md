Separate recognizing a suspicious word from proposing a correction.

## Core idea

Normalize text while preserving enough information to display the original. Look up known terms and generate plausible candidates for unknown tokens. Rank candidates using frequency, edit cost, and context. Include an unchanged option so the service can abstain when confidence is low.

## Try the boundaries

A person’s name; a valid word used in the wrong context; mixed languages; punctuation; a very long token.

For each case, write down the expected behavior before choosing an implementation. State whether invalid input is rejected or is outside the contract.

## Tradeoffs

An edit-distance threshold bounds candidate generation but does not determine semantic correctness. Limit work per token, protect private input, and measure both useful corrections and harmful replacements. An interactive suggestion interface can tolerate uncertainty better than silently changing text.

## Your design exercise

Define an abstention policy and three tests where automatic replacement would be harmful.

Use the notes panel to record your assumptions, a worked example, and a failure case. Then explain how you would test the result. Reviewing this companion is a self-assessment; it does not grade the corresponding book exercise.
