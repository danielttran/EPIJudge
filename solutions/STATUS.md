# Solutions acceptance

Branch: `codex/add-csharp-solutions`, based on completed Blind75 tip
`2b5d19f2361a9199b2b46406c17bb8b9f71305eb`. No merge or deployment.

The bank contains 334 runnable questions and 1,670 displayed algorithm solutions:

| Collection | Questions | Five-language solutions |
| --- | ---: | ---: |
| EPI | 218 | 1,090 |
| Blind 75 | 75 | 375 |
| Interview Cake | 41 | 205 |
| Total | 334 | 1,670 |

Every C# article includes an approach, correctness argument, original executable
walkthrough, complexity and edge cases. The Solution tab follows the selected
language while preserving editor drafts. Interview Cake uses independently
authored wording, examples, algorithms, tests and three local diagrams. All seven
complete factual contract batches are saved in its provenance manifest; the five
excluded conceptual/design/puzzle entries are not imported. Original EPI and
Blind 75 statements, corpora, upstream references and contracts remain intact.

The current-code acceptance gate passed all 1,670 question/language pairs through
the same submission runner as the editor: 409,667 corpus cases per language,
2,048,335 accepted case evaluations in total. Additional isolated checks passed
114 boundary cases in every language (570 evaluations across 340 executions)
and all 334 original C# walkthroughs. Interview Cake separately passed 615
starter/correct/incorrect executions: 205 executable starters, 205 actual correct
algorithms and 205 rejected incorrect fixtures, with all 13,245 execution rows
archived and hash-verified. The committed [per-question evidence](validation-results.json)
records current source, notes, corpus and compiled-harness hashes. The final
catalog SHA256 is `b5fe663e12cc8043e89e4eaba6701a8fdbddfc2d17957ae3924c6ec18fae1c9c`.

Other completed checks: 185 backend tests with none skipped; 172 frontend tests
with scoped coverage gates; 5,390 solution HTTP checks and 14 Chromium groups;
176 Interview Cake HTTP checks including all five actual timeouts; 153 existing
Blind 75 HTTP checks and six Chromium groups including all five timeouts; 22
existing website submission checks, 24 native checks and 58 practice/storage
checks. Existing WebAudit passed 274 checks over 406,899 corpus rows and 595,586
typed arguments. Wording validation passed all 218 EPI provenance records,
73 translated examples and 8,850 sensitive cases. All 38 local diagrams decode
with external origins blocked; the three new SVGs were also rendered and visually
reviewed against their examples. Locked-dependency installation, strict frontend
and warning-as-error .NET builds, analyzers, lint, reproduction checks and an
isolated fresh-checkout build/test passed.

The audit repaired real defects before final acceptance: constructor/reset and
query validation in stateful native/Python wrappers; empty and negative rotation;
zero-capacity circular-buffer growth; signed arithmetic overflow; UTF-8 versus
UTF-16 substring positions; and wide-range random sampling/checker arithmetic.
The quadratic birthday-window checker was replaced only inside independently
authored solution scaffolds by a linear-time equivalent. Each language's proof
covered 73,812 exhaustive window counts; additional comparisons matched the
unchanged original predicate (168 Python, 612 C++, 720 Java). Incorrect constant,
cycling and out-of-range sampler fixtures retain all 100,000 samples per attempt
and five retries. Original thresholds and upstream framework files are unchanged.

The inherited random screen remains statistical. One Java full-range run rejected
its sampled streams; an unchanged focused repeat and complete 114-case rerun
passed. Twenty predefined seeds (0 through 19) also passed unchanged. The initial
failure is preserved in the raw evidence, and no seed, sample count, tolerance or
retry rule was altered to obtain final acceptance. Finite tests do not prove
universal random independence or asymptotic complexity.

Local verification used Debian 13, .NET SDK 10.0.402, Node 24.19.0, C++17 with
GCC 14.2, JDK 21.0.8, and Python 3.12.14 plus isolated Python 3.14.8. All current
334 Python sources, complete corpora, 114 boundaries and Interview Cake fixtures
have Python 3.14.8 evidence. The complete matrix is Linux validation; Windows
build/native smoke/storage behavior is checked by the existing Windows CI job,
not claimed as a full Windows algorithm matrix. CI results belong to the final
commit's workflow runs. Raw reports and recovery snapshots are preserved in the
cloud workspace; CI uploads the corresponding execution artifacts.
