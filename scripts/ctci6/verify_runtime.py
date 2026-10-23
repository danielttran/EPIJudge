"""Execute separate submitted modules with resumable per-pair fingerprints.

This validates the staged submission boundary, not live HTTP registration or
completed whole-bank acceptance. Structural inventory counts are not executions.
"""

import argparse
import hashlib
import inspect
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

from core import EXT, LANGUAGES, ROOT
from corpus02 import valid_observation
from corpus03 import valid_observation as state_match
from corpus08 import valid_observation as recursive_match
from corpus10 import valid_observation as sorting_match
from corpus04 import valid_observation as graph_match
from corpus17 import STRUCTURED_REFS,valid_observation as hard_match
from corpus_line16 import valid_observation as line_match
from corpus_names17 import valid_observation as names_match
from corpus_numeric import valid_observation as numeric_match
from corpus_geometry import valid_observation as geometry_match
from corpus_bits17 import valid_observation as bits_match
from corpus_file10 import valid_observation as file_match
from corpus_rand16 import valid_observation as rand_match
from corpus_subset13 import valid_observation as subset_match
from corpus_random04 import valid_observation as random_bst_match
from corpus_random17 import valid_observation as random_match
from runtime import generate_runtime
from verify01 import execute


def core_match(case, observed):
    return (
        observed.get("mutationOk") is True
        and type(observed.get("actual")) is type(case["expected"])
        and observed.get("actual") == case["expected"]
    )


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def tool_versions():
    java = (
        str(Path(os.environ["EPI_JAVA_HOME"]) / "bin/java")
        if os.environ.get("EPI_JAVA_HOME")
        else "java"
    )
    compiler = shutil.which("g++") or shutil.which("clang++")
    commands = dict(
        csharp=["dotnet", "--version"],
        javascript=["node", "--version"],
        python=[sys.executable, "--version"],
        cpp=[compiler, "--version"],
        java=[java, "--version"],
    )
    result = {}
    for language, command in commands.items():
        completed = subprocess.run(command, text=True, capture_output=True, check=True)
        result[language] = (completed.stdout + completed.stderr).strip()
    return result


def verify(only_ref=None, only_language=None, starters=False):
    generate_runtime()
    catalog = json.loads((ROOT / "ctci6/runtime/catalog.json").read_text())
    if only_ref is not None and only_ref not in {entry["ref"] for entry in catalog}:
        raise ValueError("Unknown staged reference: " + only_ref)
    destination = ROOT / "ctci6/runtime/validation.json"
    previous = json.loads(destination.read_text()) if destination.exists() else {}
    completed = {row["key"]: row for row in previous.get("executions", [])}
    tools = tool_versions()
    grader_hashes = dict(
        subset=hashlib.sha256((ROOT / "scripts/ctci6/corpus_subset13.py").read_bytes()).hexdigest(),
        random_bst=hashlib.sha256((ROOT / "scripts/ctci6/corpus_random04.py").read_bytes()).hexdigest(),
        random=hashlib.sha256((ROOT / "scripts/ctci6/corpus_random17.py").read_bytes()).hexdigest(),
        rand=hashlib.sha256((ROOT / "scripts/ctci6/corpus_rand16.py").read_bytes()).hexdigest(),
        file=hashlib.sha256((ROOT / "scripts/ctci6/corpus_file10.py").read_bytes()).hexdigest(),
        bits=hashlib.sha256((ROOT / "scripts/ctci6/corpus_bits17.py").read_bytes()).hexdigest(),
        geometry=hashlib.sha256((ROOT / "scripts/ctci6/corpus_geometry.py").read_bytes()).hexdigest(),
        numeric=hashlib.sha256((ROOT / "scripts/ctci6/corpus_numeric.py").read_bytes()).hexdigest(),
        line=hashlib.sha256((ROOT / "scripts/ctci6/corpus_line16.py").read_bytes()).hexdigest(),
        names=hashlib.sha256((ROOT / "scripts/ctci6/corpus_names17.py").read_bytes()).hexdigest(),
        core=digest(inspect.getsource(core_match)),
        hard=hashlib.sha256((ROOT / "scripts/ctci6/corpus17.py").read_bytes()).hexdigest(),
        graphs=hashlib.sha256((ROOT / "scripts/ctci6/corpus04.py").read_bytes()).hexdigest(),
        searching=hashlib.sha256((ROOT / "scripts/ctci6/corpus10.py").read_bytes()).hexdigest(),
        combinatorial=hashlib.sha256(
            (ROOT / "scripts/ctci6/corpus08.py").read_bytes()
        ).hexdigest(),
        state=hashlib.sha256(
            (ROOT / "scripts/ctci6/corpus03.py").read_bytes()
        ).hexdigest(),
        lists=hashlib.sha256(
            (ROOT / "scripts/ctci6/corpus02.py").read_bytes()
        ).hexdigest(),
    )
    current_keys = set()
    selected_keys = set()
    started = time.monotonic()

    def save(status):
        records = [completed[key] for key in sorted(current_keys) if key in completed]
        solution = [r for r in records if r["variant"] == "solution"]
        negative = [r for r in records if r["variant"] == "starter"]
        report = dict(
            status=status,
            stage="separate-module-staging-only",
            livePublication="pending",
            expectedSolutionPairs=len(catalog) * len(LANGUAGES),
            coveredSolutionPairs=len(solution),
            rejectedStarterPairs=len(negative),
            solutionCaseExecutions=sum(r["cases"] for r in solution),
            starterCaseExecutions=sum(r["cases"] for r in negative),
            toolVersions=tools,
            executions=records,
        )
        destination.write_text(json.dumps(report, indent=2) + "\n")
        return report

    packets = []
    for entry in catalog:
        cases = json.loads(
            (
                ROOT
                / "ctci6"
                / entry["stagingDirectory"]
                / "cases"
                / (entry["id"] + ".json")
            ).read_text()
        )
        for language in LANGUAGES:
            configuration = entry["languages"][language]
            for variant in ("solution", "starter"):
                key = entry["ref"] + "/" + language + "/" + variant
                selected = (
                    (only_ref is None or entry["ref"] == only_ref)
                    and (only_language is None or language == only_language)
                    and (variant == "solution" or starters)
                )
                source = (
                    configuration["prefix"]
                    + configuration[
                        "solutionCode" if variant == "solution" else "starterCode"
                    ]
                    + configuration["suffix"]
                )
                fingerprint = digest(
                    dict(
                        source=source,
                        harness=configuration["harness"],
                        cases=cases,
                        tool=tools[language],
                        grader=grader_hashes[
                            "subset" if entry["ref"]=="13.8" else "random_bst" if entry["ref"]=="4.11" else "random" if entry["ref"] in ("17.2","17.3") else "rand" if entry["ref"]=="16.23" else "file" if entry["ref"]=="10.7" else "bits" if entry["ref"]=="17.4" else "geometry" if entry["ref"] in ("16.3","16.13") else "numeric" if entry["ref"] in ("16.26","17.20") else "line" if entry["ref"] == "16.14" else "names" if entry["ref"] == "17.7" else
                            "hard" if entry["batch"] == 17 and entry["ref"] in STRUCTURED_REFS else
                            "searching" if entry["batch"] == 10 else
                            "combinatorial"
                            if entry["batch"] == 8
                            and (entry["result"] in ("sets", "strings", "arrangements") or entry["ref"] in ("8.2", "8.3"))
                            else {
                                1: "core",
                                2: "lists",
                                3: "state",
                                4: "graphs",
                                5: "core",
                                8: "core",
                                13: "core",
                                16: "core",
                                17: "core",
                            }[entry["batch"]]
                        ],
                    )
                )
                current_keys.add(key)
                if key in completed and completed[key]["fingerprint"] != fingerprint:
                    del completed[key]
                if selected:
                    selected_keys.add(key)
                    packets.append(
                        (entry, language, variant, key, source, fingerprint, cases)
                    )
    save("running")
    for entry, language, variant, key, source, fingerprint, cases in packets:
        if key in completed:
            print(
                "REUSE "
                + key
                + " (matching submitted source, harness, cases, grader and toolchain)",
                flush=True,
            )
            continue
        print(f"RUN {key}: {len(cases)} cases", flush=True)
        directory = ROOT / ".epi-runs/ctci6-runtime" / key.replace("/", "-")
        filename = (
            "Solution." + EXT[language]
            if language in ("csharp", "java")
            else "solution." + EXT[language]
        )
        wire = [dict(ref=entry["ref"], arguments=case["arguments"]) for case in cases]
        packet_started = time.monotonic()
        try:
            values = execute(
                language,
                variant == "starter",
                wire,
                directory,
                source_builder=lambda _language, _starters: entry["languages"][
                    language
                ]["harness"],
                companion_files={filename: source},
            )
            if len(values) != len(cases):
                raise AssertionError("Incomplete submitted-module execution")
            failures = []
            elapsed = 0.0
            for case, value in zip(cases, values):
                observed = value["observation"]
                if (
                    not isinstance(value.get("elapsedMs"), (int, float))
                    or value["elapsedMs"] < 0
                ):
                    raise AssertionError("Missing per-case measured time")
                elapsed += value["elapsedMs"]
                try:
                    accepted = (
                        subset_match(entry["ref"], case, observed) if entry["ref"]=="13.8" else
                        random_bst_match(entry["ref"], case, observed) if entry["ref"]=="4.11" else
                        random_match(entry["ref"], case, observed) if entry["ref"] in ("17.2","17.3") else
                        rand_match(entry["ref"], case, observed) if entry["ref"]=="16.23" else
                        file_match(entry["ref"], case, observed) if entry["ref"]=="10.7" else
                        bits_match(entry["ref"], case, observed) if entry["ref"]=="17.4" else
                        geometry_match(entry["ref"], case, observed) if entry["ref"] in ("16.3","16.13") else
                        numeric_match(entry["ref"], case, observed) if entry["ref"] in ("16.26","17.20") else
                        line_match(entry["ref"], case, observed) if entry["ref"] == "16.14" else
                        names_match(entry["ref"], case, observed) if entry["ref"] == "17.7" else
                        hard_match(entry["ref"], case, observed) if entry["batch"] == 17 and entry["ref"] in STRUCTURED_REFS else
                        graph_match(entry["ref"], case, observed) if entry["batch"] == 4 else
                        sorting_match(entry["ref"], case, observed) if entry["batch"] == 10 else
                        recursive_match(entry["ref"], case, observed)
                        if entry["batch"] == 8
                        and (entry["result"] in ("sets", "strings", "arrangements") or entry["ref"] in ("8.2", "8.3"))
                        else core_match(case, observed)
                        if entry["batch"] in (1, 4, 5, 8, 16, 17)
                        else valid_observation(entry["ref"], case, observed)
                        if entry["batch"] == 2
                        else state_match(case, observed)
                    )
                except (KeyError, TypeError, ValueError, IndexError):
                    accepted = False
                if not accepted:
                    failures.append(
                        dict(
                            arguments=case["arguments"],
                            expected=case["expected"],
                            observation=observed,
                        )
                    )
            if (variant == "solution" and failures) or (
                variant == "starter" and not failures
            ):
                directory.mkdir(parents=True, exist_ok=True)
                (directory / "failure.json").write_text(
                    json.dumps(failures[:3], indent=2)
                )
                raise AssertionError(
                    f"Unexpected {key} result: {len(failures)} failing cases; see {directory / 'failure.json'}"
                )
            completed[key] = dict(
                key=key,
                ref=entry["ref"],
                language=language,
                variant=variant,
                fingerprint=fingerprint,
                cases=len(cases),
                measuredCaseMilliseconds=round(elapsed, 3),
                compileAndExecuteSeconds=round(time.monotonic() - packet_started, 3),
                outcome="passed" if variant == "solution" else "rejected",
            )
            save("running")
            print("PASS " + key, flush=True)
        except BaseException:
            save("failed")
            raise
    complete = all(
        entry["ref"] + "/" + language + "/solution" in completed
        for entry in catalog
        for language in LANGUAGES
    )
    negative_complete = not starters or all(
        entry["ref"] + "/" + language + "/starter" in completed
        for entry in catalog
        for language in LANGUAGES
    )
    report = save(
        "passed"
        if complete and negative_complete
        else "partial-selected-scope"
        if selected_keys <= completed.keys()
        else "incomplete"
    )
    print(
        json.dumps(
            {
                k: v
                for k, v in report.items()
                if k not in ("executions", "toolVersions")
            },
            indent=2,
        ),
        flush=True,
    )
    print(f"Invocation elapsed {time.monotonic() - started:.2f}s", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--problem")
    parser.add_argument("--language", choices=LANGUAGES)
    parser.add_argument("--starters", action="store_true")
    args = parser.parse_args()
    verify(args.problem, args.language, args.starters)
