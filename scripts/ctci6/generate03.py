"""Stage stack/queue implementations without publishing incomplete content."""

from algorithms03 import body
from chapter03 import SPECS
from core import LANGUAGES
from corpus03 import cases, oracle
from generate import generate
from models03 import declare, header, neutral


def generate03():
    # Each question has its own required API; use the common artifact writer for
    # one-question groups, then combine only the explicitly authored rows.
    import json
    from core import ROOT

    rows = []
    for spec in SPECS:
        generate(
            specs=[spec],
            algorithm=body,
            corpus=cases,
            reference=oracle,
            declare=declare,
            headers={language: header(spec["ref"], language) for language in LANGUAGES},
            neutral=neutral,
            staging_name="staged03",
        )
        rows.extend(json.loads((ROOT / "ctci6/staged03/catalog.json").read_text()))
    (ROOT / "ctci6/staged03/catalog.json").write_text(json.dumps(rows, indent=2) + "\n")


if __name__ == "__main__":
    generate03()
