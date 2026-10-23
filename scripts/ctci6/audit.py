"""Validate inventory/evidence integrity without claiming semantic completion."""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]


def audit(publication=False):
    inventory = json.loads((ROOT / "ctci6/inventory.json").read_text())
    rows = inventory["questions"]
    references = [row["ref"] for row in rows]
    if len(set(references)) != len(rows):
        raise ValueError("Duplicate canonical CtCI references")
    if references != sorted(references, key=lambda s: tuple(map(int, s.split(".")))):
        raise ValueError("CtCI inventory order differs from chapter/problem order")
    for row in rows:
        if (
            row["ref"] != f"{row['chapter']}.{row['number']}"
            or not row["title"].strip()
        ):
            raise ValueError("Invalid reference metadata")
        for source in row["sources"]:
            if (
                not re.fullmatch(r"[0-9a-f]{40}", source["commit"])
                or source["commit"] not in source["url"]
            ):
                raise ValueError("Source provenance is not pinned: " + row["ref"])
            if not source["repository"].startswith("careercup/"):
                raise ValueError("Unreviewed inventory source: " + source["repository"])
        if not row["sources"]:
            raise ValueError("Unestablished reference: " + row["ref"])
    chapters = Counter(row["chapter"] for row in rows)
    if dict(chapters) != {
        row["chapter"]: row["identifiedReferences"] for row in inventory["chapters"]
    }:
        raise ValueError("Chapter inventory totals differ")
    scope = inventory["scope"]
    if scope["identifiedNumberedReferences"] != len(rows) or scope[
        "unlocatedAdvertisedReferences"
    ] != inventory["advertisedQuestions"] - len(rows):
        raise ValueError("Advertised and located totals differ")
    if scope["algorithmCandidates"] != sum(
        row["classification"] == "algorithm-candidate" for row in rows
    ):
        raise ValueError("Candidate count is stale")
    reviewed = set()
    executed = set()
    for staging_name, review_file in (
        ("staged", "review01.json"),
        ("staged02", "review02.json"),
        ("staged03", "review03.json"),
    ):
        review = json.loads((ROOT / "ctci6" / review_file).read_text())
        batch_reviewed = {row["ref"] for row in review["questions"]}
        staged_root = ROOT / "ctci6" / staging_name
        staged = json.loads((staged_root / "catalog.json").read_text())
        staged_refs = {row["ref"] for row in staged}
        if (
            staged_refs != batch_reviewed
            or len(staged_refs) != len(staged)
            or reviewed & batch_reviewed
        ):
            raise ValueError("Staged references differ from explicit content review")
        reviewed.update(batch_reviewed)
        report = json.loads((staged_root / "validation.json").read_text())
        for name, expected_hash in report["sourceHashes"].items():
            path = ROOT / name
            if (
                not path.is_file()
                or hashlib.sha256(path.read_bytes()).hexdigest() != expected_hash
            ):
                raise ValueError("Stale execution evidence: " + name)
        batch_executed = {
            (row["ref"], row["language"])
            for row in report["executions"]
            if row["variant"] == "solution" and row["outcome"] == "passed"
        }
        rejected = {
            (row["ref"], row["language"])
            for row in report["executions"]
            if row["variant"] == "starter" and row["outcome"] == "rejected"
        }
        languages = set(review["languagesReviewed"])
        expected = {(ref, language) for ref in staged_refs for language in languages}
        if (
            batch_executed != expected
            or rejected != expected
            or report["status"] != "passed"
            or report["stage"] != "standalone-authoring-only"
        ):
            raise ValueError(
                "Incomplete or misclassified standalone execution evidence"
            )
        if (
            sum(
                row["cases"]
                for row in report["executions"]
                if row["variant"] == "solution"
            )
            != report["solutionCaseExecutions"]
        ):
            raise ValueError("Execution totals differ from individual pair records")
        executed.update(batch_executed)
        for row in staged:
            if set(row["languages"]) != languages:
                raise ValueError("Missing staged language: " + row["ref"])
            cases = json.loads(
                (staged_root / "cases" / (row["id"] + ".json")).read_text()
            )
            if len(cases) != row["testCount"]:
                raise ValueError("Staged case count differs: " + row["ref"])
    if scope["stagedExercises"] != len(reviewed) or scope[
        "stagedLanguageSolutions"
    ] != len(executed):
        raise ValueError("Staged scope totals are stale")
    result = dict(
        inventoryIntegrity="passed",
        identifiedReferences=len(rows),
        unresolvedAdvertisedReferences=inventory["advertisedQuestions"] - len(rows),
        explicitStatementReviews=len(reviewed),
        standaloneValidatedPairs=len(executed),
        liveCtciExercises=scope["liveExercises"],
        publicationReady=False,
        remaining="Unresolved references, remaining eligible content and language reviews, live callable integration, whole-bank execution, browser audit and exact-commit CI.",
    )
    print(json.dumps(result, indent=2))
    if publication:
        raise ValueError(
            "CtCI publication acceptance is incomplete; structural inventory integrity is not semantic review or live execution coverage."
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--publication", action="store_true")
    audit(parser.parse_args().publication)
