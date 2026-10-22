"""Read-only solution API and real-browser checks against an isolated local profile.

This suite validates the displayed source and its integration, not algorithm
correctness. SolutionsAudit executes every displayed algorithm separately.
"""

import argparse
import hashlib
import json
import subprocess
import tempfile
import traceback
from contextlib import ExitStack
from pathlib import Path
from urllib.parse import quote

from verify_blind75_http import Server, request

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = ["csharp", "javascript", "python", "cpp", "java"]
RUNTIMES = {
    "csharp": "C# .NET 10",
    "javascript": "JavaScript Node.js 24",
    "python": "Python 3.14",
    "cpp": "C++17",
    "java": "Java 21",
}
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


def public_references(entry):
    # Provenance paths and source hashes are internal catalog evidence. The
    # public CodeReference contract consists of exactly these three fields.
    return [
        {key: reference[key] for key in ("title", "code", "names")}
        for reference in entry["references"]
    ]


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
        "callableSourceSha256": sha(ROOT / "workspace-code/catalog.json"),
        "scriptSha256": sha(Path(__file__)),
        "algorithmExecution": "Separate SolutionsAudit required; not duplicated by this HTTP suite.",
    }
    try:
        entries = json.loads(
            (ROOT / "solutions/catalog.json").read_text(encoding="utf-8")
        )
        callable_document = json.loads(
            (ROOT / "workspace-code/catalog.json").read_text(encoding="utf-8")
        )
        callable_entries = callable_document["entries"]
        callable_by_scope = {
            (entry["problemId"], entry["language"]): entry for entry in callable_entries
        }
        check(
            callable_document["codeFormat"] == "callable-v1"
            and len(callable_entries) == len(callable_by_scope) == 1670,
            "callable inventory has 1670 unique reviewed question/language pairs",
        )
        by_scope = {
            (entry["problemId"], entry["language"]): {
                **entry,
                "code": callable_by_scope[(entry["problemId"], entry["language"])][
                    "solutionCode"
                ],
                "codeFormat": "callable-v1",
                "references": public_references(
                    callable_by_scope[(entry["problemId"], entry["language"])]
                ),
            }
            for entry in entries
        }
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
                before["version"] == 2,
                "portable backups use version 2 for explicit code formats",
            )
            check(
                not before["drafts"] and not before["attempts"],
                "isolated profile starts without drafts or attempts",
            )
            contracts = json.loads(
                (ROOT / "scripts/clarity/contracts.json").read_text()
            )
            displayed = []
            for problem in problems:
                problem_id = problem["id"]
                for language in LANGUAGES:
                    source = callable_by_scope[(problem_id, language)]
                    expected_starter = {
                        "signature": source["signature"],
                        "starterCode": source["starterCode"],
                        "filename": source["filename"],
                        "runtime": RUNTIMES[language],
                        "codeFormat": "callable-v1",
                        "references": public_references(source),
                        "contract": contracts[problem_id][language],
                    }
                    check(
                        problem["starters"][language] == expected_starter,
                        problem_id
                        + "/"
                        + language
                        + " exposes the exact callable starter and required references",
                    )
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
                            "codeFormat": actual["codeFormat"],
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
                    expected_format = (
                        "callable-v1"
                        if problem_id == "interviewcake_stock-price"
                        else "legacy-v1"
                    )
                    draft = {
                        "code": "retained draft " + problem_id + " " + language,
                        "revision": 0,
                    }
                    if expected_format == "callable-v1":
                        draft["codeFormat"] = expected_format
                    status, saved_draft, _ = request(
                        base,
                        f"/api/practice/drafts/{problem_id}/{language}",
                        "PUT",
                        draft,
                    )
                    check(
                        status == 200,
                        problem_id + "/" + language + " existing draft prepared",
                    )
                    check(
                        saved_draft["codeFormat"] == expected_format
                        and saved_draft["code"] == draft["code"],
                        problem_id
                        + "/"
                        + language
                        + " preserves exact draft source and explicit or legacy-default format",
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
