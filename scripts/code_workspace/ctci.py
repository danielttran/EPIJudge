"""Regenerate CtCI callable metadata from the reviewed practice snapshot."""

import hashlib
import json
import re
from functools import lru_cache
from common import ROOT, format_code

EXT = dict(csharp="cs", javascript="js", python="py", cpp="cpp", java="java")


@lru_cache(None)
def reference_code(code, language):
    return format_code(code, language)


def callable_entry(row, language):
    source = row["languages"][language]
    names = [
        name
        for name in ("LinkedListNode", "IntStack", "Animal", "BankError", "Listy", "TreeNode", "DepthLink", "BitArray", "BiNode", "NumberFile", "Rand5Source")
        if re.search(r"\b" + name + r"\b", source["reference"])
    ]
    references = (
        [
            dict(
                title="Required callable model APIs",
                code=reference_code(source["reference"], language),
                names=names,
            )
        ]
        if source["reference"].strip()
        else []
    )
    sha = lambda code: hashlib.sha256(code.encode()).hexdigest()
    root = (
        row["method"]
        if row["result"] == "state" or language in ("python", "javascript")
        else "Solution"
    )
    return dict(
        problemId=row["id"],
        language=language,
        filename=(
            row["method"] + ".java"
            if language == "java" and row["result"] == "state"
            else ("Solution." if language in ("csharp", "java") else "solution.")
            + EXT[language]
        ),
        signature=source["signature"],
        starterCode=source["starterCode"],
        solutionCode=source["solutionCode"],
        prefix=source["prefix"],
        suffix=source["suffix"],
        references=references,
        visibleSymbols=[root],
        hiddenSymbols=names,
        removedUnrelatedSymbols=[],
        sourcePaths=[
            "ctci6/practice/catalog.json",
            f"solutions/{language}/{row['id']}.{EXT[language]}",
        ],
        sourceSha256=dict(
            starter=sha(source["prefix"] + source["starterCode"] + source["suffix"]),
            solution=sha(source["prefix"] + source["solutionCode"] + source["suffix"]),
        ),
    )


def build_entries():
    rows = json.loads((ROOT / "ctci6/practice/catalog.json").read_text())
    return [callable_entry(row, language) for row in rows for language in EXT]


if __name__ == "__main__":
    target = ROOT / "workspace-code/parts/ctci6.json"
    target.write_text(
        json.dumps(
            dict(schemaVersion=1, codeFormat="callable-v1", entries=build_entries()),
            indent=2,
            ensure_ascii=False,
        )
        + "\n"
    )
