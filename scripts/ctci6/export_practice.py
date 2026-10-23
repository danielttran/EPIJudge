"""Export only explicitly reviewed, currently executed CtCI rows into the website.

Collection authoring can continue independently. Neither a staged file nor a
filled metadata field grants review/execution credit. Final publication remains
a separate all-collection acceptance gate.
"""

import copy
import hashlib
import inspect
import json
import sys

from core import EXT, LANGUAGES, ROOT
from corpus17 import STRUCTURED_REFS
from verify_runtime import core_match, digest, tool_versions

sys.path.insert(0, str(ROOT / "scripts/code_workspace"))
from ctci import callable_entry


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def export():
    inventory = json.loads((ROOT / "ctci6/inventory.json").read_text())
    approved = {
        row["ref"]: row
        for row in inventory["questions"]
        if row["classification"] == "coding"
    }
    runtime = {
        row["ref"]: row
        for row in json.loads((ROOT / "ctci6/runtime/catalog.json").read_text())
    }
    reports = json.loads((ROOT / "ctci6/runtime/validation.json").read_text())
    records = {row["key"]: row for row in reports["executions"]}
    reviews = {}
    for filename in (
        "review01.json",
        "review02.json",
        "review03.json",
        "review04.json",
        "review05.json",
        "review08.json",
        "review10.json",
        "review16.json",
        "review17.json",
    ):
        review = json.loads((ROOT / "ctci6" / filename).read_text())
        if set(review["languagesReviewed"]) != set(LANGUAGES):
            raise ValueError("Incomplete actual language review")
        for row in review["questions"]:
            reviews[row["ref"]] = (filename, row, review)
    if (
        not approved
        or not approved.keys() <= runtime.keys()
        or not approved.keys() <= reviews.keys()
    ):
        raise ValueError("Coding entries need explicit reviewed runtime definitions")
    tools = tool_versions()
    problems = []
    practice = []
    callables = []
    clarity = {}
    coverage = []
    topics = {
        1: "Arrays and strings",
        2: "Linked lists",
        3: "Stacks and queues",
        4: "Trees and graphs",
        5: "Bit manipulation",
        8: "Recursion and dynamic programming",
        10: "Sorting and searching",
        16: "Moderate interview problems",
        17: "Hard interview problems",
    }
    source_report = []
    for position, ref in enumerate(
        sorted(approved, key=lambda key: tuple(map(int, key.split(".")))), 1
    ):
        row = runtime[ref]
        folder = ROOT / "ctci6" / row["stagingDirectory"]
        source_entry = next(
            e
            for e in json.loads((folder / "catalog.json").read_text())
            if e["ref"] == ref
        )
        cases_path = folder / "cases" / (row["id"] + ".json")
        cases = json.loads(cases_path.read_text())
        if len(cases) != row["testCount"]:
            raise ValueError("Corpus size differs")
        if ref not in reviews:
            raise ValueError("Semantic review missing")
        contracts = {}
        for language in LANGUAGES:
            config = row["languages"][language]
            grader = hashlib.sha256((ROOT / "scripts/ctci6/corpus_line16.py").read_bytes()).hexdigest() if ref == "16.14" else hashlib.sha256((ROOT / "scripts/ctci6/corpus_names17.py").read_bytes()).hexdigest() if ref == "17.7" else hashlib.sha256((ROOT / "scripts/ctci6/corpus17.py").read_bytes()).hexdigest() if row["batch"] == 17 and ref in STRUCTURED_REFS else hashlib.sha256((ROOT / "scripts/ctci6/corpus04.py").read_bytes()).hexdigest() if row["batch"] == 4 else hashlib.sha256((ROOT / "scripts/ctci6/corpus10.py").read_bytes()).hexdigest() if row["batch"] == 10 else (
                hashlib.sha256(
                    (
                        ROOT
                        / "scripts/ctci6"
                        / (
                            "corpus02.py"
                            if row["batch"] == 2
                            else "corpus03.py"
                            if row["batch"] == 3
                            else "corpus08.py"
                        )
                    ).read_bytes()
                ).hexdigest()
                if row["batch"] in (2, 3)
                or row["batch"] == 8
                and (row["result"] in ("sets", "strings", "arrangements") or ref in ("8.2", "8.3"))
                else digest(inspect.getsource(core_match))
            )
            for variant, field, outcome in (
                ("solution", "solutionCode", "passed"),
                ("starter", "starterCode", "rejected"),
            ):
                key = ref + "/" + language + "/" + variant
                expected = digest(
                    dict(
                        source=config["prefix"] + config[field] + config["suffix"],
                        harness=config["harness"],
                        cases=cases,
                        tool=tools[language],
                        grader=grader,
                    )
                )
                if (
                    key not in records
                    or records[key]["fingerprint"] != expected
                    or records[key]["outcome"] != outcome
                    or records[key]["cases"] != len(cases)
                ):
                    raise ValueError(
                        "Missing current separate-submission execution: " + key
                    )
            notes_path = folder / language / (row["id"] + ".json")
            notes = json.loads(notes_path.read_text())
            for field in (
                "explanation",
                "correctness",
                "walkthrough",
                "timeComplexity",
                "spaceComplexity",
                "attribution",
            ):
                if not isinstance(notes.get(field), str) or not notes[field].strip():
                    raise ValueError("Missing reviewed notes")
            output = ROOT / "solutions" / language
            output.mkdir(parents=True, exist_ok=True)
            code_path = output / (row["id"] + "." + EXT[language])
            code_path.write_text(
                config["prefix"] + config["solutionCode"] + config["suffix"]
            )
            note_output = (
                ROOT
                / "solutions/notes"
                / ("" if language == "csharp" else language)
                / (row["id"] + ".json")
            )
            write(note_output, notes)
            filename = callable_entry(row, language)["filename"]
            callables.append(callable_entry(row, language))
            contracts[language] = [
                "Callable: " + config["signature"],
                *row["constraints"],
            ]
            coverage.append(
                dict(
                    problemId=row["id"],
                    collection="ctci6",
                    language=language,
                    testCount=len(cases),
                    codePath=code_path.relative_to(ROOT).as_posix(),
                    notesPath=note_output.relative_to(ROOT).as_posix(),
                    filename=filename,
                )
            )
        example = dict(
            input=json.dumps(row["example"][0], ensure_ascii=False),
            output=json.dumps(row["example"][1], ensure_ascii=False),
            explanation=source_entry["walkthrough"],
        )
        source = approved[ref]["sources"][0]["url"]
        problem = dict(
            id=row["id"],
            title=row["title"],
            topic=topics[approved[ref]["chapter"]],
            difficulty="Unrated",
            description=row["description"],
            constraints=row["constraints"],
            signature=row["languages"]["csharp"]["signature"],
            starterCode=row["languages"]["csharp"]["starterCode"],
            examples=[example],
            invocation="",
            argumentCount=len(row["example"][0]),
            testCount=len(cases),
            resultType="json",
            jsSignature=row["languages"]["javascript"]["signature"],
            jsStarterCode=row["languages"]["javascript"]["starterCode"],
            pySignature=row["languages"]["python"]["signature"],
            pyStarterCode=row["languages"]["python"]["starterCode"],
            collection="ctci6",
            position=position,
            sourceUrl=source,
            sourceAttribution="Exercise reference: Cracking the Coding Interview, sixth edition, "
            + ref
            + ". Independently authored wording, implementations, explanations and tests; no affiliation is implied.",
        )
        problems.append(problem)
        clarity[row["id"]] = dict(
            description=row["description"],
            constraints=row["constraints"],
            examples=[example],
            exampleCases=[
                dict(arguments=row["example"][0], expected=row["example"][1])
            ],
            contracts=contracts,
        )
        current = copy.deepcopy(row)
        current["stagingDirectory"] = ""
        practice.append(current)
        target = ROOT / "ctci6/cases" / (row["id"] + ".json")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(cases_path.read_bytes())
        source_report.append(
            dict(
                ref=ref,
                review=reviews[ref][0],
                sourceDirectory=row["stagingDirectory"],
                questionId=row["id"],
            )
        )
    write(ROOT / "ctci6/catalog.json", problems)
    write(ROOT / "ctci6/practice/catalog.json", practice)
    write(
        ROOT / "workspace-code/parts/ctci6.json",
        dict(schemaVersion=1, codeFormat="callable-v1", entries=callables),
    )
    write(ROOT / "scripts/clarity/parts/ctci6.json", dict(questions=clarity))
    manifest = json.loads((ROOT / "solutions/coverage.json").read_text())
    original = [row for row in manifest["entries"] if row["collection"] != "ctci6"]
    if len(original) != 334 * 5:
        raise ValueError("Existing 334-question coverage changed")
    manifest["entries"] = original + coverage
    manifest["questionCount"] = 334 + len(problems)
    manifest["collections"]["ctci6"] = len(problems)
    write(ROOT / "solutions/coverage.json", manifest)
    write(
        ROOT / "ctci6/practice/coverage.json",
        dict(
            status="verified-coding-subset-local-integration",
            questions=len(problems),
            solutionPairs=len(callables),
            collectionPublicationReady=False,
            sourceReviews=source_report,
        ),
    )
    print(
        f"Exported {len(problems)} reviewed questions and {len(callables)} executed language pairs for local integration; collection completion remains pending."
    )


if __name__ == "__main__":
    export()
