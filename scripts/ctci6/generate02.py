"""Stage chapter two while preserving the separately validated first batch."""

from algorithms02 import body
from chapter02 import SPECS
from core import LANGUAGES
from corpus02 import cases, oracle
from generate import generate
from models02 import declare, header, neutral


def generate02():
    generate(
        specs=SPECS,
        algorithm=body,
        corpus=cases,
        reference=oracle,
        declare=declare,
        headers={l: header(l) for l in LANGUAGES},
        neutral=neutral,
        staging_name="staged02",
    )


if __name__ == "__main__":
    generate02()
