"""Execute all three staged fixed-width bit tasks in all five languages."""

import hashlib
import json
import time

from chapter05 import SPECS
from core import LANGUAGES, ROOT
from corpus05 import cases, valid_observation
from generate05 import generate05
from harness05 import source
from verify01 import execute, standalone_paths


def verify():
    generate05()
    started = time.monotonic()
    rows = [dict(ref=s["ref"], **case) for s in SPECS for case in cases(s)]
    output = ROOT / ".epi-runs/ctci6-chapter05"
    evidence = []
    for language in LANGUAGES:
        for starters in (False, True):
            label = "starter" if starters else "solution"
            print(
                f"Executing staged bit {language} {label}: {len(rows)} cases",
                flush=True,
            )
            actual = execute(
                language,
                starters,
                rows,
                output / (language + "-" + label),
                source_builder=source,
            )
            if len(actual) != len(rows):
                raise AssertionError("Incomplete bit execution")
            failures = [
                dict(
                    ref=case["ref"],
                    arguments=case["arguments"],
                    expected=case["expected"],
                    observed=value,
                )
                for case, value in zip(rows, actual)
                if not valid_observation(case, value)
            ]
            if not starters and failures:
                (output / "failure.json").write_text(json.dumps(failures[:3], indent=2))
                raise AssertionError(
                    f"{language}: {len(failures)} bit failures; see {output / 'failure.json'}"
                )
            if starters and {f["ref"] for f in failures} != {s["ref"] for s in SPECS}:
                raise AssertionError("Some bit starter was accepted")
            evidence.extend(
                dict(
                    ref=s["ref"],
                    language=language,
                    variant=label,
                    cases=sum(r["ref"] == s["ref"] for r in rows),
                    outcome="rejected" if starters else "passed",
                )
                for s in SPECS
            )
            print(
                f"Passed bit {language} {label} expectations across {len(SPECS)} exercises",
                flush=True,
            )
    paths = standalone_paths(5, "staged05")
    hashes = {
        str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in paths
        if p.is_file() and p.name != "validation.json"
    }
    report = dict(
        status="passed",
        stage="standalone-authoring-only",
        livePublication="pending",
        questions=len(SPECS),
        solutionLanguagePairs=len(SPECS) * len(LANGUAGES),
        solutionCaseExecutions=len(rows) * len(LANGUAGES),
        starterCaseExecutions=len(rows) * len(LANGUAGES),
        elapsedSeconds=round(time.monotonic() - started, 2),
        sourceHashes=hashes,
        executions=evidence,
    )
    (ROOT / "ctci6/staged05/validation.json").write_text(
        json.dumps(report, indent=2) + "\n"
    )
    print(
        json.dumps(
            {k: v for k, v in report.items() if k not in ("sourceHashes", "executions")}
        ),
        flush=True,
    )


if __name__ == "__main__":
    verify()
