"""Generate staged artifacts. Staging never makes an exercise runnable in the UI."""

import json

from algorithms01 import body
from chapter01 import SPECS
from core import EXT, HEADERS, LANGUAGES, ROOT, declaration, starter_body
from corpus01 import cases, oracle


def generate():
    inventory = json.loads((ROOT / "ctci6/inventory.json").read_text())
    titles = {q["ref"]: q["title"] for q in inventory["questions"]}
    output = []
    for spec in SPECS:
        ref = spec["ref"]
        problem_id = "ctci6_" + ref.replace(".", "_")
        fixture = cases(spec)
        if oracle(ref, spec["example"][0]) != spec["example"][1]:
            raise ValueError("Incorrect worked example: " + ref)
        path = ROOT / "ctci6/staged/cases" / (problem_id + ".json")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(fixture, indent=2) + "\n")
        entry = dict(
            spec, id=problem_id, title=titles[ref], testCount=len(fixture), languages={}
        )
        for language in LANGUAGES:
            signature, source = declaration(spec, language, body(ref, language))
            _, starter = declaration(spec, language, starter_body(spec, language))
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
            directory = ROOT / "ctci6/staged" / language
            directory.mkdir(parents=True, exist_ok=True)
            (directory / (problem_id + "." + EXT[language])).write_text(
                HEADERS[language] + source
            )
            (directory / (problem_id + ".json")).write_text(
                json.dumps(notes, indent=2) + "\n"
            )
            entry["languages"][language] = dict(
                signature=signature, starterCode=starter, solutionCode=source
            )
        output.append(entry)
    path = ROOT / "ctci6/staged/catalog.json"
    path.write_text(json.dumps(output, indent=2) + "\n")
    print(
        f"Staged {len(output)} exercises and {len(output) * len(LANGUAGES)} language implementations; live publication remains pending."
    )


if __name__ == "__main__":
    generate()
