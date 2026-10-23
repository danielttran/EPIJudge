"""Stage three established bit exercises; other chapter-five tasks remain pending."""

from algorithms05 import body
from chapter05 import SPECS
from core import HEADERS
from corpus05 import cases, oracle
from generate import generate


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
    )


if __name__ == "__main__":
    generate05()
