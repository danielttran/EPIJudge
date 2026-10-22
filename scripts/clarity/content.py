"""Read independently reviewed authoring shards; reject overlapping ownership."""

import json
from pathlib import Path

PARTS = Path(__file__).resolve().parent / "parts"


def questions():
    result = {}
    for path in sorted(PARTS.glob("*.json")):
        if path.name.endswith("-boundaries.json"):
            continue
        document = json.loads(path.read_text(encoding="utf-8"))
        for problem_id, question in document.get("questions", {}).items():
            if problem_id in result:
                raise ValueError("Overlapping clarity ownership: " + problem_id)
            result[problem_id] = question
    return result


def apply_question(problem, reviewed=None):
    """Apply authored prose, leaving IDs, signatures, graders and corpora intact."""
    reviewed = questions() if reviewed is None else reviewed
    upper = "Id" in problem
    problem_id = problem["Id" if upper else "id"]
    if problem_id not in reviewed:
        return problem
    authored = reviewed[problem_id]
    for name in ("description", "constraints", "examples"):
        value = authored[name]
        if name == "examples" and upper:
            value = [
                {key.capitalize(): text for key, text in example.items()}
                for example in value
            ]
        problem[name.capitalize() if upper else name] = value
    return problem
