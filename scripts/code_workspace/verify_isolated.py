"""Execute isolated callable envelopes through an unchanged real HTTP runner.

This focused smoke suite is additional evidence, not a replacement for the
complete 334-question/five-language acceptance matrix owned by SolutionsAudit.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
from pathlib import Path

from common import ROOT

sys.path.insert(0, str(ROOT / "scripts"))
from verify_blind75_http import Server, request

SMOKE_IDS = {
    "blind75_merge_k_sorted_lists",
    "interviewcake_stock-price",
    "blind75_subtree_of_another_tree",
    "blind75_serialize_and_deserialize_binary_tree",
    "interviewcake_reverse-linked-list",
    "interviewcake_graph-coloring",
    "interviewcake_temperature-tracker",
    "interviewcake_find-duplicate-files",
    "interviewcake_shuffle",
    "interviewcake_cake-thief",
}


def sha(code):
    return hashlib.sha256(code.encode("utf-8")).hexdigest()


def leading_import_solution(row):
    """Exercise user imports with an actual imported type in a correct algorithm."""
    imports = {
        "csharp": ("using System.Numerics;\n", "return (int)new BigInteger(best);"),
        "java": (
            "import java.math.BigInteger;\n",
            "return BigInteger.valueOf(best).intValueExact();",
        ),
    }
    directive, result = imports[row["language"]]
    assert row["solutionCode"].count("return best;") == 1
    return directive + row["solutionCode"].replace("return best;", result)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dll", type=Path, required=True)
    parser.add_argument("--part", type=Path, default=ROOT / "workspace-code/parts/isolated.json")
    parser.add_argument("--ids", help="Optional explicit comma-separated subset of the smoke IDs")
    parser.add_argument("--languages", help="Optional explicit comma-separated language subset")
    parser.add_argument(
        "--report", type=Path, default=ROOT / ".epi-runs/code-workspace-isolated-smoke.json"
    )
    parser.add_argument("--correct-only", action="store_true")
    parser.add_argument(
        "--leading-imports",
        action="store_true",
        help="Run correct Apple Stocks algorithms using leading System.Numerics/java.math imports",
    )
    options = parser.parse_args()
    ids = set(options.ids.split(",")) if options.ids else SMOKE_IDS
    if not ids <= SMOKE_IDS:
        raise ValueError("Unknown smoke ID")
    rows = json.loads(options.part.read_text(encoding="utf-8"))["entries"]
    languages = (
        set(options.languages.split(","))
        if options.languages
        else {"csharp", "javascript", "python", "cpp", "java"}
    )
    if not languages <= {"csharp", "javascript", "python", "cpp", "java"}:
        raise ValueError("Unknown smoke language")
    if options.leading_imports:
        ids = {"interviewcake_stock-price"}
        languages = {"csharp", "java"}
    selected = [row for row in rows if row["problemId"] in ids and row["language"] in languages]
    assert len(selected) == len(ids) * len(languages)
    artifacts = ROOT / ".epi-runs"
    artifacts.mkdir(parents=True, exist_ok=True)
    directory = Path(tempfile.mkdtemp(prefix="code-workspace-isolated-", dir=artifacts))
    report = {
        "partSha256": hashlib.sha256(options.part.read_bytes()).hexdigest(),
        "dllSha256": hashlib.sha256(options.dll.read_bytes()).hexdigest(),
        "executions": [],
        "failures": 0,
        "logDirectory": str(directory),
    }
    server = Server(options.dll.resolve(), directory)
    try:
        for row in selected:
            for variant in (
                ["solutionCode"]
                if options.correct_only or options.leading_imports
                else ["starterCode", "solutionCode"]
            ):
                visible = leading_import_solution(row) if options.leading_imports else row[variant]
                code = row["prefix"] + visible + row["suffix"]
                status, result, _ = request(
                    server.base,
                    "/api/submissions",
                    "POST",
                    {
                        "problemId": row["problemId"],
                        "language": row["language"],
                        "code": code,
                        "mode": "submit",
                    },
                )
                success = status == 200 and (
                    result.get("status") == "Accepted"
                    if variant == "solutionCode"
                    else result.get("status") in {"Accepted", "Wrong answer", "Runtime error"}
                )
                if not success:
                    report["failures"] += 1
                report["executions"].append(
                    {
                        "problemId": row["problemId"],
                        "language": row["language"],
                        "variant": "leadingImportsSolution" if options.leading_imports else variant,
                        "success": success,
                        "codeSha256": sha(code),
                        "visibleSha256": sha(visible),
                        "result": result,
                    }
                )
                print(
                    f"{'PASS' if success else 'FAIL'} {row['language']} {row['problemId']} {variant}: {result.get('status')} {result.get('passed')}/{result.get('total')}",
                    flush=True,
                )
                if not success:
                    print(json.dumps(result, indent=2), flush=True)
                options.report.parent.mkdir(parents=True, exist_ok=True)
                options.report.write_text(
                    json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n"
                )
    finally:
        server.close()
    print(
        f"Completed {len(report['executions'])} isolated smoke executions; {report['failures']} failures."
    )
    return 1 if report["failures"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
