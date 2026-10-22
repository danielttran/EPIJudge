"""Accept only complete, current execution evidence for the exact displayed solutions."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def current(hashes):
    return bool(hashes) and all(
        (ROOT / name).is_file() and sha(ROOT / name) == expected
        for name, expected in hashes.items()
    )


def corpus_path(entry):
    collection, problem_id = entry["collection"], entry["problemId"]
    return ROOT / (
        f"{collection}/cases/{problem_id}.json"
        if collection != "epi"
        else f"test_data/{problem_id}.tsv"
    )


def auxiliary_evidence(label, cases, paths, languages, accepted, source_hashes):
    expected = {
        (case["problemId"], language) for case in cases for language in languages
    }
    accepted_rows = {}
    fixture_hashes = {path.relative_to(ROOT).as_posix(): sha(path) for path in paths}
    for path in sorted(
        (ROOT / ".epi-runs").glob(f"solutions-{label}*.json"),
        key=lambda p: p.stat().st_mtime,
    ):
        report = json.loads(path.read_text(encoding="utf-8"))
        if (
            report["sourceHashes"] != source_hashes
            or report["fixtureHashes"] != fixture_hashes
        ):
            continue
        for row in report["executions"]:
            key = row["problemId"], row["language"]
            if key not in expected:
                continue
            count = sum(case["problemId"] == key[0] for case in cases)
            result = row.get("result") or {}
            if (
                row["success"]
                and result.get("Status") == "Accepted"
                and result["Passed"] == result["Total"] == count
                and row["codeSha256"] == accepted[key]["codeSha256"]
            ):
                accepted_rows[key] = row
            else:
                accepted_rows.pop(key, None)
    missing = sorted(expected - accepted_rows.keys())
    if missing:
        raise ValueError(
            f"{label}: {len(missing)} missing/current failing executions: {missing}"
        )
    return dict(
        questionLanguageExecutions=len(accepted_rows),
        acceptedCaseEvaluations=sum(
            row["result"]["Total"] for row in accepted_rows.values()
        ),
    )


def collection_fixture_evidence(manifest, harnesses):
    definitions = {
        row["id"]: row
        for row in json.loads(
            (ROOT / "interviewcake/catalog.json").read_text(encoding="utf-8")
        )
    }
    expected = {
        (problem_id, language, variant)
        for problem_id in definitions
        for language in manifest["languages"]
        for variant in ("starter", "correct", "incorrect")
    }
    suffixes = {
        "csharp": "cs",
        "javascript": "js",
        "python": "py",
        "cpp": "cpp",
        "java": "java",
    }
    runner_hash = sha(ROOT / "EpiJudge.Runner/InterviewCakeSubmissionRunner.cs")
    catalog_hash = sha(ROOT / "interviewcake/catalog.json")
    accepted = {}
    for path in sorted(
        (ROOT / ".epi-runs").glob("interviewcake-audit-*.json"),
        key=lambda p: p.stat().st_mtime,
    ):
        report = json.loads(path.read_text(encoding="utf-8"))
        if (
            report.get("runnerSha256") != runner_hash
            or report.get("catalogSha256") != catalog_hash
        ):
            continue
        for row in report["evidence"]:
            key = row["problemId"], row["language"], row["variant"]
            if key not in expected:
                continue
            problem_id, language, variant = key
            definition = definitions[problem_id]
            if variant == "starter":
                code = definition["starters"][language]["starterCode"]
                code_hash = hashlib.sha256(code.encode()).hexdigest().upper()
            else:
                directory = (
                    "solutions"
                    if variant == "correct"
                    else "interviewcake/fixtures/incorrect"
                )
                code_hash = sha(
                    ROOT / directory / language / f"{problem_id}.{suffixes[language]}"
                )
            if (
                row["codeSha256"] != code_hash
                or row["harnessSha256"] != harnesses[(problem_id, language)]
                or row["corpusSha256"]
                != sha(ROOT / "interviewcake/cases" / f"{problem_id}.json")
            ):
                continue
            result = row.get("result") or {}
            total = definition["testCount"]
            archive = (
                ROOT
                / ".epi-runs/interviewcake-executions"
                / report["runId"]
                / language
                / f"{problem_id}-{variant}.json"
            )
            success = (
                row["success"]
                and result.get("Total") == total
                and row.get("executionReportRows") == total
                and archive.is_file()
                and row.get("executionReportSha256") == sha(archive)
                and len(json.loads(archive.read_text(encoding="utf-8"))) == total
            )
            if variant == "correct":
                success = (
                    success
                    and result.get("Status") == "Accepted"
                    and result.get("Passed") == total
                )
            elif variant == "starter":
                success = (
                    success
                    and bool(result.get("Cases"))
                    and result.get("Status")
                    in ("Accepted", "Wrong answer", "Runtime error")
                )
            else:
                success = (
                    success
                    and result.get("Passed", total) < total
                    and result.get("Status") in ("Wrong answer", "Runtime error")
                )
            if success:
                accepted[key] = dict(row, report=path.name)
            else:
                accepted.pop(key, None)
    missing = sorted(expected - accepted.keys())
    if missing:
        raise ValueError(
            f"Interview Cake: {len(missing)} missing/current failing starter/correct/incorrect executions: {missing}"
        )
    return dict(
        questions=len(definitions),
        questionLanguagePairs=len(definitions) * len(manifest["languages"]),
        fixtureExecutions=len(accepted),
        variants=["starter", "correct", "incorrect"],
        failures=0,
    )


def main():
    manifest = json.loads(
        (ROOT / "solutions/coverage.json").read_text(encoding="utf-8")
    )
    entries = {
        (entry["problemId"], entry["language"]): entry for entry in manifest["entries"]
    }
    catalog = {
        (row["problemId"], row["language"]): row
        for row in json.loads(
            (ROOT / "solutions/catalog.json").read_text(encoding="utf-8")
        )
    }
    if (
        len(entries) != manifest["questionCount"] * len(manifest["languages"])
        or catalog.keys() != entries.keys()
    ):
        raise ValueError("Incomplete or mismatched displayed solution coverage")
    compiled = json.loads(
        (ROOT / ".epi-runs/solutions-harnesses.json").read_text(encoding="utf-8")
    )
    if not current(compiled["sourceHashes"]):
        raise ValueError("Current compiled harness inventory is stale")
    harnesses = {
        (row["problemId"], row["language"]): row["harnessSha256"]
        for row in compiled["harnesses"]
    }
    if harnesses.keys() != entries.keys():
        raise ValueError("Compiled harness inventory is incomplete")
    accepted = {}
    for report_path in sorted(
        (ROOT / ".epi-runs").glob("solutions-audit-*.json"),
        key=lambda p: p.stat().st_mtime,
    ):
        report = json.loads(report_path.read_text(encoding="utf-8"))
        if report["sourceHashes"] != compiled["sourceHashes"]:
            continue
        for row in report["executions"]:
            key = row["problemId"], row.get("language")
            if key not in entries or not row["displayedEmbeddedCode"]:
                continue
            entry = entries[key]
            if (
                row["codeSha256"] != sha(ROOT / entry["codePath"])
                or row["notesSha256"] != sha(ROOT / entry["notesPath"])
                or row["corpusSha256"] != sha(corpus_path(entry))
                or row["harnessSha256"] != harnesses[key]
            ):
                continue
            if catalog[key]["code"] != (ROOT / entry["codePath"]).read_text(
                encoding="utf-8"
            ):
                raise ValueError(
                    "Displayed solution differs from source: " + "/".join(key)
                )
            result = row.get("result") or {}
            if (
                row["success"]
                and result.get("Status") == "Accepted"
                and result["Passed"] == entry["testCount"] == result["Total"]
            ):
                accepted[key] = dict(row, report=report_path.name)
            else:
                accepted.pop(key, None)
    missing = sorted(entries.keys() - accepted.keys())
    if missing:
        raise ValueError(
            f"{len(missing)} solutions lack current full-corpus displayed-code acceptance: {missing}"
        )
    fixtures = sorted((ROOT / "scripts/solutions").glob("boundaries-*.json"))
    boundaries = [
        row for path in fixtures for row in json.loads(path.read_text(encoding="utf-8"))
    ]
    boundary_summary = auxiliary_evidence(
        "boundaries",
        boundaries,
        fixtures,
        manifest["languages"],
        accepted,
        compiled["sourceHashes"],
    )
    walkthrough_summary = {
        "questionLanguageExecutions": 0,
        "acceptedCaseEvaluations": 0,
    }
    for language in manifest["languages"]:
        notes_dir = ROOT / "solutions/notes"
        if language != "csharp":
            notes_dir /= language
        walkthrough_paths = sorted(notes_dir.glob("*.json"))
        walkthroughs = [
            dict(
                problemId=path.stem,
                **json.loads(path.read_text(encoding="utf-8"))["walkthroughCase"],
            )
            for path in walkthrough_paths
        ]
        counts = auxiliary_evidence(
            "walkthroughs",
            walkthroughs,
            walkthrough_paths,
            [language],
            accepted,
            compiled["sourceHashes"],
        )
        for key in walkthrough_summary:
            walkthrough_summary[key] += counts[key]
    collection_summary = collection_fixture_evidence(manifest, harnesses)
    summary = dict(
        questions=manifest["questionCount"],
        solutionLanguagePairs=len(accepted),
        languages=manifest["languages"],
        collections=manifest["collections"],
        acceptedCaseEvaluations=sum(
            row["result"]["Total"] for row in accepted.values()
        ),
        additiveBoundaries=boundary_summary,
        originalWalkthroughs=walkthrough_summary,
        interviewCakeFixtures=collection_summary,
        catalogSha256=sha(ROOT / "solutions/catalog.json"),
        failures=0,
    )
    rows = [
        dict(row, questionId=key[0], language=key[1])
        for key, row in sorted(accepted.items())
    ]
    (ROOT / "solutions/validation-results.json").write_text(
        json.dumps(dict(summary=summary, executions=rows), indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
