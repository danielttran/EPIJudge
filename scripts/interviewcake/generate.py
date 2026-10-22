"""Reproduce independent collection content, exact displayed solutions and fixtures."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys

from banktypes import HEADER
from corpus import cases
from interfaces import EXT, full_source, interfaces
from specs import LANGUAGES, ROOT, S

sys.path.insert(0, str(ROOT / "scripts"))
from clarity.content import apply_question, questions as clarity_questions

ATTRIBUTION = "Original EPI Practice implementation and explanation. Task identity and technical compatibility facts are attributed to Interview Cake; no course prose, examples, solution code or artwork are included. No affiliation is implied."
WALK = {
    "second-largest-item-in-bst": "In the first example, follow 12 -> 20 -> 25. The largest key 25 has no left child, so its parent 20 is the predecessor and the answer.",
    "stock-price": "For [11,7,13,4,10], the sale at 13 follows the earlier minimum 7 and gives 6. After the minimum becomes 4, selling at 10 also gives 6. Thus the best required transaction returns 6.",
    "balanced-binary-tree": "The first example has leaves 1, 3 and 9, all at depth 2, giving spread 0. The second example has only one leaf at depth 3, so its deepest and shallowest leaves are the same leaf and it also passes.",
    "bst-checker": "In the second example, key 8 lies inside the right subtree of root 10. Although 8 is smaller than its immediate parent 16, it violates the inherited lower bound 10, so the answer is false.",
    "bracket-validator": "In a{b[c](d)}, the stack changes through {, {[, {, {(, {, and empty as the paired delimiters close. Letters have no effect, and the final empty stack gives true.",
    "cafe-order-checker": "Serving [5,8,3,9] consumes dine-in 5, then take-out 8 and 3, then dine-in 9. Each source advances in its own order and both are exhausted, so the interleaving is valid.",
    "nth-fibonacci": "Starting with 0 and 1 yields the sequence 0,1,1,2,3,5,8,13. Index 7 therefore returns 13, with only the last two values needed at each step.",
    "delete-node": "The target object contains 4 in [9,4,7,2]. Copy 7 into that object and point it to the node containing 2. The reachable sequence becomes [9,7,2], while an alias to the bypassed successor still refers to its separate original object.",
    "linked-list-cycles": "The second example links the tail of [2,5,9,1] back to the original node containing 5. Pointer identities eventually coincide within that cycle. Equal payloads in the first example alone do not create any cycle.",
    "find-duplicate-files": "The first directory contains a.txt and nested/b.txt with equal sizes and sampled bytes. Their modification times are 1000 and 2000, so the result labels a.txt as the suspected original and nested/b.txt as the suspected copy. The files are never changed.",
    "find-duplicate-optimize-for-space": "For [1,3,4,2,3], the lower value half 1..2 contains two entries, fitting its capacity. The repeated value therefore remains in 3..4; another count isolates 3.",
    "find-duplicate-optimize-for-space-beast-mode": "For [4,1,3,4,2], follow the index/value links until the slow and fast walkers meet. Restarting one walker at the initial index and advancing both locates the cycle entry 4, which is repeated. Other valid inputs can have several acceptable repeated values.",
    "find-rotation-point": "For [mint,oak,ant,birch,cedar], the wrap separates oak from ant. The smallest word is ant at index 2; binary comparisons discard portions that cannot contain that minimum.",
    "graph-coloring": "The first graph is a triangle. A valid result gives its three nodes red, blue and green, making every edge join different colors. The example output true denotes validated color fields and preserved graph structure, rather than a return value from the void method.",
    "highest-product-of-3": "In [-8,-5,2,4], the two negative values produce 40; multiplying by 4 gives 160. Considering only the three numerically largest values would miss this optimum.",
    "queue-two-stacks": "After enqueueing 4 then 9, transfer the input stack when the first dequeue occurs, yielding 4. Enqueueing 2 does not disturb 9 waiting in the output stack, so later removals return 9 then 2.",
    "shuffle": "For [4,8,1], position zero has three choices and position one has two. Each of the six permutations therefore has probability 1/6. The example output true means the mutation and randomness properties passed; no exact permutation is prescribed.",
    "inflight-entertainment": "For durations [35,60,45,20] and target 80, duration 20 finds the earlier complement 60. A single duration 40 would not fill target 80 by itself, but two separate 40 entries would.",
    "kth-to-last-node-in-singly-linked-list": "For k=2 and [5,8,1,6], the selected original node contains 1. It has zero-based position 2, which is the adapter output; the submitted method returns that existing node object.",
    "largest-stack": "Push 5 then 9: the running maximum becomes 9. Pop returns 9 and restores the earlier maximum 5. Two equal maxima each retain a record, so popping one does not discard the other.",
    "coin": "Amount 8 with denominations 2,3,5 has three combinations: four 2s; one 2 and two 3s; or one 3 and one 5. Reordering those coins does not create additional combinations.",
    "merge-sorted-arrays": "For [1,4,4] and [2,4,9], take 1 then 2, preserve all three occurrences of 4, and finish with 9. The new result is [1,2,4,4,4,9].",
    "merging-ranges": "Sort [9,12],[1,4],[4,7],[10,14] by start. The touching first pair merges to [1,7], while the overlapping later pair merges to [9,14]. A gap remains between 7 and 9.",
    "mesh-message": "In the first network, a reaches b and c in one edge, then d in two. Both [a,b,d] and [a,c,d] are valid shortest routes; the example chooses the first without requiring that tie-breaking order.",
    "compress-url-list": "Insert https://a/b, then its shorter prefix https://a: both are new complete keys. Reinserting https://a/b returns false. Extending it to https://a/b/c again returns true because terminal membership is separate from prefix existence.",
    "matching-parens": "In x(ab(cd)e)y, the opener at index 1 contains another pair at indices 4 and 7. Closing the inner pair leaves the outer depth active, so the matching outer closer is index 9.",
    "permutation-palindrome": "For aabbc, a and b each occur twice and c once. Put c at the center and mirror the pairs to form abcba. Two odd frequencies, as in aabc, cannot both occupy the single center.",
    "product-of-other-numbers": "For [2,0,-3,4], every result except position 1 includes the zero factor. Excluding that zero yields 2*(-3)*4=-24, so the result is [0,-24,0,0]. No division is needed.",
    "rectangular-love": "The first rectangles span x=1..7 and x=4..9, so the shared x interval is 4..7. Their y intervals share 2..4. The intersection is therefore (LeftX=4, BottomY=2, Width=3, Height=2).",
    "recursive-string-permutations": "For ab, recursively permuting b gives {b}. Insert a before and after b to obtain {ab,ba}. For empty input there is one permutation, the empty string, rather than no results.",
    "reverse-linked-list": "For the original nodes 3 -> 8 -> 1, redirect 3 to null, then 8 to 3, then 1 to 8. Return the original node containing 1. The observed values become [1,8,3], and every node retains its own original value.",
    "reverse-string-in-place": "For cloud, swap c with d and l with u; the middle o remains in place. The same character array now contains duolc, which is the observed example output.",
    "reverse-words": "Reverse foxes run fast to tsaf nur sexof, then reverse each word individually. The same array now reads fast run foxes; no word has its spelling changed in the final result.",
    "simulate-5-sided-die": "If the supplied sequence begins 6,7,5, reject the first two source values and accept 5. Conditioning on any accepted source outcome makes each value 1..5 equally likely. The example output true summarizes properties, not a fixed die return.",
    "simulate-7-sided-die": "Two source draws give 25 equally likely states. Keep states 0..20, which contain three copies of each remainder 0..6; reject 21..24 and retry. The example output true summarizes the injected-source and distribution checks.",
    "temperature-tracker": "Insert 4,10,4. The minimum is 4, maximum 10, sum 18 and count 3, so the mean is 6 and mode 4. With only 3 and 8 inserted, either mode is acceptable; the displayed example chooses scalar 3.",
    "cake-thief": "At capacity 11, one weight-5/value-13 item and two weight-3/value-7 items use all 11 weight and total 27 value. A zero-weight positive-value type instead yields an unbounded optimum, represented by the normalized infinite error.",
    "find-unique-int-among-duplicates": "For [14,3,14,8,3], the two 14s cancel and the two 3s cancel under XOR, leaving 8. Array order does not affect the result.",
    "top-scores": "For [3,8,3,0,5] and maximum 8, the buckets contain one 8, one 5, two 3s and one 0. Emit them in that order to get [8,5,3,3,0].",
    "which-appears-twice": "XOR [3,1,4,2,3] with the required range [1,2,3,4]. One occurrence of every required key cancels, leaving the extra 3. No overflowing arithmetic sum is formed.",
    "word-cloud": "In Owls fly; OWLS don't crawl. Fly-by owls!, the case variants become the same key owls, counted three times. Internal punctuation keeps don't and fly-by as complete tokens under the disclosed bank grammar.",
}


def example_explanation(s, index):
    mode = s["mode"]
    text = WALK[s["sourceId"]] if index == 0 else s["approach"]
    if mode in ("color", "shuffle", "rand5", "rand7") and index != 0:
        text += " true denotes successful contract/property validation; it is not the submitted method return value."
    if mode in ("chars", "words", "delete", "reverse_list") and index != 0:
        text += " The output shows the observed mutated sequence."
    if mode == "kth" and index != 0:
        text += (
            " The adapter displays the zero-based index of the returned original node."
        )
    if mode == "temperature" and index == 2:
        text = "After inserting 3 and 8, both frequencies equal one. GetMode may return either scalar 3 or scalar 8; this example shows 3."
    return text


def configuration(s, lang):
    fields = {
        "ClassName": s["className"],
        "Method": s["method"],
        "Kinds": [p["type"] for p in s["params"]],
        "Result": s["result"],
        "Mode": s["mode"],
    }
    if lang == "python":
        return "\n".join(k + " = " + repr(v) for k, v in fields.items())
    if lang == "javascript":
        return "\n".join(
            "const " + k + " = " + json.dumps(v) + ";" for k, v in fields.items()
        )
    if lang in ("csharp", "java"):
        prefix = "static readonly " if lang == "csharp" else "static final "
        return "\n".join(
            prefix
            + ("string[]" if lang == "csharp" else "String[]")
            + " "
            + k
            + " = "
            + ("[" if lang == "csharp" else "{")
            + ", ".join(json.dumps(x) for x in v)
            + ("];" if lang == "csharp" else "};")
            if isinstance(v, list)
            else prefix
            + ("string" if lang == "csharp" else "String")
            + " "
            + k
            + " = "
            + json.dumps(v)
            + ";"
            for k, v in fields.items()
        )
    module = ROOT / "scripts/interviewcake/cpp_config.py"
    if module.exists():
        spec = importlib.util.spec_from_file_location("ic_cpp_config", module)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        return m.configuration(s)
    return "// C++ typed dispatch generation pending."


def generate(check=False):
    def emit(path, text):
        if check:
            if not path.is_file() or path.read_text(encoding="utf-8") != text:
                raise ValueError(
                    "Stale generated artifact: " + str(path.relative_to(ROOT))
                )
        else:
            if not path.is_file() or path.read_text(encoding="utf-8") != text:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8", newline="\n")

    emit(ROOT / "scripts/interviewcake/specs.json", json.dumps(S, indent=2) + "\n")
    author_interfaces = [
        dict(
            spec,
            interfaces={language: interfaces(spec, language) for language in LANGUAGES},
        )
        for spec in S
    ]
    emit(
        ROOT / "scripts/interviewcake/interfaces.json",
        json.dumps(author_interfaces, indent=2) + "\n",
    )
    for language in LANGUAGES:
        emit(
            ROOT / "scripts/interviewcake" / ("header_" + language + ".txt"),
            HEADER[language].rstrip() + "\n",
        )
    definitions = []
    coverage = []
    for s in S:
        rows = cases(s)
        emit(
            ROOT / "interviewcake/cases" / (s["id"] + ".json"),
            json.dumps(rows, indent=2) + "\n",
        )
        d = {
            k: v
            for k, v in s.items()
            if k
            not in (
                "examplesData",
                "approach",
                "timeComplexity",
                "spaceComplexity",
                "correctness",
                "edgeCases",
            )
        }
        d["constraints"] = [s["bankConventions"]]
        legends = {
            "tree": "Example trees use compact breadth-first order; null marks a missing child, and missing children have no child slots. [] is an empty tree.",
            "list": "Example linked lists encode node values in head-to-tail order; identity-sensitive adapter outputs and extra indices are described above.",
            "rect": "Example rectangles are [LeftX,BottomY,Width,Height].",
            "meetings": "Example intervals are [StartTime,EndTime] pairs.",
            "cakes": "Example item types are [Weight,Value] pairs.",
            "files": "Example input describes ordinary files created in a controlled temporary directory. The submitted method receives that directory's full path, not the descriptor records.",
        }
        d["constraints"] += [
            text
            for kind, text in legends.items()
            if any(p["type"] == kind for p in s["params"])
        ]
        if s["mode"] in ("rand5", "rand7"):
            d["constraints"].append(
                "The example input is a judge-only source-draw prefix, not a submitted-method argument. The method has no value arguments; after the forced prefix, an injected deterministic stream supplies further valid draws."
            )
        d["examples"] = [
            {
                "input": json.dumps(a, ensure_ascii=False),
                "output": json.dumps(e, ensure_ascii=False),
                "explanation": example_explanation(s, i),
            }
            for i, (a, e) in enumerate(s["examplesData"])
        ]
        d["testCount"] = len(rows)
        d["comparison"] = "unordered" if s["mode"] == "set" else "ordered"
        d["starters"] = {}
        d["harnessConfigs"] = {}
        for language in LANGUAGES:
            api = interfaces(s, language)
            filename = (
                "Solution.cs"
                if language == "csharp"
                else "Solution.java"
                if language == "java"
                else "solution." + EXT[language]
            )
            d["starters"][language] = {
                "signature": api["signature"],
                "starterCode": full_source(s, language, api["starter"]),
                "filename": filename,
                "runtime": language,
            }
            d["harnessConfigs"][language] = configuration(s, language)
            algorithms = json.loads(
                (
                    ROOT
                    / "scripts/interviewcake"
                    / ("algorithms_" + language + ".json")
                ).read_text(encoding="utf-8")
            )
            assert len(algorithms) == 41 and s["id"] in algorithms
            code = full_source(s, language, algorithms[s["id"]]["code"])
            wrong = full_source(s, language, algorithms[s["id"]]["incorrectCode"])
            assert len(code) < 40000
            dest = ROOT / "solutions" / language / (s["id"] + "." + EXT[language])
            emit(dest, code)
            fixture = (
                ROOT
                / "interviewcake/fixtures/incorrect"
                / language
                / (s["id"] + "." + EXT[language])
            )
            emit(fixture, wrong)
            notes = {
                "explanation": s["approach"],
                "correctness": s["correctness"],
                "walkthrough": WALK[s["sourceId"]],
                "edgeCases": [
                    x.strip() for x in s["edgeCases"].split(";") if x.strip()
                ],
                "timeComplexity": s["timeComplexity"],
                "spaceComplexity": s["spaceComplexity"],
                "attribution": ATTRIBUTION,
            }
            trace_file = ROOT / "scripts/interviewcake/walkthroughs.json"
            if trace_file.exists():
                trace = json.loads(trace_file.read_text(encoding="utf-8")).get(s["id"])
                if trace:
                    notes["walkthrough"] = trace["walkthrough"]
                    notes["walkthroughCase"] = trace["walkthroughCase"]
            if s["sourceId"] == "which-appears-twice" and language in (
                "python",
                "javascript",
                "cpp",
            ):
                notes["walkthrough"] = WALK[s["sourceId"]]
            notes.update(algorithms[s["id"]].get("notes", {}))
            note = (
                ROOT / "solutions/notes" / (s["id"] + ".json")
                if language == "csharp"
                else ROOT / "solutions/notes" / language / (s["id"] + ".json")
            )
            emit(note, json.dumps(notes, indent=2, ensure_ascii=False) + "\n")
            coverage.append(
                {
                    "problemId": s["id"],
                    "collection": "interviewcake",
                    "language": language,
                    "source": str(dest.relative_to(ROOT)),
                    "codeSha256": hashlib.sha256(code.encode()).hexdigest(),
                    "corpusSha256": hashlib.sha256(
                        json.dumps(rows, indent=2).encode() + b"\n"
                    ).hexdigest(),
                    "testCount": len(rows),
                    "incorrectReason": algorithms[s["id"]]["incorrectReason"],
                    "validationEvidence": "See solutions/validation-results.json and the current hash-matched 615-execution Interview Cake audit.",
                }
            )
        diagrams = {
            "balanced-binary-tree": (
                "global-leaf-depth.svg",
                "A single-leaf chain satisfies the global rule; leaves at depths one and three do not.",
            ),
            "rectangular-love": (
                "rectangle-overlap.svg",
                "Original rectangles intersect in the region with lower-left (4,2), width 3 and height 2.",
            ),
            "delete-node": (
                "delete-node-aliases.svg",
                "The target node object remains, copying its successor value and bypassing that separate successor object.",
            ),
        }
        if s["sourceId"] in diagrams:
            d["diagram"] = "/interviewcake/diagrams/" + diagrams[s["sourceId"]][0]
            d["diagramAlt"] = diagrams[s["sourceId"]][1]
        definitions.append(d)
    reviewed = clarity_questions()
    definitions = [apply_question(problem, reviewed) for problem in definitions]
    emit(
        ROOT / "interviewcake/catalog.json",
        json.dumps(definitions, indent=2, ensure_ascii=False) + "\n",
    )
    emit(ROOT / "interviewcake/coverage.json", json.dumps(coverage, indent=2) + "\n")
    print(
        "Generated",
        len(definitions),
        "questions,",
        len(coverage),
        "displayed algorithms,",
        sum(d["testCount"] for d in definitions),
        "cases across",
        len(LANGUAGES),
        "languages.",
    )


if __name__ == "__main__":
    generate("--check" in sys.argv)
