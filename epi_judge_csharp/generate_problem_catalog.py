#!/usr/bin/env python3
"""Generate the C# catalog from the language-neutral TSV test corpus."""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEST_DATA = ROOT / "test_data"
OUTPUT = Path(__file__).with_name("problem_catalog.json")


def strip_comment(type_name: str) -> str:
    return re.sub(r"\s*\[.*?]\s*", "", type_name).strip()


def main() -> None:
    problems = []
    for path in sorted(TEST_DATA.glob("*.tsv")):
        with path.open(encoding="utf-8") as source:
            signature = [strip_comment(field) for field in source.readline().rstrip("\n").split("\t")]
        if len(signature) < 2:
            raise ValueError(f"{path.name}: signature must contain an argument and result")
        problems.append({
            "id": path.stem,
            "testDataFile": path.name,
            "argumentTypes": signature[:-1],
            "resultType": signature[-1],
        })

    OUTPUT.write_text(json.dumps({"problems": problems}, indent=2) + "\n", encoding="utf-8")
    print(f"Generated {OUTPUT.relative_to(ROOT)} with {len(problems)} problems")


if __name__ == "__main__":
    main()
