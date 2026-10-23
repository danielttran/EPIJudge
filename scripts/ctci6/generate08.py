"""Stage the first three independently authored chapter-eight coding exercises."""

from algorithms08 import body
from chapter08 import SPECS
from core import HEADERS
from corpus08 import cases, oracle
from generate import generate


def generate08():
    headers = dict(HEADERS)
    headers["cpp"] += "#include <cstdint>\n"
    generate(
        specs=SPECS,
        algorithm=body,
        corpus=cases,
        reference=oracle,
        headers=headers,
        staging_name="staged08",
    )


if __name__ == "__main__":
    generate08()
