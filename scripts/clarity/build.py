"""Build contracts and executable examples from reviewed question authoring sources.

This copies explicit author decisions; it does not perform semantic review or
mark ledger records reviewed. Run audit.py check and execution gates separately.
"""

import argparse
import json
from pathlib import Path

from content import questions

ROOT = Path(__file__).resolve().parents[2]


def build(check=False):
    authored = questions()
    manifest = json.loads((ROOT / "solutions/coverage.json").read_text())
    ids = {e["problemId"] for e in manifest["entries"]}
    if authored.keys() != ids:
        raise ValueError("Authoring scope differs from live question inventory")
    contracts = {}
    examples = []
    for pid, question in sorted(authored.items()):
        if set(question["contracts"]) != set(manifest["languages"]):
            raise ValueError("Incomplete language contracts: " + pid)
        contracts[pid] = question["contracts"]
        if len(question["examples"]) != len(question["exampleCases"]):
            raise ValueError("Every displayed example needs an executable case: " + pid)
        for index, case in enumerate(question["exampleCases"]):
            examples.append(
                dict(
                    problemId=pid,
                    **case,
                    reason=f"Clarity statement example {index + 1}",
                )
            )
    boundaries = [
        case
        for path in sorted((ROOT / "scripts/clarity/parts").glob("*-boundaries.json"))
        for case in json.loads(path.read_text())
    ]
    outputs = {
        "scripts/clarity/contracts.json": contracts,
        "scripts/solutions/boundaries-clarity-examples.json": examples,
        "scripts/solutions/boundaries-clarity-reviewed.json": boundaries,
    }
    for filename, value in outputs.items():
        path = ROOT / filename
        text = json.dumps(value, indent=2, ensure_ascii=False) + "\n"
        if check:
            if path.read_text() != text:
                raise ValueError("Generated clarity content is stale: " + filename)
        else:
            path.write_text(text)
    print(
        f"{len(contracts)} questions, {len(contracts) * len(manifest['languages'])} callable contracts, {len(examples)} statement examples, {len(boundaries)} reviewed boundary cases"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    build(parser.parse_args().check)
