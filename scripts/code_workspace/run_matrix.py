"""Run complete callable acceptance with bounded local process concurrency."""

import argparse
import json
import subprocess
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime
from pathlib import Path

from common import ROOT


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit-dll", type=Path, required=True)
    parser.add_argument("--fixtures-dll", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--tag", default="final")
    args = parser.parse_args()
    if args.workers < 1 or args.workers > 4 or not args.tag.replace("-", "").isalnum():
        raise ValueError("Use 1..4 workers and a simple report tag")
    for path in [args.audit_dll, args.fixtures_dll]:
        if not path.is_file():
            raise FileNotFoundError(path)
    artifacts = ROOT / ".epi-runs"
    logs = artifacts / ("callable-matrix-" + args.tag)
    logs.mkdir(parents=True, exist_ok=True)
    audit = ["dotnet", str(args.audit_dll.resolve())]
    fixture = ["dotnet", str(args.fixtures_dll.resolve())]
    languages = ["csharp", "cpp", "java", "python", "javascript"]
    jobs = []
    for language in languages:
        jobs.append(
            (
                "solution-" + language,
                audit
                + [
                    "--callable",
                    "--language=" + language,
                    "--report=callable-correct-" + language + "-" + args.tag,
                ],
            )
        )
    for language in ["cpp", "csharp", "java", "python", "javascript"]:
        jobs.append(
            (
                "starter-" + language,
                audit
                + [
                    "--callable",
                    "--starters",
                    "--language=" + language,
                    "--report=callable-starter-" + language + "-" + args.tag,
                ],
            )
        )
    for language in languages:
        jobs.append(
            (
                "boundaries-" + language,
                audit + ["boundaries", "--callable", "--language=" + language],
            )
        )
    jobs.append(("walkthroughs-csharp", audit + ["walkthroughs", "--callable"]))
    for language in languages:
        jobs.append(("fixtures-" + language, fixture + [language, "all", "--callable"]))
    ledger = {"tag": args.tag, "jobs": [], "completed": False, "passed": False}
    ledger_path = artifacts / ("callable-matrix-" + args.tag + ".json")
    lock = threading.Lock()

    def now():
        return datetime.now(UTC).isoformat()

    def run(job):
        name, command = job
        row = {
            "name": name,
            "command": command,
            "startedUtc": now(),
            "status": "running",
        }
        log = logs / (name + ".log")
        row["log"] = log.relative_to(ROOT).as_posix()
        with lock:
            ledger["jobs"].append(row)
            ledger_path.write_text(
                json.dumps(ledger, indent=2) + "\n", encoding="utf-8", newline="\n"
            )
            print("START " + name, flush=True)
        with log.open("w", encoding="utf-8", newline="\n") as output:
            result = subprocess.run(
                command, cwd=ROOT, stdout=output, stderr=subprocess.STDOUT, check=False
            )
        with lock:
            row.update(
                exitCode=result.returncode,
                finishedUtc=now(),
                status="completed",
                passed=result.returncode == 0,
            )
            ledger_path.write_text(
                json.dumps(ledger, indent=2) + "\n", encoding="utf-8", newline="\n"
            )
            print(
                ("PASS " if result.returncode == 0 else "FAIL ")
                + name
                + " -> "
                + row["log"],
                flush=True,
            )
        return result.returncode == 0

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = [pool.submit(run, job) for job in jobs]
        outcomes = [future.result() for future in as_completed(results)]
        passed = all(outcomes)
    ledger.update(completed=True, passed=passed, finishedUtc=now())
    ledger_path.write_text(
        json.dumps(ledger, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(f"Completed {len(jobs)} full matrix jobs; passed={passed}", flush=True)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
