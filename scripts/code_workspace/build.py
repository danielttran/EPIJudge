"""Combine the complete, reviewed callable-code inventory; never sample coverage."""

import argparse
import hashlib
import json
from pathlib import Path

from common import ROOT

PARTS = {"epi-native": 436, "epi-managed": 654, "isolated": 580}
LANGUAGES = {"csharp", "javascript", "python", "cpp", "java"}


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def build():
    expected = json.loads(
        (ROOT / "solutions/coverage.json").read_text(encoding="utf-8")
    )
    scopes = {(row["problemId"], row["language"]) for row in expected["entries"]}
    if any(
        expected["collections"].get(key) != count
        for key, count in {"epi": 218, "blind75": 75, "interviewcake": 41}.items()
    ):
        raise ValueError("Existing collection coverage changed")
    parts = dict(PARTS)
    if expected["collections"].get("ctci6", 0):
        parts["ctci6"] = expected["collections"]["ctci6"] * len(LANGUAGES)
    expected_pairs = expected["questionCount"] * len(LANGUAGES)
    entries = []
    for name, count in parts.items():
        path = ROOT / "workspace-code/parts" / (name + ".json")
        part = json.loads(path.read_text(encoding="utf-8"))
        if (
            part.get("schemaVersion") != 1
            or part.get("codeFormat") != "callable-v1"
            or len(part.get("entries", [])) != count
        ):
            raise ValueError(
                f"Incomplete callable code part: {name}; expected {count} pairs"
            )
        entries.extend(part["entries"])
    by_scope = {(row["problemId"], row["language"]): row for row in entries}
    if (
        len(entries) != len(by_scope)
        or set(by_scope) != scopes
        or len(scopes) != expected_pairs
    ):
        raise ValueError(
            "Callable coverage must match every live question/language pair exactly"
        )
    artifacts = []
    for scope, row in sorted(by_scope.items()):
        if (
            row["language"] not in LANGUAGES
            or Path(row["filename"]).name != row["filename"]
        ):
            raise ValueError(f"Invalid callable language/filename: {scope}")
        for field in ["signature", "starterCode", "solutionCode"]:
            if not isinstance(row.get(field), str) or not row[field].strip():
                raise ValueError(f"Missing {field}: {scope}")
        for field in ["prefix", "suffix"]:
            if not isinstance(row.get(field), str):
                raise TypeError(f"Missing envelope {field}: {scope}")
        if not isinstance(row.get("references"), list):
            raise TypeError(f"Missing required-reference decision: {scope}")
        for reference in row["references"]:
            if (
                not reference.get("title")
                or not reference.get("code")
                or not isinstance(reference.get("names"), list)
            ):
                raise ValueError(f"Incomplete required reference: {scope}")
        for role in ["starter", "solution"]:
            code = row[role + "Code"]
            artifacts.append(
                {
                    "problemId": scope[0],
                    "language": scope[1],
                    "role": role,
                    "codeSha256": sha(code),
                    "lines": len(code.splitlines()),
                    "maximumLineLength": max(map(len, code.splitlines()), default=0),
                    "referenceNames": sorted(
                        {
                            name
                            for reference in row["references"]
                            for name in reference["names"]
                        }
                    ),
                    "visibleSymbols": row.get("visibleSymbols", []),
                    "hiddenSymbols": row.get("hiddenSymbols", []),
                    "removedUnrelatedSymbols": row.get("removedUnrelatedSymbols", []),
                    "sourceSha256": row.get("sourceSha256", {}),
                }
            )
    document = {
        "schemaVersion": 1,
        "codeFormat": "callable-v1",
        "entries": [by_scope[key] for key in sorted(by_scope)],
    }
    coverage = {
        "schemaVersion": 1,
        "questions": expected["questionCount"],
        "questionLanguagePairs": expected_pairs,
        "visibleArtifacts": len(artifacts),
        "roles": ["starter", "solution"],
        "collections": expected["collections"],
        "artifacts": artifacts,
    }
    if len(artifacts) != expected_pairs * 2:
        raise ValueError(
            "Every starter and solution must appear in the visible-code coverage manifest"
        )
    return document, coverage


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    document, coverage = build()
    for name, content in [("catalog.json", document), ("coverage.json", coverage)]:
        path = ROOT / "workspace-code" / name
        text = json.dumps(content, indent=2, ensure_ascii=False) + "\n"
        if args.check:
            if path.read_text(encoding="utf-8") != text:
                raise ValueError(
                    f"Callable artifact is stale: {path.relative_to(ROOT)}"
                )
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8", newline="\n")
    print(
        f"Verified {coverage['questions']} questions, {coverage['questionLanguagePairs']} callable contracts and {coverage['visibleArtifacts']} visible code artifacts."
    )


if __name__ == "__main__":
    main()
