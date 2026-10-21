"""Read-only solution API and real-browser checks against an isolated local profile.

This suite validates the displayed source and its integration, not algorithm
correctness. SolutionsAudit executes every displayed algorithm separately.
"""

import argparse
from contextlib import ExitStack
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import traceback
from urllib.parse import quote

from verify_blind75_http import Server, request

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = ["csharp", "javascript", "python", "cpp", "java"]
CHECKS = []


def check(condition, label):
    if not condition:
        raise AssertionError(label)
    CHECKS.append(label)
    print("PASS solutions HTTP " + label, flush=True)


def get(base, path):
    status, payload, _ = request(base, path)
    if status != 200:
        raise AssertionError(f"GET {path}: expected 200, received {status}: {payload}")
    return payload


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dll", type=Path, required=True)
    parser.add_argument("--browser", action="store_true")
    args = parser.parse_args()
    artifacts = ROOT / ".epi-runs"
    artifacts.mkdir(parents=True, exist_ok=True)
    directory = Path(tempfile.mkdtemp(prefix="solutions-http-", dir=artifacts))
    report = {
        "passed": False,
        "checks": CHECKS,
        "browserRequested": args.browser,
        "logDirectory": str(directory),
        "sourceSha256": sha(ROOT / "solutions/catalog.json"),
        "scriptSha256": sha(Path(__file__)),
        "algorithmExecution": "Separate SolutionsAudit required; not duplicated by this HTTP suite.",
    }
    try:
        entries = json.loads(
            (ROOT / "solutions/catalog.json").read_text(encoding="utf-8")
        )
        by_scope = {(entry["problemId"], entry["language"]): entry for entry in entries}
        check(
            len(entries) == len(by_scope) == 1670,
            "displayed inventory has 1670 unique question/language solutions",
        )
        with ExitStack() as stack:
            server = Server(args.dll.resolve(), directory)
            stack.callback(server.close)
            base = server.base
            problems = get(base, "/api/problems")
            check(len(problems) == 334, "API exposes all 334 coding questions")
            check(
                sum(p["collection"] == "epi" for p in problems) == 218,
                "all 218 EPI questions remain",
            )
            check(
                sum(p["collection"] == "blind75" for p in problems) == 75,
                "all 75 Blind questions remain",
            )
            check(
                sum(p["collection"] == "interviewcake" for p in problems) == 41,
                "all 41 Interview Cake coding tasks are runnable",
            )
            check(
                {key[0] for key in by_scope} == {p["id"] for p in problems},
                "every question has explicit displayed solutions",
            )
            check(
                all(
                    {key[1] for key in by_scope if key[0] == p["id"]} == set(LANGUAGES)
                    for p in problems
                ),
                "every question exposes all five solution languages",
            )
            before = get(base, "/api/practice/export")
            check(
                not before["drafts"] and not before["attempts"],
                "isolated profile starts without drafts or attempts",
            )
            displayed = []
            for problem in problems:
                problem_id = problem["id"]
                for language in LANGUAGES:
                    status, actual, headers = request(
                        base,
                        f"/api/problems/{quote(problem_id, safe='')}/solution?language={language}",
                    )
                    expected = by_scope[(problem_id, language)]
                    label = problem_id + "/" + language
                    check(
                        status == 200 and actual == expected,
                        label + " displays exact reviewed source and metadata",
                    )
                    check(
                        actual["problemId"] == problem_id
                        and actual["collection"] == problem["collection"]
                        and actual["language"] == language
                        and all(
                            isinstance(actual[key], str) and actual[key].strip()
                            for key in [
                                "code",
                                "explanation",
                                "timeComplexity",
                                "spaceComplexity",
                                "attribution",
                            ]
                        ),
                        label + " has complete language-specific solution content",
                    )
                    check(
                        headers.get("Content-Type", "").startswith("application/json"),
                        label + " has JSON media type",
                    )
                    if language == "csharp":
                        check(
                            all(
                                actual.get(key)
                                for key in ["correctness", "walkthrough", "edgeCases"]
                            ),
                            label
                            + " has detailed proof, original walkthrough and edge cases",
                        )
                    displayed.append(
                        {
                            "problemId": problem_id,
                            "language": language,
                            "collection": problem["collection"],
                            "codeSha256": hashlib.sha256(
                                actual["code"].encode()
                            ).hexdigest(),
                            "matched": True,
                        }
                    )
            report["solutions"] = displayed
            after = get(base, "/api/practice/export")
            check(
                before == after,
                "reading all 1670 solutions creates no drafts, attempts or progress",
            )
            for problem_id in [
                "not-a-question",
                "reading-parent-pointer-lca",
                "COUNT_BITS",
                "not-a-question';--",
            ]:
                check(
                    request(
                        base,
                        "/api/problems/" + quote(problem_id, safe="") + "/solution",
                    )[0]
                    == 404,
                    problem_id + " has explicit unavailable response",
                )
            check(
                request(base, "/api/problems/count_bits/solution", "POST", {})[0]
                == 404,
                "existing API catch-all rejects solution writes with 404",
            )
            for problem_id in [
                "count_bits",
                "blind75_two_sum",
                "interviewcake_stock-price",
            ]:
                for language in LANGUAGES:
                    status, _, _ = request(
                        base,
                        f"/api/practice/drafts/{problem_id}/{language}",
                        "PUT",
                        {
                            "code": "retained draft " + problem_id + " " + language,
                            "revision": 0,
                        },
                    )
                    check(
                        status == 200,
                        problem_id + "/" + language + " existing draft prepared",
                    )
            saved = get(base, "/api/practice/export")
            for problem_id in [
                "count_bits",
                "blind75_two_sum",
                "interviewcake_stock-price",
            ]:
                for language in LANGUAGES:
                    check(
                        get(
                            base,
                            f"/api/problems/{problem_id}/solution?language={language}",
                        )
                        == by_scope[(problem_id, language)],
                        problem_id
                        + "/"
                        + language
                        + " answer remains independent of saved drafts",
                    )
            check(
                saved == get(base, "/api/practice/export"),
                "solution reads preserve all fifteen saved language drafts exactly",
            )
            if args.browser:
                subprocess.run(
                    ["node", str(ROOT / "scripts/verify_solutions_browser.cjs"), base],
                    check=True,
                    cwd=ROOT,
                )
                browser = json.loads(
                    (artifacts / "solutions-browser.json").read_text(encoding="utf-8")
                )
                check(
                    browser["passed"] is True,
                    "real Chromium suite completed successfully",
                )
                report["browser"] = browser
            report["passed"] = True
    except Exception as error:
        report["error"] = str(error)
        report["traceback"] = traceback.format_exc()
        raise
    finally:
        (artifacts / "solutions-http.json").write_text(
            json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n"
        )
    print(
        f"PASS all {len(CHECKS)} solution HTTP checks; browser={args.browser}",
        flush=True,
    )


if __name__ == "__main__":
    main()
