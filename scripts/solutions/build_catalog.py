"""Build the offline solution resource from the complete live-question manifest."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LANGUAGES = {
    "csharp": ".cs",
    "javascript": ".js",
    "python": ".py",
    "cpp": ".cpp",
    "java": ".java",
}
NOTE_FIELDS = ("explanation", "timeComplexity", "spaceComplexity", "attribution")
DETAIL_FIELDS = ("correctness", "walkthrough", "edgeCases")


def build():
    manifest = json.loads(
        (ROOT / "solutions/coverage.json").read_text(encoding="utf-8")
    )
    if set(manifest["languages"]) != set(LANGUAGES):
        raise ValueError("Coverage manifest must include all five supported languages")
    entries = manifest["entries"]
    keys = {(entry["problemId"], entry["language"]) for entry in entries}
    if len(keys) != len(entries):
        raise ValueError("Duplicate question/language coverage pair")
    question_ids = {entry["problemId"] for entry in entries}
    if len(question_ids) != manifest["questionCount"] or keys != {
        (problem_id, language) for problem_id in question_ids for language in LANGUAGES
    }:
        raise ValueError("Every live question must have every supported language")
    counts = {
        collection: len(
            {
                entry["problemId"]
                for entry in entries
                if entry["collection"] == collection
            }
        )
        for collection in manifest["collections"]
    }
    if counts != manifest["collections"] or sum(counts.values()) != len(question_ids):
        raise ValueError("Collection coverage counts differ")
    rows = []
    for entry in entries:
        problem_id, language = entry["problemId"], entry["language"]
        code = (ROOT / entry["codePath"]).read_text(encoding="utf-8")
        notes = json.loads((ROOT / entry["notesPath"]).read_text(encoding="utf-8"))
        if any(
            not isinstance(notes.get(key), str) or not notes[key].strip()
            for key in NOTE_FIELDS
        ):
            raise ValueError(
                f"Incomplete solution explanation: {problem_id}/{language}"
            )
        if (
            not code.strip()
            or len(code) > 40000
            or any(
                marker in code
                for marker in (
                    "throw new NotImplementedException",
                    "raise NotImplementedError",
                )
            )
        ):
            raise ValueError(
                f"Invalid or unfinished solution source: {problem_id}/{language}"
            )
        if language == "csharp":
            if (
                any(
                    not isinstance(notes.get(key), str) or not notes[key].strip()
                    for key in ("correctness", "walkthrough")
                )
                or not isinstance(notes.get("edgeCases"), list)
                or not notes["edgeCases"]
                or any(
                    not isinstance(value, str) or not value.strip()
                    for value in notes["edgeCases"]
                )
            ):
                raise ValueError(f"Missing detailed C# explanation: {problem_id}")
            example = notes.get("walkthroughCase")
            if (
                not isinstance(example, dict)
                or not isinstance(example.get("arguments"), list)
                or "expected" not in example
            ):
                raise ValueError(
                    f"Missing executable original walkthrough: {problem_id}"
                )
        rows.append(
            dict(
                problemId=problem_id,
                collection=entry["collection"],
                language=language,
                code=code,
                **{key: notes[key] for key in NOTE_FIELDS},
                **{key: notes.get(key) for key in DETAIL_FIELDS},
            )
        )
    for language, suffix in LANGUAGES.items():
        code_ids = {
            path.stem for path in (ROOT / "solutions" / language).glob("*" + suffix)
        }
        note_directory = (
            ROOT / "solutions/notes" / language
            if language != "csharp"
            else ROOT / "solutions/notes"
        )
        note_ids = {path.stem for path in note_directory.glob("*.json")}
        if code_ids != question_ids or note_ids != question_ids:
            raise ValueError(
                f"Unexpected or missing {language} files: code={code_ids.symmetric_difference(question_ids)}, notes={note_ids.symmetric_difference(question_ids)}"
            )
    output = json.dumps(rows, indent=2, ensure_ascii=False) + "\n"
    (ROOT / "solutions/catalog.json").write_text(output, encoding="utf-8", newline="\n")
    print(
        f"Built {len(rows)} offline solutions for {len(question_ids)} questions; SHA256={hashlib.sha256(output.encode()).hexdigest()}"
    )


if __name__ == "__main__":
    build()
