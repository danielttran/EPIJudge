Define exactly which textual differences your application should ignore.

## Core idea

Build a documented pipeline for Unicode normalization, case handling, tokenization, and any stemming or lemmatization. Preserve original input or offsets when users need highlights. Version the pipeline so search indexes and query processing can use compatible transformations.

## Try the boundaries

Accents; composed and decomposed Unicode; identifiers; language-specific casing; words whose stems collide.

For each case, write down the expected behavior before choosing an implementation. State whether invalid input is rejected or is outside the contract.

## Tradeoffs

Normalization can improve matching while destroying distinctions that matter for display or meaning. Stemming is a heuristic reduction, not a universal grammar engine. Evaluate with examples from the supported languages and plan how to rebuild indexes after a pipeline change.

## Your design exercise

Write a transformation contract and identify which original information must survive.

Use the notes panel to record your assumptions, a worked example, and a failure case. Then explain how you would test the result. Reviewing this companion is a self-assessment; it does not grade the corresponding book exercise.
