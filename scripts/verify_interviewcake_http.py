"""Exercise the new collection through real HTTP with isolated practice profiles.

Intentional timeouts run in all five languages. This suite does not replace the
complete displayed-solution matrix or the 615 starter/positive/negative checks.
"""

import argparse
from contextlib import ExitStack
import hashlib
import json
from pathlib import Path
import tempfile
import sys
import traceback

from verify_blind75_http import Server, request

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts/interviewcake"))
from interfaces import full_source

LANGUAGES = ["csharp", "javascript", "python", "cpp", "java"]
EXTENSIONS = dict(csharp="cs", javascript="js", python="py", cpp="cpp", java="java")
CHECKS = []


def check(condition, label):
    if not condition:
        raise AssertionError(label)
    CHECKS.append(label)
    print("PASS Interview Cake HTTP " + label, flush=True)


def get(base, path):
    status, value, _ = request(base, path)
    check(status == 200, "GET " + path)
    return value


def submit(base, problem_id, language, code):
    status, result, _ = request(
        base,
        "/api/submissions",
        "POST",
        dict(problemId=problem_id, language=language, code=code, mode="submit"),
    )
    check(
        status == 200,
        problem_id + "/" + language + " execution returns a graded HTTP response",
    )
    return result


def source(problem_id, language):
    return (
        ROOT / "solutions" / language / (problem_id + "." + EXTENSIONS[language])
    ).read_text(encoding="utf-8")


def custom(language, variant):
    if variant == "syntax":
        return "this is deliberately invalid code !@#"
    if language == "csharp":
        body = (
            "while (true) {}"
            if variant == "timeout"
            else 'throw new System.InvalidOperationException("controlled runtime error");'
        )
        return (
            "public class Solution { public int GetMaxProfit(int[] prices) { "
            + body
            + " } }"
        )
    if language == "java":
        body = (
            "while (true) {}"
            if variant == "timeout"
            else 'throw new IllegalStateException("controlled runtime error");'
        )
        return (
            "class Solution { public int GetMaxProfit(int[] prices) { " + body + " } }"
        )
    if language == "cpp":
        body = (
            "for (;;) {}"
            if variant == "timeout"
            else 'throw std::runtime_error("controlled runtime error");'
        )
        return (
            "#include <vector>\n#include <stdexcept>\nclass Solution { public: int GetMaxProfit(std::vector<int>& prices) { "
            + body
            + " } };"
        )
    if language == "javascript":
        body = (
            "while (true) {}"
            if variant == "timeout"
            else 'throw Error("controlled runtime error");'
        )
        return (
            "class Solution { GetMaxProfit(prices) { "
            + body
            + " } }\nmodule.exports = {Solution};"
        )
    body = (
        "while True:\n            pass"
        if variant == "timeout"
        else 'raise RuntimeError("controlled runtime error")'
    )
    return (
        "class Solution:\n    def GetMaxProfit(self, prices):\n        " + body + "\n"
    )


def complete_custom(language, variant):
    return full_source({"className": "Solution"}, language, custom(language, variant))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dll", type=Path, required=True)
    args = parser.parse_args()
    artifacts = ROOT / ".epi-runs"
    artifacts.mkdir(parents=True, exist_ok=True)
    directory = Path(tempfile.mkdtemp(prefix="interviewcake-http-", dir=artifacts))
    catalog = json.loads(
        (ROOT / "interviewcake/catalog.json").read_text(encoding="utf-8")
    )
    report = dict(
        passed=False,
        checks=CHECKS,
        timeoutsSkipped=False,
        logDirectory=str(directory),
        scriptSha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        catalogSha256=hashlib.sha256(
            (ROOT / "interviewcake/catalog.json").read_bytes()
        ).hexdigest(),
    )
    stock = "interviewcake_stock-price"
    try:
        with ExitStack() as stack:
            server = Server(args.dll.resolve(), directory)
            stack.callback(server.close)
            base = server.base
            problems = get(base, "/api/problems")
            cake = [
                problem
                for problem in problems
                if problem["collection"] == "interviewcake"
            ]
            check(
                len(cake) == 41
                and [p["id"] for p in cake] == [p["id"] for p in catalog],
                "all 41 independently runnable tasks retain their exact stable ordering",
            )
            for problem in cake:
                check(
                    problem["testCount"] > 0
                    and set(problem["starters"]) == set(LANGUAGES),
                    problem["id"] + " has five executable APIs and a real corpus",
                )
                check(
                    problem["sourceUrl"].startswith(
                        "https://www.interviewcake.com/question/csharp/"
                    )
                    and "independently authored" in problem["sourceAttribution"],
                    problem["id"]
                    + " exposes factual attribution separately from local content",
                )
            for asset in (ROOT / "EpiJudge.Web/wwwroot/interviewcake/diagrams").glob(
                "*.svg"
            ):
                status, body, headers = request(
                    base, "/interviewcake/diagrams/" + asset.name
                )
                check(
                    status == 200
                    and body == asset.read_bytes()
                    and headers.get("Content-Type", "").startswith("image/svg+xml"),
                    asset.name + " is served locally byte-for-byte",
                )
            before = get(base, "/api/practice/export")
            for language in ["ruby", "", "CSharp", "js", "python;drop"]:
                check(
                    request(
                        base,
                        "/api/problems/" + stock + "/solution?language=" + language,
                    )[0]
                    == 400,
                    "unsupported solution language is rejected: " + repr(language),
                )
            check(
                get(base, "/api/problems/" + stock + "/solution")["language"]
                == "csharp",
                "omitted solution language defaults to CSharp",
            )
            check(
                before == get(base, "/api/practice/export"),
                "invalid and readonly solution requests change no storage",
            )
            accepted = []
            for language in LANGUAGES:
                result = submit(base, stock, language, source(stock, language))
                check(
                    result["status"] == "Accepted"
                    and result["passed"] == result["total"] == cake[1]["testCount"],
                    language + " actual stock algorithm passes its full HTTP corpus",
                )
                accepted.append((language, result["id"]))
                syntax = submit(
                    base, stock, language, complete_custom(language, "syntax")
                )
                check(
                    syntax["status"]
                    == (
                        "Runtime error"
                        if language in ("javascript", "python")
                        else "Compilation error"
                    ),
                    language + " syntax/compilation failures are graded safely",
                )
                runtime = submit(
                    base, stock, language, complete_custom(language, "runtime")
                )
                check(
                    runtime["status"] == "Runtime error" and runtime["passed"] == 0,
                    language + " thrown exceptions are isolated across cases",
                )
            malformed = submit(
                base,
                stock,
                "javascript",
                full_source(
                    {"className": "Solution"},
                    "javascript",
                    "class Solution { GetMaxProfit(prices) { return {unexpected:true}; } }",
                ),
            )
            check(
                malformed["status"] == "Wrong answer",
                "malformed result type is rejected without HTTP500",
            )
            oversized = submit(
                base,
                stock,
                "javascript",
                full_source(
                    {"className": "Solution"},
                    "javascript",
                    'class Solution { GetMaxProfit(prices) { return "x".repeat(900000); } }',
                ),
            )
            check(
                oversized["status"] == "Output limit exceeded",
                "oversized file-based judge output is bounded",
            )
            for language in LANGUAGES:
                result = submit(
                    base, stock, language, complete_custom(language, "timeout")
                )
                check(
                    result["status"] == "Time limit exceeded",
                    language + " genuine infinite loop reaches its execution limit",
                )
                recovery = submit(
                    base, stock, "javascript", source(stock, "javascript")
                )
                check(
                    recovery["status"] == "Accepted",
                    language + " timed-out runner releases the gate and recovers",
                )
            for language, attempt_id in accepted:
                history = get(base, "/api/practice/history/" + attempt_id)
                check(
                    history["problemId"] == stock
                    and history["language"] == language
                    and history["code"] == source(stock, language),
                    language + " history retains exact submitted source",
                )
            backup = get(base, "/api/practice/export")
            restored_directory = directory / "restored"
            restored_directory.mkdir()
            restored = Server(args.dll.resolve(), restored_directory)
            stack.callback(restored.close)
            for _ in range(2):
                status, _, _ = request(
                    restored.base, "/api/practice/import", "POST", backup
                )
                check(status == 200, "Interview Cake backup imports idempotently")
            restored_backup = get(restored.base, "/api/practice/export")
            check(
                len(restored_backup["attempts"]) == len(backup["attempts"]),
                "restoration retains all accepted and failed Interview Cake attempts without duplicates",
            )
            for language, attempt_id in accepted:
                history = get(restored.base, "/api/practice/history/" + attempt_id)
                check(
                    history["code"] == source(stock, language),
                    language + " restored history preserves source bytes",
                )
            report["passed"] = True
    except Exception as error:
        report["error"] = str(error)
        report["traceback"] = traceback.format_exc()
        raise
    finally:
        (artifacts / "interviewcake-http.json").write_text(
            json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n"
        )
    print(
        f"PASS all {len(CHECKS)} Interview Cake HTTP checks; all five timeouts executed",
        flush=True,
    )


if __name__ == "__main__":
    main()
