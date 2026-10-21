"""Exercise every cleaned EPI Python solution through its original typed judge.

This is a fast integration smoke, not a substitute for the full five-language
acceptance matrix. It uses exactly the original comparator-capture and symbol
overlay contract implemented by SubmissionRunner.
"""

import argparse
import ast
import hashlib
import importlib.util
import json
import sys
import time
from pathlib import Path

from common import ROOT
from managed import problems


def run(limit: int) -> dict:
    sys.path.insert(0, str(ROOT / "epi_judge_python"))
    from test_framework.generic_test_handler import GenericTestHandler
    from test_framework.test_utils import split_tsv_file

    inventory = {p["Id"]: p for p in problems()}
    entries = json.loads(
        (ROOT / "workspace-code/parts/epi-managed.json").read_text(encoding="utf-8")
    )["entries"]
    rows = []
    for entry in entries:
        if entry["language"] != "python":
            continue
        problem = inventory[entry["problemId"]]
        reference_path = ROOT / "epi_judge_python" / problem["PySourceFile"]
        reference_spec = importlib.util.spec_from_file_location("ref_problem_mod", reference_path)
        reference = importlib.util.module_from_spec(reference_spec)
        reference_spec.loader.exec_module(reference)
        comparator = None
        for call in ast.walk(ast.parse(reference_path.read_text(encoding="utf-8"))):
            if not isinstance(call, ast.Call):
                continue
            called = (
                call.func.attr
                if isinstance(call.func, ast.Attribute)
                else call.func.id
                if isinstance(call.func, ast.Name)
                else ""
            )
            if called != "generic_test_main":
                continue
            expression = (
                call.args[3]
                if len(call.args) > 3
                else next((item.value for item in call.keywords if item.arg == "comparator"), None)
            )
            if expression is not None:
                comparator = eval(
                    compile(ast.Expression(expression), str(reference_path), "eval"),
                    reference.__dict__,
                )
            break
        code = entry["prefix"] + entry["solutionCode"] + entry["suffix"]
        namespace = {"__name__": "solution", "__file__": "solution.py"}
        # Integration tests execute trusted, checked-in bank algorithms only.
        exec(compile(code, "solution.py", "exec"), namespace)  # noqa: S102
        for name, value in namespace.items():
            if not name.startswith("_"):
                setattr(reference, name, value)
        target = getattr(reference, problem["PyInvocation"])
        corpus = split_tsv_file(str(ROOT / "test_data" / (problem["Id"] + ".tsv")))
        handler = GenericTestHandler(target, comparator)
        handler.parse_signature(corpus[0])
        cases = []
        for number, row in enumerate(corpus[1 : limit + 1], start=1):
            started = time.perf_counter()
            try:
                handler.run_test(15, lambda method, *arguments: method, row[:-1])
                cases.append({"case": number, "passed": True})
            # Record every fixture failure and fail the final report; do not
            # abandon the remaining question inventory after the first defect.
            except Exception as error:  # noqa: BLE001
                cases.append(
                    {
                        "case": number,
                        "passed": False,
                        "error": type(error).__name__ + ": " + str(error),
                    }
                )
            cases[-1]["elapsedSeconds"] = round(time.perf_counter() - started, 6)
        rows.append(
            {
                "problemId": problem["Id"],
                "language": "python",
                "programSha256": hashlib.sha256(code.encode("utf-8")).hexdigest(),
                "cases": cases,
                "passed": all(c["passed"] for c in cases),
            }
        )
    return {
        "scope": "All 218 EPI Python callable solutions, first corpus cases through original typed framework",
        "limitPerQuestion": limit,
        "questions": len(rows),
        "caseEvaluations": sum(len(r["cases"]) for r in rows),
        "failures": sum(not r["passed"] for r in rows),
        "results": rows,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument(
        "--report", type=Path, default=ROOT / ".epi-runs/managed-callable-smoke.json"
    )
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("limit must be positive")
    report = run(args.limit)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({key: value for key, value in report.items() if key != "results"}))
    for result in report["results"]:
        if not result["passed"]:
            print(json.dumps(result))
    raise SystemExit(bool(report["failures"]))
