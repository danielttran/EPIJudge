"""Compile every composed EPI native starter and solution without changing sources."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

try:
    from .common import ROOT
except ImportError:
    from common import ROOT


def run(command, timeout=90):
    start = time.monotonic()
    try:
        result = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            check=False,
            timeout=timeout,
        )
        return {
            "exitCode": result.returncode,
            "elapsedSeconds": time.monotonic() - start,
            "diagnostics": (result.stdout + result.stderr)[-20000:],
        }
    except subprocess.TimeoutExpired as error:
        return {
            "exitCode": None,
            "elapsedSeconds": time.monotonic() - start,
            "diagnostics": f"Compilation exceeded {timeout} seconds: {error}",
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--language", choices=["cpp", "java"])
    parser.add_argument("--variant", choices=["starter", "solution"])
    parser.add_argument("--problem", action="append")
    parser.add_argument("--jobs", type=int, default=3)
    parser.add_argument(
        "--report", type=Path, default=ROOT / ".epi-runs/native-code-compilation.json"
    )
    args = parser.parse_args()
    manifest_path = ROOT / "workspace-code/parts/epi-native.json"
    manifest_bytes = manifest_path.read_bytes()
    entries = json.loads(manifest_bytes)["entries"]
    entries = [
        e
        for e in entries
        if (not args.language or e["language"] == args.language)
        and (not args.problem or e["problemId"] in args.problem)
    ]
    variants = [args.variant] if args.variant else ["starter", "solution"]
    parent = ROOT / ".epi-runs"
    parent.mkdir(exist_ok=True)
    directory = Path(tempfile.mkdtemp(prefix="native-code-compile-", dir=parent))
    results = []
    for variant in variants:
        for language in ["cpp", "java"]:
            selected = [e for e in entries if e["language"] == language]
            if not selected:
                continue
            language_dir = directory / variant / language
            source_dir = language_dir / "epi" if language == "java" else language_dir
            source_dir.mkdir(parents=True)
            sources = []
            for entry in selected:
                source = entry["prefix"] + entry[variant + "Code"] + entry["suffix"]
                filename = (
                    entry["filename"]
                    if language == "java"
                    else entry["problemId"] + ".cpp"
                )
                path = source_dir / filename
                path.write_text(source, encoding="utf-8", newline="\n")
                sources.append(
                    (entry, path, hashlib.sha256(source.encode()).hexdigest())
                )
            if language == "java":
                javac = shutil.which("javac") or "/workspace/toolchains/jdk/bin/javac"
                output = language_dir / "classes"
                output.mkdir()
                command = [
                    javac,
                    "-encoding",
                    "UTF-8",
                    "--release",
                    "21",
                    "-parameters",
                    "-d",
                    str(output),
                    "-sourcepath",
                    str(language_dir) + os.pathsep + str(ROOT / "epi_judge_java"),
                ]
                command.extend(str(path) for _, path, _ in sources)
                result = run(command, 180)
                for entry, path, digest in sources:
                    results.append(
                        {
                            "problemId": entry["problemId"],
                            "language": language,
                            "variant": variant,
                            "sourceSha256": digest,
                            "batchCompilation": True,
                            **result,
                        }
                    )
                print(
                    f"{language}/{variant}: {len(sources)} sources, exit {result['exitCode']}",
                    flush=True,
                )
                if result["exitCode"]:
                    print(result["diagnostics"], flush=True)
            else:

                def compile_one(item, language=language, variant=variant):
                    entry, path, digest = item
                    result = run(
                        [
                            shutil.which("g++") or "g++",
                            "-std=c++17",
                            "-fsyntax-only",
                            "-pthread",
                            "-I",
                            str(ROOT / "epi_judge_cpp"),
                            str(path),
                        ],
                        60,
                    )
                    return {
                        "problemId": entry["problemId"],
                        "language": language,
                        "variant": variant,
                        "sourceSha256": digest,
                        "batchCompilation": False,
                        **result,
                    }

                with ThreadPoolExecutor(max_workers=args.jobs) as pool:
                    futures = [pool.submit(compile_one, item) for item in sources]
                    for future in as_completed(futures):
                        result = future.result()
                        results.append(result)
                        if result["exitCode"] != 0:
                            print(
                                f"FAILED {language}/{variant}/{result['problemId']}: {result['diagnostics']}",
                                flush=True,
                            )
                        if (
                            len(
                                [
                                    r
                                    for r in results
                                    if r["language"] == language
                                    and r["variant"] == variant
                                ]
                            )
                            % 25
                            == 0
                        ):
                            print(
                                f"{language}/{variant}: progress {len([r for r in results if r['language'] == language and r['variant'] == variant])}/{len(sources)}",
                                flush=True,
                            )
    report = {
        "schemaVersion": 1,
        "manifestSha256": hashlib.sha256(manifest_bytes).hexdigest(),
        "artifactCount": len(results),
        "passed": sum(r["exitCode"] == 0 for r in results),
        "failures": sum(r["exitCode"] != 0 for r in results),
        "sourceDirectory": str(directory),
        "results": sorted(
            results, key=lambda r: (r["language"], r["variant"], r["problemId"])
        ),
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(
        json.dumps(
            {
                key: report[key]
                for key in ["artifactCount", "passed", "failures", "sourceDirectory"]
            }
        )
    )
    raise SystemExit(1 if report["failures"] else 0)


if __name__ == "__main__":
    main()
