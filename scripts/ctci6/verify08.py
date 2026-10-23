"""Execute the first three staged recursion/DP tasks in all five languages."""

import hashlib
import json
import time

from chapter08 import SPECS
from core import LANGUAGES, ROOT
from corpus08 import cases, valid_observation
from generate08 import generate08
from harness08 import source
from verify01 import execute, standalone_paths


def verify(specs=SPECS, batch=8, generator=generate08, case_builder=cases, matcher=valid_observation, adapter=source):
    generator()
    started = time.monotonic()
    rows = [dict(ref=s["ref"], **case) for s in specs for case in case_builder(s)]
    output = ROOT / f".epi-runs/ctci6-chapter{batch:02}"
    evidence = []
    for language in LANGUAGES:
        for starters in (False, True):
            label = "starter" if starters else "solution"
            print(
                f"Executing staged recursion/DP {language} {label}: {len(rows)} cases",
                flush=True,
            )
            actual = execute(
                language,
                starters,
                rows,
                output / (language + "-" + label),
                source_builder=adapter,
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
                if not matcher(case["ref"], case, value)
            ]
            if not starters and failures:
                (output / "failure.json").write_text(json.dumps(failures[:3], indent=2))
                raise AssertionError(
                    f"{language}: {len(failures)} bit failures; see {output / 'failure.json'}"
                )
            if starters and {f["ref"] for f in failures} != {s["ref"] for s in specs}:
                raise AssertionError("Some bit starter was accepted")
            evidence.extend(
                dict(
                    ref=s["ref"],
                    language=language,
                    variant=label,
                    cases=sum(r["ref"] == s["ref"] for r in rows),
                    outcome="rejected" if starters else "passed",
                )
                for s in specs
            )
            print(
                f"Passed recursion/DP {language} {label} expectations across {len(specs)} exercises",
                flush=True,
            )
    paths = standalone_paths(batch, f"staged{batch:02}") + [ROOT / "scripts/ctci6/harness08_typed.py", ROOT / "scripts/ctci6/verify08.py", ROOT / "scripts/ctci6/models08.py"]
    hashes = {
        str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in paths
        if p.is_file() and p.name != "validation.json"
    }
    report = dict(
        status="passed",
        stage="standalone-authoring-only",
        livePublication="pending",
        questions=len(specs),
        solutionLanguagePairs=len(specs) * len(LANGUAGES),
        solutionCaseExecutions=len(rows) * len(LANGUAGES),
        starterCaseExecutions=len(rows) * len(LANGUAGES),
        elapsedSeconds=round(time.monotonic() - started, 2),
        sourceHashes=hashes,
        executions=evidence,
    )
    (ROOT / f"ctci6/staged{batch:02}/validation.json").write_text(
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
