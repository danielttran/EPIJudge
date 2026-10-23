"""Real local HTTP checks for the registered CtCI snapshot and submission route."""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from verify_blind75_http import Server, create_run_directory, request


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dll", type=Path, required=True)
    parser.add_argument("--browser", action="store_true")
    args = parser.parse_args()
    directory = create_run_directory(ROOT)
    server = Server(args.dll.resolve(), directory)
    checks = []

    def check(condition, label):
        if not condition:
            raise AssertionError(label)
        checks.append(label)
        print("PASS CtCI HTTP " + label, flush=True)

    try:
        status, problems, _ = request(server.base, "/api/problems")
        check(status == 200, "catalog available")
        expected = json.loads((ROOT / "ctci6/catalog.json").read_text())
        ctci = [p for p in problems if p["collection"] == "ctci6"]
        check(
            [p["id"] for p in ctci] == [p["id"] for p in expected],
            "all and only exported coding references registered in order",
        )
        check(
            all(len(p["starters"]) == 5 for p in ctci),
            "five starters per registered problem",
        )
        check(
            all(
                "invocation" not in p and "harness" not in str(p["starters"].keys())
                for p in ctci
            ),
            "internal judge configuration omitted",
        )
        draft = "// original draft remains intact Ω"
        status, saved, _ = request(
            server.base,
            "/api/practice/drafts/count_bits/csharp",
            "PUT",
            dict(code=draft, revision=0, codeFormat="callable-v1"),
        )
        check(status == 200, "original-bank draft saved in isolated profile")
        selected = [
            ("ctci6_3_6", "csharp"),
            ("ctci6_8_8", "javascript"),
            ("ctci6_2_7", "python"),
            ("ctci6_5_8", "cpp"),
            ("ctci6_8_11", "java"),
        ]
        for problem_id, language in selected:
            problem = next(p for p in ctci if p["id"] == problem_id)
            status, solution, _ = request(
                server.base,
                "/api/problems/" + problem_id + "/solution?language=" + language,
            )
            check(
                status == 200 and solution["language"] == language,
                problem_id + "/" + language + " solution available",
            )
            for variant, code in [
                ("correct", solution["code"]),
                ("starter", problem["starters"][language]["starterCode"]),
            ]:
                status, result, _ = request(
                    server.base,
                    "/api/submissions",
                    "POST",
                    dict(
                        problemId=problem_id,
                        language=language,
                        code=code,
                        mode="submit",
                        codeFormat="callable-v1",
                    ),
                )
                check(
                    status == 200,
                    problem_id
                    + "/"
                    + language
                    + "/"
                    + variant
                    + " reaches normal submission service",
                )
                check(
                    result["total"] == problem["testCount"],
                    problem_id + "/" + variant + " full declared corpus used",
                )
                check(
                    result["status"]
                    == ("Accepted" if variant == "correct" else "Wrong answer"),
                    problem_id + "/" + variant + " correct outcome",
                )
                check(
                    all(
                        c["hidden"]
                        and c["input"] is None
                        and c["expected"] is None
                        and c["actual"] is None
                        for c in result["cases"]
                    ),
                    problem_id + "/" + variant + " hidden cases remain hidden",
                )
        status, state, _ = request(server.base, "/api/practice")
        check(
            status == 200 and saved in state["drafts"],
            "original draft remains byte-for-byte unchanged after new-collection submissions",
        )
        if args.browser:
            import subprocess

            subprocess.run(
                [
                    "node",
                    str(ROOT / "scripts/verify_solution_language_browser.cjs"),
                    server.base,
                    "ctci6_3_6",
                ],
                cwd=ROOT,
                check=True,
                timeout=360,
            )
        report = dict(
            passed=True,
            checks=checks,
            questions=len(ctci),
            submissionExecutions=len(selected) * 2,
            isolatedDirectory=str(directory),
        )
        (ROOT / ".epi-runs/ctci6-http.json").write_text(
            json.dumps(report, indent=2) + "\n"
        )
    finally:
        server.close()
    print(
        json.dumps(
            dict(
                passed=True,
                checks=len(checks),
                questions=len(ctci),
                submissionExecutions=len(selected) * 2,
            )
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
