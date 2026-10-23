"""Real HTTP acceptance for every clean starter and displayed solution.

Algorithm-matrix acceptance is separate. This checks all 3,340 API payloads,
actual callable/legacy submissions, diagnostics, timeouts and durable format
metadata using temporary local profiles only.
"""

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import threading
import time
import traceback
from contextlib import ExitStack
from pathlib import Path
from urllib.parse import quote

from common import ROOT

sys.path.insert(0, str(ROOT / "scripts"))
from verify_blind75_http import Server, request

LANGUAGES = ["csharp", "javascript", "python", "cpp", "java"]
SUBJECTS = {
    "simple": "interviewcake_stock-price",
    "tree": "interviewcake_balanced-binary-tree",
    "list": "interviewcake_delete-node",
    "graph": "interviewcake_graph-coloring",
    "stateful": "interviewcake_temperature-tracker",
}


def hash_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def has_editor_line(diagnostic, filename, line):
    number = str(line)
    pattern = (
        re.escape(filename)
        + r"(?::"
        + number
        + r"(?!\d)|\("
        + number
        + r',|", line '
        + number
        + r"(?!\d))"
    )
    return re.search(pattern, diagnostic) is not None


def import_fixtures(entries):
    """Actual algorithms requiring leading imports, plus exact-line failures."""
    apple = SUBJECTS["simple"]
    return [
        {
            "label": "Python future import and UTF-8 Unicode",
            "problemId": apple,
            "language": "python",
            "code": "from __future__ import annotations\n# UTF-8: Δ Ω 漢字\n"
            + entries[(apple, "python")]["solutionCode"],
            "invalid": "from __future__ import annotations\n# UTF-8: Δ Ω 漢字\ndef broken(:\n",
            "errorLine": 3,
        },
        {
            "label": "CSharp leading System.Numerics import",
            "problemId": apple,
            "language": "csharp",
            "code": """using System.Numerics;
public class Solution
{
    public int GetMaxProfit(int[] prices)
    {
        if (prices.Length < 2) throw new ArgumentException();
        BigInteger minimum = prices[0];
        BigInteger best = (BigInteger)prices[1] - minimum;
        for (int i = 1; i < prices.Length; ++i)
        {
            best = BigInteger.Max(best, (BigInteger)prices[i] - minimum);
            minimum = BigInteger.Min(minimum, prices[i]);
        }
        return (int)best;
    }
}
""",
            "invalid": """using System.Numerics;
// User source Δ
public class Solution
{
    public int GetMaxProfit(int[] prices)
    {
        return unknownName;
    }
}
""",
            "errorLine": 7,
        },
        {
            "label": "Java InterviewCake leading BigInteger import",
            "problemId": apple,
            "language": "java",
            "code": """import java.math.BigInteger;
// User comment with ; and Unicode Δ
class Solution {
    public int GetMaxProfit(int[] prices) {
        if (prices.length < 2) throw new IllegalArgumentException();
        BigInteger minimum = BigInteger.valueOf(prices[0]);
        BigInteger best = BigInteger.valueOf(prices[1]).subtract(minimum);
        for (int i = 1; i < prices.length; ++i) {
            BigInteger value = BigInteger.valueOf(prices[i]);
            best = best.max(value.subtract(minimum));
            minimum = minimum.min(value);
        }
        return best.intValueExact();
    }
}
""",
            "invalid": """import java.math.BigInteger;
// User comment with ; and Unicode Δ
class Solution {
    public int GetMaxProfit(int[] prices) {
        return unknownName;
    }
}
""",
            "errorLine": 5,
        },
        {
            "label": "JavaScript local fs and path bindings",
            "problemId": apple,
            "language": "javascript",
            "code": """const fs = require("node:fs");
const path = require("node:path");
class Solution {
    GetMaxProfit(prices) {
        if (typeof fs.readFileSync !== "function" || path.basename("/practice/prices") !== "prices") {
            throw new Error("Expected standard Node modules");
        }
        if (prices.length < 2) throw new Error("Need two prices");
        let minimum = prices[0];
        let best = prices[1] - minimum;
        for (let i = 1; i < prices.length; ++i) {
            best = Math.max(best, prices[i] - minimum);
            minimum = Math.min(minimum, prices[i]);
        }
        return best;
    }
}
""",
            "invalid": """const fs = require("node:fs");
const path = require("node:path");
// User comment Δ
class Solution {
    GetMaxProfit(prices) {
        const = ;
    }
}
""",
            "errorLine": 6,
        },
        {
            "label": "Java EPI leading import with semicolons in comments",
            "problemId": "count_bits",
            "language": "java",
            "code": """/* This ; and import not.real.Type; are only comment text. */
import java.util.Objects; // another ; comment
// UTF-8 user comment Δ ;
public static short countBits(int x) {
    Objects.requireNonNull(Integer.valueOf(x));
    short count = 0;
    while (x != 0) {
        count += (x & 1);
        x >>>= 1;
    }
    return count;
}
""",
            "invalid": """/* This ; is only a comment. */
import java.util.Objects; // ; ignored
// User comment Δ ;
public static short countBits(int x) {
    return unknownName;
}
""",
            "errorLine": 5,
        },
    ]


def api(base, path, method="GET", body=None, expected_status=200):
    status, data, headers = request(base, path, method, body)
    if status != expected_status:
        raise AssertionError(
            f"{method} {path}: {status}, expected {expected_status}: {data}"
        )
    return data, headers


def fail_source(language, failure):
    """Independent, deliberately broken callable programs for one known API."""
    body = {
        "csharp": {
            "runtime": 'throw new InvalidOperationException("callable fixture");',
            "timeout": "while (true) { }",
        },
        "cpp": {
            "runtime": 'throw std::runtime_error("callable fixture");',
            "timeout": "while (true) { }",
        },
        "java": {
            "runtime": 'throw new IllegalStateException("callable fixture");',
            "timeout": "while (true) { }",
        },
        "javascript": {
            "runtime": 'throw new Error("callable fixture");',
            "timeout": "while (true) { }",
        },
        "python": {
            "runtime": 'raise RuntimeError("callable fixture")',
            "timeout": "while True:\n            pass",
        },
    }[language][failure]
    if language == "csharp":
        return (
            "public class Solution\n{\n    public int GetMaxProfit(int[] prices)\n    {\n        "
            + body
            + "\n    }\n}\n"
        )
    if language == "cpp":
        return (
            "class Solution {\npublic:\n    int GetMaxProfit(std::vector<int>& prices) {\n        "
            + body
            + "\n    }\n};\n"
        )
    if language == "java":
        return (
            "class Solution {\n    public int GetMaxProfit(int[] prices) {\n        "
            + body
            + "\n    }\n}\n"
        )
    if language == "javascript":
        return (
            "class Solution {\n    GetMaxProfit(prices) {\n        "
            + body
            + "\n    }\n}\n"
        )
    return (
        "class Solution:\n    def GetMaxProfit(self, prices: list[int]) -> int:\n        "
        + body
        + "\n"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dll", type=Path, required=True)
    parser.add_argument("--browser", action="store_true")
    parser.add_argument("--no-timeouts", action="store_true")
    args = parser.parse_args()
    artifact_root = ROOT / ".epi-runs"
    artifact_root.mkdir(parents=True, exist_ok=True)
    directory = Path(tempfile.mkdtemp(prefix="callable-http-", dir=artifact_root))
    checks = []
    report = {
        "passed": False,
        "checks": checks,
        "codeFormat": "callable-v1",
        "logDirectory": str(directory),
        "catalogSha256": hash_text(
            (ROOT / "workspace-code/catalog.json").read_text(encoding="utf-8")
        ),
        "scriptSha256": hash_text(Path(__file__).read_text(encoding="utf-8")),
        "dllSha256": hashlib.sha256(args.dll.read_bytes()).hexdigest(),
        "clientIndexSha256": hashlib.sha256(
            (ROOT / "epijudge.client/dist/index.html").read_bytes()
        ).hexdigest(),
        "browserRequested": args.browser,
        "timeoutsSkipped": args.no_timeouts,
        "algorithmMatrix": "Separate complete SolutionsAudit callable runs are required.",
        "artifacts": [],
        "executions": [],
    }

    def check(condition, label):
        if not condition:
            raise AssertionError(label)
        checks.append(label)

    def submit(
        base, problem_id, language, code, mode="submit", code_format="callable-v1"
    ):
        body = {
            "problemId": problem_id,
            "language": language,
            "code": code,
            "mode": mode,
        }
        if code_format is not None:
            body["codeFormat"] = code_format
        result, _ = api(base, "/api/submissions", "POST", body)
        return result

    try:
        document = json.loads(
            (ROOT / "workspace-code/catalog.json").read_text(encoding="utf-8")
        )
        manifest = json.loads((ROOT / "solutions/coverage.json").read_text())
        expected_questions = manifest["questionCount"]
        expected_pairs = expected_questions * len(LANGUAGES)
        entries = document["entries"]
        by_scope = {(entry["problemId"], entry["language"]): entry for entry in entries}
        check(
            document["codeFormat"] == "callable-v1"
            and len(entries) == len(by_scope) == expected_pairs,
            f"catalog enumerates all {expected_pairs} callable contracts",
        )
        with ExitStack() as stack:
            server = Server(args.dll.resolve(), directory)
            stack.callback(server.close)
            base = server.base
            problems, _ = api(base, "/api/problems")
            check(
                len(problems) == expected_questions,
                f"all {expected_questions} runnable questions remain",
            )
            check(
                {
                    collection: sum(p["collection"] == collection for p in problems)
                    for collection in ["epi", "blind75", "interviewcake"]
                }
                == {"epi": 218, "blind75": 75, "interviewcake": 41},
                "exact EPI/Blind75/InterviewCake collection counts",
            )
            check(
                {p["id"] for p in problems} == {scope[0] for scope in by_scope},
                "callable contract IDs exactly match the live bank",
            )
            before, _ = api(base, "/api/practice/export")
            for problem in problems:
                check(
                    set(problem["starters"]) == set(LANGUAGES),
                    problem["id"] + " exposes five starters",
                )
                for language in LANGUAGES:
                    expected = by_scope[(problem["id"], language)]
                    public_references = [
                        {key: reference[key] for key in ["title", "code", "names"]}
                        for reference in expected["references"]
                    ]
                    starter = problem["starters"][language]
                    scope = problem["id"] + "/" + language
                    check(
                        starter["starterCode"] == expected["starterCode"],
                        scope + " starter source matches reviewed callable code",
                    )
                    check(
                        starter["codeFormat"] == "callable-v1"
                        and starter["references"] == public_references,
                        scope + " starter format and required references match",
                    )
                    check(
                        starter["signature"] == expected["signature"]
                        and starter["filename"] == expected["filename"],
                        scope + " starter API and filename match",
                    )
                    solution, headers = api(
                        base,
                        f"/api/problems/{quote(problem['id'], safe='')}/solution?language={language}",
                    )
                    check(
                        solution["code"] == expected["solutionCode"],
                        scope + " solution source matches reviewed callable code",
                    )
                    check(
                        solution["codeFormat"] == "callable-v1"
                        and solution["references"] == public_references,
                        scope + " solution format and required references match",
                    )
                    check(
                        solution["problemId"] == problem["id"]
                        and solution["language"] == language
                        and solution["collection"] == problem["collection"],
                        scope + " solution identity is exact",
                    )
                    check(
                        headers.get("Content-Type", "").startswith("application/json"),
                        scope + " solution has JSON content type",
                    )
                    check(
                        all(
                            isinstance(solution.get(key), str) and solution[key].strip()
                            for key in [
                                "explanation",
                                "timeComplexity",
                                "spaceComplexity",
                                "attribution",
                            ]
                        ),
                        scope + " explanation and attribution remain complete",
                    )
                    if language == "csharp":
                        check(
                            all(
                                solution.get(key)
                                for key in ["correctness", "walkthrough", "edgeCases"]
                            ),
                            scope + " detailed C# explanation is retained",
                        )
                    for role, code in [
                        ("starter", starter["starterCode"]),
                        ("solution", solution["code"]),
                    ]:
                        report["artifacts"].append(
                            {
                                "problemId": problem["id"],
                                "language": language,
                                "role": role,
                                "codeSha256": hash_text(code),
                                "matched": True,
                            }
                        )
            check(
                len(report["artifacts"]) == expected_pairs * 2,
                f"all {expected_pairs * 2} visible code payloads checked without sampling",
            )
            after, _ = api(base, "/api/practice/export")
            check(
                before == after,
                "reading all clean starters and solutions does not write drafts or history",
            )
            print(
                f"PASS callable HTTP all {expected_pairs * 2} visible source payloads",
                flush=True,
            )

            for language in LANGUAGES:
                language_catalog, _ = api(base, "/api/problems?lang=" + language)
                check(
                    len(language_catalog) == expected_questions,
                    language + " legacy language query remains supported",
                )
                check(
                    all(
                        p["starterCode"] == by_scope[(p["id"], language)]["starterCode"]
                        for p in language_catalog
                    ),
                    language
                    + " top-level selected-language starters also use clean source",
                )

            valid = {
                "problemId": SUBJECTS["simple"],
                "language": "javascript",
                "mode": "run",
                "code": by_scope[(SUBJECTS["simple"], "javascript")]["solutionCode"],
                "codeFormat": "callable-v1",
            }
            for invalid_format in ["unknown", "", "CALLABLE-V1", 42]:
                body = dict(valid, codeFormat=invalid_format)
                status, _, _ = request(base, "/api/submissions", "POST", body)
                check(
                    status == 400,
                    "invalid submission format is rejected: " + repr(invalid_format),
                )
            for invalid_format in ["future", "", None]:
                status, _, _ = request(
                    base,
                    "/api/practice/drafts/count_bits/python",
                    "PUT",
                    {
                        "code": "# unchanged",
                        "revision": 0,
                        "codeFormat": invalid_format,
                    },
                )
                check(
                    status == 400,
                    "invalid draft format is rejected: " + repr(invalid_format),
                )

            for category, problem_id in SUBJECTS.items():
                for language in LANGUAGES:
                    code = by_scope[(problem_id, language)]["solutionCode"]
                    result = submit(base, problem_id, language, code)
                    problem = next(p for p in problems if p["id"] == problem_id)
                    check(
                        result["status"] == "Accepted"
                        and result["passed"] == result["total"] == problem["testCount"],
                        f"actual {category} callable solution accepted through HTTP: {language}",
                    )
                    snapshot, _ = api(base, "/api/practice/history/" + result["id"])
                    check(
                        snapshot["code"] == code
                        and snapshot["codeFormat"] == "callable-v1",
                        f"{category}/{language} history stores the original clean code and format",
                    )
                    report["executions"].append(
                        {
                            "category": category,
                            "problemId": problem_id,
                            "language": language,
                            "codeFormat": "callable-v1",
                            "codeSha256": hash_text(code),
                            "result": result,
                        }
                    )
                print(
                    "PASS callable HTTP actual "
                    + category
                    + " solutions in five languages",
                    flush=True,
                )

            for problem_id, language in [
                ("count_bits", "python"),
                ("blind75_two_sum", "javascript"),
            ]:
                result = submit(
                    base,
                    problem_id,
                    language,
                    by_scope[(problem_id, language)]["solutionCode"],
                )
                check(
                    result["status"] == "Accepted",
                    problem_id + " callable route preserves its collection adapter",
                )

            for language in LANGUAGES:
                extension = {
                    "csharp": "cs",
                    "javascript": "js",
                    "python": "py",
                    "cpp": "cpp",
                    "java": "java",
                }[language]
                full_code = (
                    ROOT
                    / "solutions"
                    / language
                    / (SUBJECTS["simple"] + "." + extension)
                ).read_text(encoding="utf-8")
                for code_format in [None, "legacy-v1"]:
                    result = submit(
                        base,
                        SUBJECTS["simple"],
                        language,
                        full_code,
                        code_format=code_format,
                    )
                    check(
                        result["status"] == "Accepted",
                        language
                        + " legacy full program still executes without duplicate type injection",
                    )
                    saved, _ = api(base, "/api/practice/history/" + result["id"])
                    check(
                        saved["code"] == full_code
                        and saved["codeFormat"] == "legacy-v1",
                        language + " legacy submission snapshot is byte-preserved",
                    )

            syntax = {
                "csharp": "THIS IS INVALID !!!\n",
                "cpp": "THIS IS INVALID !!!\n",
                "java": "THIS IS INVALID !!!\n",
                "javascript": "const = !!!;\n",
                "python": "def broken(:\n",
            }
            for language in LANGUAGES:
                result = submit(
                    base, SUBJECTS["simple"], language, syntax[language], mode="run"
                )
                expected_status = (
                    "Runtime error"
                    if language in ["javascript", "python"]
                    else "Compilation error"
                )
                check(
                    result["status"] == expected_status,
                    language + " callable syntax failure is reported",
                )
                report.setdefault("diagnostics", []).append(
                    {"language": language, "result": result}
                )
                diagnostic = result.get("diagnostics") or ""
                filename = by_scope[(SUBJECTS["simple"], language)]["filename"]
                check(
                    has_editor_line(diagnostic, filename, 1),
                    language + " syntax diagnostic points to editor line 1",
                )
                runtime = submit(
                    base,
                    SUBJECTS["simple"],
                    language,
                    fail_source(language, "runtime"),
                    mode="run",
                )
                check(
                    runtime["status"] == "Runtime error",
                    language + " callable runtime failure is reported",
                )
                filename = by_scope[(SUBJECTS["simple"], language)]["filename"]
                marker = filename + ":" + "9" * 80
                oversized_source = fail_source(language, "runtime").replace(
                    '"callable fixture"', json.dumps(marker)
                )
                oversized = submit(
                    base, SUBJECTS["simple"], language, oversized_source, mode="run"
                )
                report.setdefault("oversizedDiagnostics", []).append(
                    {"language": language, "marker": marker, "result": oversized}
                )
                check(
                    oversized["status"] == "Runtime error"
                    and any(
                        marker in (case.get("error") or "")
                        for case in oversized["cases"]
                    ),
                    language
                    + " oversized diagnostic line is preserved without mapper overflow",
                )

            for fixture in import_fixtures(by_scope):
                problem_id, language = fixture["problemId"], fixture["language"]
                result = submit(base, problem_id, language, fixture["code"])
                problem = next(p for p in problems if p["id"] == problem_id)
                snapshot, _ = api(base, "/api/practice/history/" + result["id"])
                check(
                    result["status"] == "Accepted"
                    and result["passed"] == result["total"] == problem["testCount"],
                    fixture["label"] + " accepts the complete question corpus",
                )
                check(
                    snapshot["code"] == fixture["code"]
                    and snapshot["codeFormat"] == "callable-v1",
                    fixture["label"] + " preserves the original user source snapshot",
                )
                invalid = submit(
                    base, problem_id, language, fixture["invalid"], mode="run"
                )
                filename = by_scope[(problem_id, language)]["filename"]
                report.setdefault("leadingImports", []).append(
                    {
                        "label": fixture["label"],
                        "problemId": problem_id,
                        "language": language,
                        "codeSha256": hash_text(fixture["code"]),
                        "expectedErrorLine": fixture["errorLine"],
                        "result": result,
                        "invalidResult": invalid,
                    }
                )
                check(
                    invalid["status"]
                    == (
                        "Runtime error"
                        if language in ["python", "javascript"]
                        else "Compilation error"
                    )
                    and has_editor_line(
                        invalid.get("diagnostics") or "", filename, fixture["errorLine"]
                    ),
                    fixture["label"]
                    + " reports the original editor line after imports",
                )
            print(
                "PASS callable HTTP leading imports, Unicode and original diagnostic lines",
                flush=True,
            )

            if not args.no_timeouts:
                for language in LANGUAGES:
                    responses = []
                    worker = threading.Thread(
                        target=lambda lang=language, results=responses: results.append(
                            submit(
                                base,
                                SUBJECTS["simple"],
                                lang,
                                fail_source(lang, "timeout"),
                                mode="run",
                            )
                        )
                    )
                    worker.start()
                    active = False
                    for _ in range(150):
                        history, _ = api(
                            base,
                            "/api/practice/history?problemId=" + SUBJECTS["simple"],
                        )
                        if any(row["status"] == "Running" for row in history):
                            active = True
                            break
                        time.sleep(0.1)
                    check(
                        active,
                        language
                        + " callable timeout source is durably recorded before completion",
                    )
                    status, _, _ = request(base, "/api/submissions", "POST", valid)
                    check(
                        status == 429,
                        language + " callable timeout preserves runner busy response",
                    )
                    worker.join(145)
                    check(
                        not worker.is_alive()
                        and responses
                        and responses[0]["status"] == "Time limit exceeded",
                        language + " actual callable timeout is enforced",
                    )
                    report.setdefault("timeouts", []).append(
                        {"language": language, "result": responses[0]}
                    )
                    check(
                        submit(
                            base,
                            SUBJECTS["simple"],
                            "javascript",
                            valid["code"],
                            mode="run",
                        )["status"]
                        == "Accepted",
                        language + " callable runner recovers after timeout",
                    )
                    print("PASS callable HTTP actual timeout " + language, flush=True)

            legacy_text = "// exact old draft Ω\r\nmodule.exports = {};\r\n"
            legacy_draft, _ = api(
                base,
                "/api/practice/drafts/count_bits/javascript",
                "PUT",
                {"code": legacy_text, "revision": 0},
            )
            check(
                legacy_draft["code"] == legacy_text
                and legacy_draft["codeFormat"] == "legacy-v1",
                "omitted draft format preserves old CRLF/Unicode source as legacy",
            )
            clean = by_scope[("count_bits", "python")]["starterCode"]
            new_draft, _ = api(
                base,
                "/api/practice/drafts/count_bits/python",
                "PUT",
                {"code": clean, "revision": 0, "codeFormat": "callable-v1"},
            )
            check(
                new_draft["code"] == clean and new_draft["codeFormat"] == "callable-v1",
                "new draft stores callable format explicitly",
            )
            changed, _ = api(
                base,
                "/api/practice/drafts/count_bits/python",
                "PUT",
                {
                    "code": clean,
                    "revision": new_draft["revision"],
                    "codeFormat": "legacy-v1",
                },
            )
            check(
                changed["revision"] > new_draft["revision"]
                and changed["codeFormat"] == "legacy-v1",
                "format-only draft change creates a new revision",
            )
            api(
                base,
                "/api/practice/drafts/count_bits/python",
                "PUT",
                {
                    "code": clean,
                    "revision": changed["revision"],
                    "codeFormat": "callable-v1",
                },
            )
            status, _, _ = request(
                base,
                "/api/practice/drafts/count_bits/python",
                "PUT",
                {
                    "code": clean,
                    "revision": new_draft["revision"],
                    "codeFormat": "legacy-v1",
                },
            )
            check(
                status == 409,
                "stale format-only draft update conflicts without overwriting",
            )

            if args.browser:
                subprocess.run(
                    ["node", str(ROOT / "scripts/clarity/browser.cjs"), base],
                    check=True,
                    cwd=ROOT,
                )
                clarity = json.loads(
                    (artifact_root / "clarity-layout/report.json").read_text()
                )
                check(
                    clarity["passed"]
                    and len(clarity["checks"]) >= 15
                    and len(
                        {
                            (check["profile"], check["language"])
                            for check in clarity["checks"]
                        }
                    )
                    == 15,
                    "all language explanations fit desktop, mobile and native 200% zoom",
                )
                subprocess.run(
                    ["node", str(ROOT / "scripts/code_workspace/browser.cjs"), base],
                    cwd=ROOT,
                    check=True,
                )
            backup, _ = api(base, "/api/practice/export")
            check(
                backup["version"] == 2
                and {draft["codeFormat"] for draft in backup["drafts"]}
                == {"legacy-v1", "callable-v1"},
                "version 2 export contains both legacy and callable draft formats",
            )
            restored_dir = directory / "restored"
            restored_dir.mkdir()
            restored = Server(args.dll.resolve(), restored_dir)
            stack.callback(restored.close)
            api(restored.base, "/api/practice/import", "POST", backup)
            api(restored.base, "/api/practice/import", "POST", backup)
            restored_backup, _ = api(restored.base, "/api/practice/export")
            original_by_scope = {
                (d["problemId"], d["language"]): (d["code"], d["codeFormat"])
                for d in backup["drafts"]
            }
            restored_by_scope = {
                (d["problemId"], d["language"]): (d["code"], d["codeFormat"])
                for d in restored_backup["drafts"]
            }
            check(
                original_by_scope == restored_by_scope,
                "mixed-format backup restoration preserves all exact source strings and formats",
            )
            original_attempts = {
                a["id"]: (a["code"], a["codeFormat"]) for a in backup["attempts"]
            }
            restored_attempts = {
                a["id"]: (a["code"], a["codeFormat"])
                for a in restored_backup["attempts"]
            }
            check(
                original_attempts == restored_attempts,
                "mixed-format attempt snapshots restore without duplication",
            )
            v1 = {
                "version": 1,
                "drafts": [
                    {
                        "problemId": "parity",
                        "language": "python",
                        "code": "# old backup Ω\r\n",
                        "revision": 0,
                        "updatedAt": "2026-01-01T00:00:00Z",
                    }
                ],
                "attempts": [],
                "solvedIds": [],
            }
            api(restored.base, "/api/practice/import", "POST", v1)
            restored_state, _ = api(restored.base, "/api/practice")
            check(
                any(
                    d["problemId"] == "parity"
                    and d["code"] == "# old backup Ω\r\n"
                    and d["codeFormat"] == "legacy-v1"
                    for d in restored_state["drafts"]
                ),
                "version 1 backup remains valid and defaults safely to legacy",
            )
            report["passed"] = True
    except Exception:
        report["error"] = traceback.format_exc()
        raise
    finally:
        (artifact_root / "callable-http.json").write_text(
            json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n"
        )
    print(
        f"PASS callable HTTP {len(checks)} checks; all {expected_pairs * 2} payloads; browser={args.browser}; timeoutsSkipped={args.no_timeouts}",
        flush=True,
    )


if __name__ == "__main__":
    main()
