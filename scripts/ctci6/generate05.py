"""Stage the seven established bit coding exercises; Debugger is conceptual."""

from algorithms05 import body
from chapter05 import SPECS
from core import HEADERS
from corpus05 import cases, oracle
from generate import generate
from models05 import declare, neutral


def generate05():
    headers = dict(HEADERS)
    headers["cpp"] += "#include <cstdint>\n"
    generate(
        specs=SPECS,
        algorithm=body,
        corpus=cases,
        reference=oracle,
        headers=headers,
        staging_name="staged05",
        declare=declare,
        neutral=neutral,
    )


if __name__ == "__main__":
    generate05()
