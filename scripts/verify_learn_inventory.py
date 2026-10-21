"""Audit every existing local reading, its provenance, and related practice links."""

import hashlib
import json
import math
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]


def audit(root=ROOT):
    folder = root / "epijudge.client/src/reading"
    lessons = json.loads((folder / "content/lessons.json").read_text(encoding="utf-8"))
    inventory = json.loads((folder / "learnInventory.json").read_text(encoding="utf-8"))
    articles = inventory["articles"]
    ids = [lesson["id"] for lesson in lessons]
    assert len(ids) == len(set(ids)) == 12, "Original reading inventory changed"
    assert [item["id"] for item in articles] == ids, (
        "Lost, duplicate, or reordered reading"
    )
    assert {path.stem for path in (folder / "content").glob("*.md")} == set(ids)
    catalogs = [
        json.loads((root / path).read_text(encoding="utf-8"))
        for path in [
            "EpiJudge.Runner/catalog.json",
            "blind75/catalog.json",
            "interviewcake/catalog.json",
        ]
    ]
    # Three curated EPI entries live in ProblemCatalog.cs rather than its JSON.
    assert [len(items) for items in catalogs] == [215, 75, 41]
    solutions = json.loads(
        (root / "solutions/catalog.json").read_text(encoding="utf-8")
    )
    current = [item for item in solutions if item["language"] == "csharp"]
    assert {
        name: sum(item["collection"] == name for item in current)
        for name in ["epi", "blind75", "interviewcake"]
    } == {"epi": 218, "blind75": 75, "interviewcake": 41}
    problems = {item["problemId"] for item in current}
    assert {
        item.get("Id", item.get("id")) for items in catalogs for item in items
    } <= problems
    assert len(problems) == 334
    topics = {}
    relations = 0
    for lesson, article in zip(lessons, articles, strict=True):
        body = (folder / "content" / (article["id"] + ".md")).read_bytes()
        assert hashlib.sha256(body).hexdigest() == article["bodySha256"], article["id"]
        assert article["title"] == lesson["title"]
        assert article["originalTopic"] == lesson["topic"]
        assert article["sourceUrls"] == lesson["sources"]
        assert (
            article["sourceId"] == "other"
            and article["sourceLabel"] == "EPI study companion"
        )
        words = len(body.decode().split())
        assert article["wordCount"] == words
        assert article["readingMinutes"] == max(1, math.ceil(words / 200))
        assert article["description"] == body.decode().splitlines()[0]
        assert article["topicId"] in ["foundations", "trees-graphs", "system-design"]
        topics[article["topicId"]] = topics.get(article["topicId"], 0) + 1
        headings = re.findall(r"^## (.+)$", body.decode(), re.MULTILINE)
        assert len(headings) == len(set(headings)) == 4
        for source in article["sourceUrls"]:
            url = urlparse(source)
            assert url.scheme == "https" and url.netloc
        assert not re.search(r"!\[|<script|<iframe", body.decode(), re.IGNORECASE)
        related_ids = [item["id"] for item in article["relatedProblems"]]
        assert len(related_ids) == len(set(related_ids))
        for item in article["relatedProblems"]:
            assert item["id"] in problems and item["reason"].strip()
            relations += 1
    assert topics == {"trees-graphs": 2, "foundations": 4, "system-design": 6}
    return {
        "passed": True,
        "articles": 12,
        "topics": topics,
        "codingQuestions": 334,
        "relatedLinks": relations,
        "missingInterviewCakeArticles": True,
        "newExternalArticleImports": 0,
        "originalReadingIdsPreserved": True,
    }


if __name__ == "__main__":
    result = audit()
    target = ROOT / ".epi-runs/learn-inventory-audit.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
