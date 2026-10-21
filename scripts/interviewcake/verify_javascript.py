"""Run original JavaScript fixtures through the actual Interview Cake adapter.

This diagnostic uses the same runtime resource and independent semantic matcher
as other author checks. Final acceptance additionally uses SubmissionRunner.
"""

from __future__ import annotations

import argparse
import base64
import collections
import hashlib
import json
import math
import os
import subprocess
import tempfile
import time
from pathlib import Path

from interfaces import full_source
from verify_python import ROOT, semantic_match


def matches(spec, row, actual, file_root):
    if spec["mode"] != "temperature":
        return semantic_match(spec, row, actual, file_root)
    operations, arguments = row["arguments"]
    if not isinstance(actual, list) or len(actual) != len(operations):
        return False
    readings = []
    for operation, args, result in zip(operations, arguments, actual):
        if operation == "Insert":
            readings.append(args[0])
            if result is not None:
                return False
        elif not readings:
            if result is not None:
                return False
        elif operation == "GetMean":
            if (
                type(result) not in (int, float)
                or not math.isfinite(result)
                or not math.isclose(
                    result, sum(readings) / len(readings), rel_tol=1e-9, abs_tol=1e-9
                )
            ):
                return False
        elif operation == "GetMode":
            counts = collections.Counter(readings)
            if type(result) is not int or counts[result] != max(counts.values()):
                return False
        elif operation in ("GetMin", "GetMax"):
            if type(result) is not int or result != (
                min(readings) if operation == "GetMin" else max(readings)
            ):
                return False
        else:
            return False
    return True


def run_fixture(spec, rows, code, directory):
    directory.mkdir()
    arguments = [row["arguments"] for row in rows]
    file_roots = [None] * len(rows)
    if spec["mode"] == "files":
        for index, row in enumerate(rows):
            root = directory / ("files-" + str(index))
            root.mkdir()
            file_roots[index] = root.resolve()
            for entry in row["arguments"][0]:
                target = root / entry["path"]
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(
                    base64.b64decode(entry["base64"])
                    if "base64" in entry
                    else entry["content"].encode()
                )
                stamp = entry["modified"] * 1_000_000_000
                os.utime(target, ns=(stamp, stamp))
            arguments[index] = [str(root.resolve())]
    values = {
        "ClassName": spec["className"],
        "Method": spec["method"],
        "Kinds": [parameter["type"] for parameter in spec["params"]],
        "Result": spec["result"],
        "Mode": spec["mode"],
    }
    configuration = "\n".join(
        "const " + name + " = " + json.dumps(value) + ";"
        for name, value in values.items()
    )
    harness = (
        (ROOT / "interviewcake/runtime/harness.js")
        .read_text(encoding="utf-8")
        .replace("// CONFIGURATION", configuration)
    )
    (directory / "solution.js").write_text(
        full_source(spec, "javascript", code), encoding="utf-8", newline="\n"
    )
    (directory / "harness.js").write_text(harness, encoding="utf-8", newline="\n")
    (directory / "cases.json").write_text(
        json.dumps(arguments), encoding="utf-8", newline="\n"
    )
    started = time.monotonic()
    process = subprocess.run(
        ["node", "harness.js"],
        cwd=directory,
        text=True,
        capture_output=True,
        timeout=45,
        check=False,
    )
    if process.returncode:
        return {"passed": 0, "total": len(rows), "processError": process.stderr[-4000:]}
    results = json.loads((directory / "results.json").read_text(encoding="utf-8"))
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
            or not matches(spec, row, result["Actual"], file_roots[index])
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
        "codeSha256": hashlib.sha256(
            (directory / "solution.js").read_bytes()
        ).hexdigest(),
        "harnessSha256": hashlib.sha256(
            (directory / "harness.js").read_bytes()
        ).hexdigest(),
    }


def random_adversaries(spec, code):
    reference = code.replace("class Solution", "class Reference", 1)
    if spec["mode"] == "shuffle":
        cached = (
            reference
            + """
class Solution extends Reference {
    Shuffle(array) {
        if (this.saved === undefined) {
            super.Shuffle(array);
            this.saved = array.slice();
            return;
        }
        for (let i = array.length - 1; i > 0; i--) RandomSource.GetRandom(0, i);
        for (let i = 0; i < array.length; i++) array[i] = this.saved[i];
    }
}
"""
        )
        return [("cached-permutation", cached)]
    method, outcomes = spec["method"], 5 if spec["mode"] == "rand5" else 7
    cached = (
        reference
        + "\nclass Solution extends Reference {\n"
        + method
        + """() {
        const face = super."""
        + method
        + """();
        if (this.saved === undefined) this.saved = face;
        return this.saved;
    }}\n"""
    )
    cyclic = (
        reference
        + "\nclass Solution extends Reference {\n"
        + method
        + """() {
        const face = super."""
        + method
        + """();
        if (this.offset === undefined) { this.offset = face - 1; this.turn = 0; }
        const result = (this.offset + this.turn) % """
        + str(outcomes)
        + """ + 1;
        this.turn++;
        return result;
    }}\n"""
    )
    return [("cached", cached), ("correlated-cycle", cyclic)]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--report", default=".epi-runs/interviewcake-javascript-author.json"
    )
    parser.add_argument("--ids", default="")
    parser.add_argument("--include-starters", action="store_true")
    parser.add_argument("--random-adversaries", action="store_true")
    options = parser.parse_args()
    chosen = set(options.ids.split(",")) if options.ids else None
    specs = json.loads(
        (ROOT / "scripts/interviewcake/interfaces.json").read_text(encoding="utf-8")
    )
    algorithms = json.loads(
        (ROOT / "scripts/interviewcake/algorithms_javascript.json").read_text(
            encoding="utf-8"
        )
    )
    reports = []
    with tempfile.TemporaryDirectory(prefix="interviewcake-js-author-") as temporary:
        for spec in specs:
            if chosen is not None and spec["id"] not in chosen:
                continue
            if options.random_adversaries and spec["mode"] not in (
                "rand5",
                "rand7",
                "shuffle",
            ):
                continue
            rows = json.loads(
                (ROOT / "interviewcake/cases" / (spec["id"] + ".json")).read_text(
                    encoding="utf-8"
                )
            )
            entry = algorithms[spec["id"]]
            variants = (
                random_adversaries(spec, entry["code"])
                if options.random_adversaries
                else [
                    ("code", entry["code"]),
                    ("incorrectCode", entry["incorrectCode"]),
                ]
            )
            if options.include_starters and not options.random_adversaries:
                variants.append(
                    ("starter", spec["interfaces"]["javascript"]["starter"])
                )
            for variant, code in variants:
                result = run_fixture(
                    spec, rows, code, Path(temporary) / (spec["id"] + "-" + variant)
                )
                if variant == "starter":
                    success = "processError" not in result
                elif variant == "code":
                    success = result["passed"] == result["total"]
                else:
                    success = (
                        "processError" not in result
                        and result["passed"] < result["total"]
                    )
                report = {
                    "problemId": spec["id"],
                    "variant": variant,
                    "success": success,
                    **result,
                }
                reports.append(report)
                print(
                    ("PASS" if success else "FAIL"),
                    spec["id"],
                    variant,
                    str(result["passed"]) + "/" + str(result["total"]),
                    flush=True,
                )
                if not success:
                    print(json.dumps(report), flush=True)
    path = ROOT / options.report
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(reports, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    failures = sum(not report["success"] for report in reports)
    print(
        "Completed",
        len(reports),
        "fixture executions;",
        failures,
        "failures.",
        flush=True,
    )
    return int(failures != 0)


if __name__ == "__main__":
    raise SystemExit(main())
