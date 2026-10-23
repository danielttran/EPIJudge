"""Track semantic review independently from catalog shape and execution evidence.

`inventory` creates missing pending records without claiming a review. `check`
requires complete, current review records. A digest detects edits after review;
it is not itself evidence that a human-readable contract or proof is correct.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "scripts/clarity/review.json"
STATEMENT_CHECKS = (
    "inputDomain",
    "outputAndTies",
    "mutationAndIdentity",
    "boundaryBehavior",
    "examples",
    "languageContracts",
    "judgeAgreement",
)
SOLUTION_CHECKS = (
    "actualAlgorithm",
    "correctness",
    "workedTrace",
    "edgeCases",
    "timeDerivation",
    "spaceDerivation",
    "callableAgreement",
)


def digest(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, ensure_ascii=False).encode()
    ).hexdigest()


def inputs():
    coverage = json.loads((ROOT / "solutions/coverage.json").read_text())
    callables = {
        (p["problemId"], p["language"]): p
        for p in json.loads((ROOT / "workspace-code/catalog.json").read_text())[
            "entries"
        ]
    }
    statements = {}
    for filename in (
        "EpiJudge.Runner/catalog.json",
        "blind75/catalog.json",
        "interviewcake/catalog.json",
        "ctci6/catalog.json",
    ):
        for p in json.loads((ROOT / filename).read_text()):
            normalized = {k.lower(): v for k, v in p.items()}
            statements[normalized["id"]] = {
                k: normalized[k] for k in ("description", "constraints", "examples")
            }
    # Curated declarations are source-authored rather than generated JSON.
    source = (ROOT / "EpiJudge.Runner/ProblemCatalog.cs").read_text()
    for name in ("count_bits", "two_sum", "anagrams"):
        start = source.index('new("' + name + '"')
        end = source.find('\n        new("', start + 1)
        statements[name] = source[
            start : end if end >= 0 else source.index("\n    ];", start)
        ]
    return coverage, callables, statements


def snapshot():
    coverage, callables, statements = inputs()
    contracts_path = ROOT / "scripts/clarity/contracts.json"
    contracts = (
        json.loads(contracts_path.read_text()) if contracts_path.exists() else {}
    )
    questions, solutions = {}, {}
    for entry in coverage["entries"]:
        problem, language = entry["problemId"], entry["language"]
        questions[problem] = {
            "collection": entry["collection"],
            "statementSha256": digest(
                {"statement": statements[problem], "contracts": contracts.get(problem)}
            ),
        }
        notes = json.loads((ROOT / entry["notesPath"]).read_text())
        solutions[problem + "/" + language] = {
            "codePath": entry["codePath"],
            "notesPath": entry["notesPath"],
            "contentSha256": digest(
                {
                    "code": (ROOT / entry["codePath"]).read_text(),
                    "notes": notes,
                    "callable": callables[problem, language],
                }
            ),
        }
    return questions, solutions


def pending(record, checks):
    return dict(record, status="pending", checks={k: None for k in checks}, evidence=[])


def inventory():
    questions, solutions = snapshot()
    ledger = (
        json.loads(LEDGER.read_text())
        if LEDGER.exists()
        else {
            "schemaVersion": 1,
            "baselineCommit": "f5ae2fabb0712830a3c57cb8b6c05af605d1d221",
            "questions": {},
            "solutions": {},
        }
    )
    for section, rows, checks in (
        ("questions", questions, STATEMENT_CHECKS),
        ("solutions", solutions, SOLUTION_CHECKS),
    ):
        for key, record in rows.items():
            ledger[section].setdefault(key, pending(record, checks))
    LEDGER.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n")
    report(ledger)


def report(ledger):
    for section in ("questions", "solutions"):
        rows = ledger[section]
        print(
            f"{section}: {sum(r['status'] == 'reviewed' for r in rows.values())}/{len(rows)} marked reviewed"
        )


def check():
    ledger = json.loads(LEDGER.read_text())
    questions, solutions = snapshot()
    errors = []
    contracts = json.loads((ROOT / "scripts/clarity/contracts.json").read_text())
    coverage, _, _ = inputs()
    for entry in coverage["entries"]:
        problem, language = entry["problemId"], entry["language"]
        key = problem + "/" + language
        contract = contracts.get(problem, {}).get(language)
        if (
            not isinstance(contract, list)
            or not contract
            or any(not isinstance(s, str) or not s.strip() for s in contract)
        ):
            errors.append(f"{key}: missing callable contract")
        notes = json.loads((ROOT / entry["notesPath"]).read_text())
        for field in (
            "explanation",
            "correctness",
            "walkthrough",
            "timeComplexity",
            "spaceComplexity",
        ):
            if not isinstance(notes.get(field), str) or not notes[field].strip():
                errors.append(f"{key}: missing {field}")
        if (
            not isinstance(notes.get("edgeCases"), list)
            or not notes["edgeCases"]
            or any(not isinstance(s, str) or not s.strip() for s in notes["edgeCases"])
        ):
            errors.append(f"{key}: missing edge cases")
        trace = notes.get("walkthroughCase")
        if (
            not isinstance(trace, dict)
            or not isinstance(trace.get("arguments"), list)
            or "expected" not in trace
        ):
            errors.append(f"{key}: missing executable language walkthrough")
    for section, rows, checks in (
        ("questions", questions, STATEMENT_CHECKS),
        ("solutions", solutions, SOLUTION_CHECKS),
    ):
        actual = ledger[section]
        if actual.keys() != rows.keys():
            errors.append(f"{section}: inventory differs from live coverage")
        for key, current in rows.items():
            review = actual.get(key, {})
            if review.get("status") != "reviewed":
                errors.append(f"{key}: semantic review pending")
                continue
            if any(review.get(k) != v for k, v in current.items()):
                errors.append(f"{key}: review fingerprint is stale")
            decisions = review.get("checks", {})
            if set(decisions) != set(checks) or any(
                not isinstance(v, str) or not v.strip() for v in decisions.values()
            ):
                errors.append(f"{key}: missing written review decisions")
            if not review.get("evidence"):
                errors.append(f"{key}: missing review evidence")
    report(ledger)
    if errors:
        print("\n".join(errors[:20]))
        raise SystemExit(
            f"INCOMPLETE: {len(errors)} review issues; structural inventory is not semantic acceptance"
        )
    print(
        "PASS complete current review ledger; run execution and rendered-content gates separately"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("inventory", "check"))
    args = parser.parse_args()
    inventory() if args.command == "inventory" else check()
