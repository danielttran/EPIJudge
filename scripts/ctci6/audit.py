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
        if row["classification"] not in {"coding", "conceptual", "design", "algorithm-candidate", "coding-candidate", "classification-pending"}:
            raise ValueError("Unreviewed classification: " + row["ref"])
        if (
            row["ref"] != f"{row['chapter']}.{row['number']}"
            or not row["title"].strip()
        ):
            raise ValueError("Invalid reference metadata")
        for source in row["sources"]:
            if source.get("provider") == "SDE Skills":
                if (
                    source.get("url") != "https://www.sdeskills.com/ctci"
                    or row["chapter"] != 12
                    or source.get("evidenceType") != "independent-course-numbered-index"
                    or (row["classification"] == "coding" and not any(s.get("repository", "").startswith("careercup/") for s in row["sources"]))
                ):
                    raise ValueError("Course index cannot establish executable specifications")
                continue
            if (
                not re.fullmatch(r"[0-9a-f]{40}", source["commit"])
                or source["commit"] not in source["url"]
            ):
                raise ValueError("Source provenance is not pinned: " + row["ref"])
            if not source["repository"].startswith("careercup/") and not (
                source["repository"] == "satheeshaGowda/Cracking-The-Coding-Interview"
                and source["commit"] == "8d40586f0f7498bd6568e9f3c6da2a2d6b21603b"
                and row["chapter"] in (11, 13, 14, 15)
                and row["classification"] != "coding"
            ):
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
        row["classification"] in ("algorithm-candidate", "coding-candidate") for row in rows
    ):
        raise ValueError("Candidate count is stale")
    if scope["requiresIndividualClassification"] != sum(
        row["classification"] == "classification-pending" for row in rows
    ):
        raise ValueError("Individual-classification count is stale")
    metadata = {row["ref"]: row for row in rows}
    classifications = json.loads(
        (ROOT / "ctci6/classification-review.json").read_text()
    )["reviews"]
    excluded = {
        row["ref"] for row in rows if row["classification"] in ("conceptual", "design")
    }
    if len(classifications) != len(
        {row["ref"] for row in classifications}
    ) or excluded != {row["ref"] for row in classifications}:
        raise ValueError("Noncallable classifications differ from explicit review")
    for category, field in (
        ("conceptual", "conceptualReferences"),
        ("design", "designReferences"),
    ):
        if scope[field] != sum(row["classification"] == category for row in rows):
            raise ValueError("Noncallable classification count is stale")
    for review in classifications:
        if metadata[review["ref"]]["classification"] != review["classification"]:
            raise ValueError("Classification differs from its reviewed category")
        if not any(
            (
                source.get("repository") == review.get("repository")
                and source.get("commit") == review.get("commit")
                if "repository" in review
                else source.get("provider") == review.get("provider")
                and source.get("url") == review.get("url")
            )
            and review["path"] in source["files"]
            for source in metadata[review["ref"]]["sources"]
        ):
            raise ValueError("Classification evidence is not a pinned inventory source")
    reviewed = set()
    executed = set()
    for staging_name, review_file in (
        ("staged", "review01.json"),
        ("staged02", "review02.json"),
        ("staged03", "review03.json"),
        ("staged04", "review04.json"),
        ("staged05", "review05.json"),
        ("staged07", "review07.json"),
        ("staged08", "review08.json"),
        ("staged10", "review10.json"),
        ("staged13", "review13.json"),
        ("staged15", "review15.json"),
        ("staged16", "review16.json"),
        ("staged17", "review17.json"),
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
        if languages != {"csharp", "javascript", "python", "cpp", "java"}:
            raise ValueError("Every coding review must cover the five supported languages")
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
        record_keys = [
            (record["ref"], record["language"], record["variant"])
            for record in report["executions"]
        ]
        if (
            len(record_keys) != len(set(record_keys))
            or len(record_keys) != len(expected) * 2
        ):
            raise ValueError("Duplicated or extraneous standalone execution records")
        for row in staged:
            if row["title"] != metadata[row["ref"]]["title"]:
                raise ValueError(
                    "Staged title differs from the source-established reference"
                )
            if any(
                record["cases"] != row["testCount"]
                for record in report["executions"]
                if record["ref"] == row["ref"]
            ):
                raise ValueError(
                    "Pair execution count differs from its authored corpus"
                )
            if set(row["languages"]) != languages:
                raise ValueError("Missing staged language: " + row["ref"])
            cases = json.loads(
                (staged_root / "cases" / (row["id"] + ".json")).read_text()
            )
            if len(cases) != row["testCount"]:
                raise ValueError("Staged case count differs: " + row["ref"])
    if {row["ref"] for row in rows if row["classification"] == "coding"} != reviewed:
        raise ValueError("Coding inventory differs from explicit reviewed scope")
    if scope["stagedExercises"] != len(reviewed) or scope[
        "stagedLanguageSolutions"
    ] != len(executed):
        raise ValueError("Staged scope totals are stale")
    def current_evidence(filename, status):
        path = ROOT / "ctci6" / filename
        if not path.is_file():
            return False
        document = json.loads(path.read_text())
        hashes = document.get("sourceHashes", {})
        return document.get("status") == status and bool(hashes) and all(
            (ROOT / name).is_file()
            and hashlib.sha256((ROOT / name).read_bytes()).hexdigest().lower() == value.lower()
            for name, value in hashes.items()
        )

    pending = [row["ref"] for row in rows if row["classification"] in ("algorithm-candidate", "coding-candidate")]
    exclusions_path = ROOT / "ctci6/exclusions.json"
    excluded_publication = set()
    if exclusions_path.is_file():
        exclusions = json.loads(exclusions_path.read_text())
        entries = exclusions["exclusions"]
        excluded_publication = {row["ref"] for row in entries}
        if (excluded_publication != {"12.2", "12.8", "12.9", "12.10", "12.11", "14.1", "14.2", "14.3"}
            or len(entries) != len(excluded_publication)
            or excluded_publication != set(pending)
            or exclusions["supportedExercises"] != len(reviewed)
            or exclusions["supportedSolutionPairs"] != len(executed)
            or exclusions["completeBookCodingCoverage"] is not False
            or any(row["disposition"] != "excluded-from-supported-publication" or not row["reason"] or not row["evidenceUrls"] for row in entries)):
            raise ValueError("Supported-publication exclusions must explicitly reconcile every unresolved reference")
    bank_current = current_evidence("whole-bank-validation.json", "passed-current-registered-bank")
    integration_current = current_evidence("integration-validation.json", "passed-current-registered-bank-integration")
    remaining = []
    if set(pending) - excluded_publication:
        remaining.append("Unresolved coding references without reviewed publication disposition")
    if not bank_current:
        remaining.append("Current whole-bank application-callable execution evidence")
    if not integration_current:
        remaining.append("Current integration and rendered audit evidence")
    ready = not remaining and len(rows) == inventory["advertisedQuestions"] and not scope["requiresIndividualClassification"]
    result = dict(
        inventoryIntegrity="passed",
        identifiedReferences=len(rows),
        unresolvedAdvertisedReferences=inventory["advertisedQuestions"] - len(rows),
        explicitStatementReviews=len(reviewed),
        standaloneValidatedPairs=len(executed),
        liveCtciExercises=scope["liveExercises"],
        publicationReady=ready,
        publicationScope="audited-supported-five-language-coding-collection",
        completeBookCodingCoverage=not pending,
        excludedFromSupportedPublication=sorted(excluded_publication, key=lambda value: tuple(map(int, value.split(".")))),
        wholeBankCallableEvidence="passed-current" if bank_current else "missing-or-stale",
        integrationAndRenderedEvidence="passed-current" if integration_current else "missing-or-stale",
        pendingCodingReferences=pending,
        remaining=remaining,
        publicationStatus="Source-bound supported-collection acceptance; remote publication and exact-commit CI are tracked separately.",
    )
    print(json.dumps(result, indent=2))
    if publication and not ready:
        raise ValueError(
            "CtCI publication acceptance is incomplete: " + "; ".join(remaining)
            + ". Structural inventory integrity is not semantic review or live execution coverage."
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--publication", action="store_true")
    audit(parser.parse_args().publication)
