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
    review = json.loads((ROOT / "ctci6/review01.json").read_text())
    reviewed = {row["ref"] for row in review["questions"]}
    staged = json.loads((ROOT / "ctci6/staged/catalog.json").read_text())
    staged_refs = {row["ref"] for row in staged}
    if staged_refs != reviewed or len(staged_refs) != len(staged):
        raise ValueError(
            "Staged chapter-one references differ from explicit content review"
        )
    report = json.loads((ROOT / "ctci6/staged/validation.json").read_text())
    for name, expected in report["sourceHashes"].items():
        path = ROOT / name
        if (
            not path.is_file()
            or hashlib.sha256(path.read_bytes()).hexdigest() != expected
        ):
            raise ValueError("Stale execution evidence: " + name)
    executed = {
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
        executed != expected
        or rejected != expected
        or report["stage"] != "standalone-authoring-only"
    ):
        raise ValueError("Incomplete or misclassified standalone execution evidence")
    for row in staged:
        if set(row["languages"]) != languages:
            raise ValueError("Missing staged language: " + row["ref"])
        cases = json.loads(
            (ROOT / "ctci6/staged/cases" / (row["id"] + ".json")).read_text()
        )
        if len(cases) != row["testCount"]:
            raise ValueError("Staged case count differs: " + row["ref"])
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
