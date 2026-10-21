"""Run every original Interview Cake Python fixture through the real adapter.

This authoring check needs no .NET build. It executes the same generated support
header, user class and adapter, and applies the collection's semantic comparisons.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import math
import os
import subprocess
import sys
import tempfile
import time
from itertools import pairwise
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def equal(expected, actual):
    if isinstance(expected, dict):
        return (
            isinstance(actual, dict)
            and expected.keys() == actual.keys()
            and all(equal(value, actual[key]) for key, value in expected.items())
        )
    if isinstance(expected, list):
        return (
            isinstance(actual, list)
            and len(expected) == len(actual)
            and all(equal(left, right) for left, right in zip(expected, actual))
        )
    if isinstance(expected, bool) or expected is None:
        return type(expected) is type(actual) and expected == actual
    if isinstance(expected, (int, float)):
        return (
            type(actual) in (int, float)
            and math.isfinite(actual)
            and math.isclose(expected, actual, rel_tol=1e-9, abs_tol=1e-9)
        )
    return type(expected) is type(actual) and expected == actual


def semantic_match(spec, row, actual, file_root):
    expected = row["expected"]
    mode = spec["mode"]
    if mode == "duplicate":
        return type(actual) is int and row["arguments"][0].count(actual) >= 2
    if mode == "path":
        graph, start, end = row["arguments"]
        if expected is None:
            return actual is None
        return (
            isinstance(actual, list)
            and len(actual) == len(expected)
            and actual[0] == start
            and actual[-1] == end
            and all(type(vertex) is str and vertex in graph for vertex in actual)
            and all(right in graph[left] for left, right in pairwise(actual))
        )
    if mode == "set":
        return isinstance(actual, list) and sorted(expected) == sorted(actual)
    if mode == "temperature":
        if not isinstance(actual, list) or len(actual) != len(expected):
            return False
        counts = {}
        for method, arguments, left, right in zip(*row["arguments"], expected, actual):
            if method == "Insert":
                temperature = arguments[0]
                counts[temperature] = counts.get(temperature, 0) + 1
            if method == "GetMode" and counts:
                if type(right) is not int or counts.get(right, 0) != max(
                    counts.values()
                ):
                    return False
            elif not equal(left, right):
                return False
        return True
    if mode == "files":
        if not isinstance(actual, list):
            return False
        wanted = {frozenset(pair) for pair in expected}
        observed = set()
        modified = {entry["path"]: entry["modified"] for entry in row["arguments"][0]}
        for pair in actual:
            if (
                not isinstance(pair, list)
                or len(pair) != 2
                or not all(type(p) is str for p in pair)
            ):
                return False
            try:
                first, second = (
                    str(Path(p).resolve().relative_to(file_root)) for p in pair
                )
            except (ValueError, TypeError):
                return False
            key = frozenset((first, second))
            if len(key) != 2 or key not in wanted or key in observed:
                return False
            if modified[first] > modified[second]:
                return False
            observed.add(key)
        return observed == wanted
    return equal(expected, actual)


def run_fixture(spec, rows, code, root):
    root.mkdir()
    args = [row["arguments"] for row in rows]
    file_roots = [None] * len(rows)
    if spec["mode"] == "files":
        for index, row in enumerate(rows):
            directory = root / ("files-" + str(index))
            directory.mkdir()
            file_roots[index] = directory.resolve()
            for entry in row["arguments"][0]:
                target = directory / entry["path"]
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(
                    base64.b64decode(entry["base64"])
                    if "base64" in entry
                    else entry["content"].encode()
                )
                stamp = entry["modified"] * 1_000_000_000
                os.utime(target, ns=(stamp, stamp))
            args[index] = [str(directory.resolve())]
    header = (ROOT / "scripts/interviewcake/header_python.txt").read_text(
        encoding="utf-8"
    )
    harness = (ROOT / "interviewcake/runtime/harness.py").read_text(encoding="utf-8")
    values = {
        "ClassName": spec["className"],
        "Method": spec["method"],
        "Kinds": [param["type"] for param in spec["params"]],
        "Result": spec["result"],
        "Mode": spec["mode"],
    }
    config = "\n".join(key + " = " + repr(value) for key, value in values.items())
    (root / "solution.py").write_text(
        header + "\n" + code, encoding="utf-8", newline="\n"
    )
    (root / "harness.py").write_text(
        harness.replace("# CONFIGURATION", config), encoding="utf-8", newline="\n"
    )
    (root / "cases.json").write_text(json.dumps(args), encoding="utf-8", newline="\n")
    started = time.monotonic()
    try:
        execution = subprocess.run(
            [sys.executable, "harness.py"],
            cwd=root,
            text=True,
            capture_output=True,
            timeout=90,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return {
            "passed": 0,
            "total": len(rows),
            "processError": "Python adapter exceeded 90 seconds.",
        }
    if execution.returncode:
        return {
            "passed": 0,
            "total": len(rows),
            "processError": execution.stderr[-4000:],
        }
    results = json.loads((root / "results.json").read_text(encoding="utf-8"))
    if len(results) != len(rows):
        return {
            "passed": 0,
            "total": len(rows),
            "processError": "Incomplete case results.",
        }
    failures = []
    for index, (row, result) in enumerate(zip(rows, results)):
        if (
            result["Error"] is not None
            or result["ValidationFailed"]
            or not semantic_match(spec, row, result["Actual"], file_roots[index])
        ):
            failures.append(
                {
                    "case": index + 1,
                    "actual": result["Actual"],
                    "error": result["Error"],
                    "validationFailed": result["ValidationFailed"],
                }
            )
    return {
        "passed": len(rows) - len(failures),
        "total": len(rows),
        "seconds": time.monotonic() - started,
        "failures": failures[:6],
    }


def adapter_regressions(specs, algorithms, directory):
    """Catch output-type and identity loopholes beyond each algorithm mutation."""
    by_id = {spec["id"]: spec for spec in specs}
    graph = algorithms["interviewcake_graph-coloring"]["code"]
    path = algorithms["interviewcake_mesh-message"]["code"]
    cached_shuffle = """class Solution:
    def __init__(self):
        self._saved = None
    def Shuffle(self, array):
        if self._saved is not None:
            for index in range(len(array)):
                RandomSource.GetRandom(index, len(array) - 1)
            for index, value in enumerate(self._saved):
                array[index] = value
            return
        for index in range(len(array)):
            other = RandomSource.GetRandom(index, len(array) - 1)
            array[index], array[other] = array[other], array[index]
        self._saved = list(array)
"""
    checks = [
        (
            "integer-bool",
            "interviewcake_stock-price",
            "class Solution:\n    def GetMaxProfit(self, prices):\n        return True\n",
        ),
        (
            "integer-float",
            "interviewcake_stock-price",
            "class Solution:\n    def GetMaxProfit(self, prices):\n        return 6.0\n",
        ),
        (
            "nonserializable-integer",
            "interviewcake_stock-price",
            "class Solution:\n    def GetMaxProfit(self, prices):\n        return 10 ** 10000\n",
        ),
        (
            "graph-node-removal",
            "interviewcake_graph-coloring",
            "class Solution:\n    def ColorGraph(self, graph, colors):\n        graph.clear()\n",
        ),
        (
            "graph-edge-container-replacement",
            "interviewcake_graph-coloring",
            graph
            + "\n        for node in graph:\n            node.Neighbors = set(node.Neighbors)\n",
        ),
        (
            "map-neighbor-array-replacement",
            "interviewcake_mesh-message",
            path.replace(
                "        previous = {start: None}",
                "        for vertex in graph:\n            graph[vertex] = list(graph[vertex])\n        previous = {start: None}",
            ),
        ),
        (
            "word-count-floating-point",
            "interviewcake_word-cloud",
            algorithms["interviewcake_word-cloud"]["code"]
            + "\n        self.WordsToCounts = {word: float(count) for word, count in self.WordsToCounts.items()}\n",
        ),
        (
            "rand5-cached-despite-fresh-source",
            "interviewcake_simulate-5-sided-die",
            (
                "class Solution:\n"
                "    def __init__(self):\n        self._cached = None\n"
                "    def Rand5(self):\n"
                "        while True:\n"
                "            draw = RandomSource.Rand7()\n"
                "            if draw <= 5:\n"
                "                if self._cached is None:\n                    self._cached = draw\n"
                "                return self._cached\n"
            ),
        ),
        (
            "rand7-cached-despite-fresh-source",
            "interviewcake_simulate-7-sided-die",
            algorithms["interviewcake_simulate-7-sided-die"]["code"]
            .replace(
                "class Solution:\n",
                "class Solution:\n    def __init__(self):\n        self._cached = None\n\n",
            )
            .replace(
                "                return state % 7 + 1",
                "                if self._cached is None:\n                    self._cached = state % 7 + 1\n                return self._cached",
            ),
        ),
        (
            "rand5-uniform-marginals-correlated-sequence",
            "interviewcake_simulate-5-sided-die",
            (
                "class Solution:\n"
                "    def __init__(self):\n        self._previous = None\n"
                "    def Rand5(self):\n"
                "        while True:\n"
                "            draw = RandomSource.Rand7()\n"
                "            if draw <= 5:\n"
                "                self._previous = draw if self._previous is None else self._previous % 5 + 1\n"
                "                return self._previous\n"
            ),
        ),
        (
            "shuffle-cached-despite-fresh-source",
            "interviewcake_shuffle",
            cached_shuffle,
        ),
    ]
    results = []
    for name, problem_id, code in checks:
        rows = json.loads(
            (ROOT / ("interviewcake/cases/" + problem_id + ".json")).read_text(
                encoding="utf-8"
            )
        )
        result = run_fixture(
            by_id[problem_id], rows, code, directory / ("regression-" + name)
        )
        result.update(name=name, problemId=problem_id)
        result["accepted"] = (
            result["passed"] < result["total"] and "processError" not in result
        )
        results.append(result)
        print("adapter", name, "PASS" if result["accepted"] else "FAIL", flush=True)
    # Include length five even when the official examples happen to be smaller.
    # Empty/singleton inputs intentionally remain valid for a cached algorithm:
    # their only possible permutation cannot reveal this defect.
    distinct = [
        {"arguments": [list(range(size))], "expected": True} for size in range(2, 6)
    ]
    correct = run_fixture(
        by_id["interviewcake_shuffle"],
        distinct,
        algorithms["interviewcake_shuffle"]["code"],
        directory / "shuffle-distinct-correct",
    )
    cached = run_fixture(
        by_id["interviewcake_shuffle"],
        distinct,
        cached_shuffle,
        directory / "shuffle-distinct-cached",
    )
    result = {
        "name": "shuffle-distinct-lengths-two-through-five",
        "problemId": "interviewcake_shuffle",
        "correct": correct,
        "incorrect": cached,
        "accepted": correct["passed"] == 4
        and cached["passed"] == 0
        and "processError" not in correct
        and "processError" not in cached,
    }
    results.append(result)
    print(
        "adapter", result["name"], "PASS" if result["accepted"] else "FAIL", flush=True
    )
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--report", default=".epi-runs/interviewcake-python-author.json"
    )
    parser.add_argument("--ids", default="")
    options = parser.parse_args()
    chosen = set(options.ids.split(",")) if options.ids else None
    specs = json.loads(
        (ROOT / "scripts/interviewcake/interfaces.json").read_text(encoding="utf-8")
    )
    algorithms = json.loads(
        (ROOT / "scripts/interviewcake/algorithms_python.json").read_text(
            encoding="utf-8"
        )
    )
    if chosen is not None and not chosen <= {spec["id"] for spec in specs}:
        parser.error("--ids contains an unknown problem ID")
    results = []
    with tempfile.TemporaryDirectory(prefix="interviewcake-python-") as temporary:
        directory = Path(temporary)
        for spec in specs:
            if chosen is not None and spec["id"] not in chosen:
                continue
            rows = json.loads(
                (ROOT / ("interviewcake/cases/" + spec["id"] + ".json")).read_text(
                    encoding="utf-8"
                )
            )
            fixtures = algorithms[spec["id"]]
            result = {
                "problemId": spec["id"],
                "correct": run_fixture(
                    spec, rows, fixtures["code"], directory / (spec["id"] + "-correct")
                ),
            }
            result["incorrect"] = run_fixture(
                spec,
                rows,
                fixtures["incorrectCode"],
                directory / (spec["id"] + "-incorrect"),
            )
            result["starter"] = run_fixture(
                spec,
                rows,
                spec["interfaces"]["python"]["starter"],
                directory / (spec["id"] + "-starter"),
            )
            result["accepted"] = (
                result["correct"]["passed"] == len(rows)
                and result["incorrect"]["passed"] < len(rows)
                and "processError" not in result["incorrect"]
                and result["starter"]["passed"] < len(rows)
                and "processError" not in result["starter"]
            )
            results.append(result)
            print(
                spec["id"],
                "PASS" if result["accepted"] else "FAIL",
                "correct",
                str(result["correct"]["passed"]) + "/" + str(len(rows)),
                "wrong",
                str(result["incorrect"]["passed"]) + "/" + str(len(rows)),
                flush=True,
            )
        regressions = adapter_regressions(specs, algorithms, directory)
    report = ROOT / options.report
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(
        json.dumps(
            {
                "python": sys.version,
                "algorithmsSha256": hashlib.sha256(
                    (ROOT / "scripts/interviewcake/algorithms_python.json").read_bytes()
                ).hexdigest(),
                "runtimeSha256": hashlib.sha256(
                    (ROOT / "interviewcake/runtime/harness.py").read_bytes()
                ).hexdigest(),
                "results": results,
                "adapterRegressions": regressions,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return 0 if all(result["accepted"] for result in results + regressions) else 1


if __name__ == "__main__":
    raise SystemExit(main())
