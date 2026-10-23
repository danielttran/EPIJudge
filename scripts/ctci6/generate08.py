"""Stage the first three independently authored chapter-eight coding exercises."""

from algorithms08 import body
from chapter08 import SPECS
from core import LANGUAGES, ROOT
from corpus08 import cases, oracle
from generate import generate
from models08 import declare, header, neutral
import json


def generate08():
    # Validate every reference before replacing any passing staged artifacts.
    # A newly drafted unsupported oracle must not leave a partial catalog.
    for spec in SPECS:
        if oracle(spec["ref"], spec["example"][0]) != spec["example"][1]:
            raise ValueError("Incorrect worked example: " + spec["ref"])
        cases(spec)
    rows = []
    for spec in SPECS:
        generate(
            specs=[spec],
            algorithm=body,
            corpus=cases,
            reference=oracle,
            headers={language: header(spec["ref"], language) for language in LANGUAGES},
            declare=declare,
            neutral=neutral,
            staging_name="staged08",
        )
        rows.extend(json.loads((ROOT / "ctci6/staged08/catalog.json").read_text()))
    (ROOT / "ctci6/staged08/catalog.json").write_text(json.dumps(rows, indent=2) + "\n")


if __name__ == "__main__":
    generate08()
