"""Generate staged artifacts. Staging never makes an exercise runnable in the UI."""

import json
import sys

from algorithms01 import body
from chapter01 import SPECS
from core import EXT, HEADERS, LANGUAGES, ROOT, declaration, starter_body
from corpus01 import cases, oracle

sys.path.insert(0, str(ROOT / "scripts/code_workspace"))
from common import format_code


def generate(
    specs=SPECS,
    algorithm=body,
    corpus=cases,
    reference=oracle,
    declare=declaration,
    headers=HEADERS,
    neutral=starter_body,
    staging_name="staged",
):
    inventory = json.loads((ROOT / "ctci6/inventory.json").read_text())
    titles = {q["ref"]: q["title"] for q in inventory["questions"]}
    output = []
    staging = ROOT / "ctci6" / staging_name
    for spec in specs:
        ref = spec["ref"]
        problem_id = "ctci6_" + ref.replace(".", "_")
        fixture = corpus(spec)
        if reference(ref, spec["example"][0]) != spec["example"][1]:
            raise ValueError("Incorrect worked example: " + ref)
        path = staging / "cases" / (problem_id + ".json")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "[\n"
            + ",\n".join(json.dumps(case, separators=(",", ":")) for case in fixture)
            + "\n]\n"
        )
        entry = dict(
            spec, id=problem_id, title=titles[ref], testCount=len(fixture), languages={}
        )
        for language in LANGUAGES:
            signature, source = declare(spec, language, algorithm(ref, language))
            _, starter = declare(spec, language, neutral(spec, language))
            source = format_code(source, language)
            starter = format_code(starter, language)
            notes = dict(
                explanation=spec["why"],
                correctness=spec["correctness"],
                walkthrough=spec["walkthrough"],
                walkthroughCase=dict(
                    arguments=spec["example"][0], expected=spec["example"][1]
                ),
                timeComplexity=spec["time"],
                spaceComplexity=spec["space"],
                edgeCases=spec["edges"],
                attribution="Independently authored EPI Practice description, examples, implementation and explanation. Exercise reference: Cracking the Coding Interview, sixth edition, "
                + ref
                + ". No affiliation is implied.",
            )
            directory = staging / language
            directory.mkdir(parents=True, exist_ok=True)
            (directory / (problem_id + "." + EXT[language])).write_text(
                headers[language] + source
            )
            (directory / (problem_id + ".json")).write_text(
                json.dumps(notes, indent=2) + "\n"
            )
            entry["languages"][language] = dict(
                signature=signature, starterCode=starter, solutionCode=source
            )
        output.append(entry)
    path = staging / "catalog.json"
    path.write_text(json.dumps(output, indent=2) + "\n")
    print(
        f"Staged {len(output)} exercises and {len(output) * len(LANGUAGES)} language implementations; live publication remains pending."
    )


if __name__ == "__main__":
    generate()
