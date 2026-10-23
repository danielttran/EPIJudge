"""Execute staged chapter-one solutions and reject unfinished starter programs.

This is authoring evidence. It does not substitute for final website harness,
whole-bank, browser, or CI acceptance checks.
"""

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

from chapter01 import SPECS
from core import EXT, LANGUAGES, ROOT
from corpus01 import cases
from generate import generate
from harness01 import source


def run(command, directory, timeout=90):
    result = subprocess.run(
        command, cwd=directory, text=True, capture_output=True, timeout=timeout
    )
    if result.returncode:
        raise RuntimeError(
            " ".join(map(str, command))
            + "\n"
            + result.stdout[-8000:]
            + result.stderr[-8000:]
        )


def execute(language, starters, rows, directory):
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "cases.json").write_text(json.dumps(rows), encoding="utf-8")
    filename = (
        "Harness." + EXT[language]
        if language in ("java", "csharp")
        else "harness." + EXT[language]
    )
    (directory / filename).write_text(source(language, starters), encoding="utf-8")
    if language == "csharp":
        (directory / "Submission.csproj").write_text(
            '<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup><OutputType>Exe</OutputType><TargetFramework>net10.0</TargetFramework><ImplicitUsings>enable</ImplicitUsings><Nullable>enable</Nullable><StartupObject>Harness</StartupObject></PropertyGroup></Project>'
        )
        (directory / "NuGet.Config").write_text(
            "<configuration><packageSources><clear /></packageSources></configuration>"
        )
        run(
            ["dotnet", "build", "Submission.csproj", "-o", "out", "--nologo", "-v:q"],
            directory,
        )
        command = ["dotnet", "out/Submission.dll"]
    elif language == "java":
        home = os.environ.get("EPI_JAVA_HOME")
        javac = str(Path(home) / "bin/javac") if home else "javac"
        java = str(Path(home) / "bin/java") if home else "java"
        run(
            [
                javac,
                "--release",
                "21",
                "-encoding",
                "UTF-8",
                "-sourcepath",
                str(ROOT / "epi_judge_java"),
                "-d",
                "classes",
                filename,
            ],
            directory,
        )
        command = [java, "-cp", "classes", "Harness"]
    elif language == "cpp":
        compiler = shutil.which("g++") or shutil.which("clang++")
        if not compiler:
            raise RuntimeError("C++ compiler unavailable")
        run(
            [
                compiler,
                "-std=c++17",
                "-O1",
                "-I",
                str(ROOT / "epi_judge_cpp"),
                filename,
                "-o",
                "harness",
            ],
            directory,
        )
        command = [str(directory / "harness")]
    else:
        command = ["python3" if language == "python" else "node", filename]
    run(command, directory, 30)
    return json.loads((directory / "results.json").read_text())


def verify():
    generate()
    started = time.monotonic()
    output = ROOT / ".epi-runs/ctci6-chapter01"
    output.mkdir(parents=True, exist_ok=True)
    rows = [dict(ref=spec["ref"], **case) for spec in SPECS for case in cases(spec)]
    evidence = []
    for language in LANGUAGES:
        for starters in (False, True):
            label = "starter" if starters else "solution"
            print(f"Executing staged {language} {label}: {len(rows)} cases", flush=True)
            actual = execute(
                language, starters, rows, output / (language + "-" + label)
            )
            if len(actual) != len(rows):
                raise AssertionError((language, label, "Incomplete execution"))
            mismatches = []
            for case, value in zip(rows, actual):
                if (
                    value.get("mutationOk") is not True
                    or type(value.get("actual")) is not type(case["expected"])
                    or value.get("actual") != case["expected"]
                ):
                    mismatches.append(
                        dict(
                            ref=case["ref"],
                            arguments=case["arguments"],
                            expected=case["expected"],
                            actual=value,
                        )
                    )
            if not starters and mismatches:
                (output / "failure.json").write_text(
                    json.dumps(mismatches[:5], indent=2)
                )
                raise AssertionError(
                    f"{language}: {len(mismatches)} solution failures; see {output / 'failure.json'}"
                )
            rejected = {m["ref"] for m in mismatches}
            if starters and rejected != {s["ref"] for s in SPECS}:
                raise AssertionError(
                    (language, "Incorrectly accepted starter", rejected)
                )
            for spec in SPECS:
                evidence.append(
                    dict(
                        ref=spec["ref"],
                        language=language,
                        variant=label,
                        cases=sum(row["ref"] == spec["ref"] for row in rows),
                        outcome="rejected" if starters else "passed",
                    )
                )
            print(
                f"Passed {language} {label} expectations across {len(SPECS)} exercises",
                flush=True,
            )
    paths = sorted((ROOT / "scripts/ctci6").glob("*.py")) + sorted(
        (ROOT / "ctci6/staged").rglob("*")
    )
    fingerprints = {
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
        sourceHashes=fingerprints,
        executions=evidence,
    )
    (ROOT / "ctci6/staged/validation.json").write_text(
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
