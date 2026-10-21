"""Read-only deterministic content, generated-source, provenance and asset audit."""

from __future__ import annotations

import collections
import contextlib
import hashlib
import io
import itertools
import json
import re
import xml.etree.ElementTree as ET

from corpus import oracle
from generate import generate
from interfaces import EXT, full_source, interfaces
from specs import LANGUAGES, ROOT, S


def require(value, message):
    if not value:
        raise AssertionError(message)


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def same_result(spec, args, expected):
    mode = spec["mode"]
    actual = oracle(spec, args)
    if mode == "duplicate":
        return collections.Counter(args[0])[expected] >= 2
    if mode == "set":
        return sorted(expected) == sorted(actual)
    if mode == "path":
        if actual is None:
            return expected is None
        graph, start, end = args
        return (
            isinstance(expected, list)
            and len(expected) == len(actual)
            and expected[0] == start
            and expected[-1] == end
            and all(y in graph[x] for x, y in itertools.pairwise(expected))
        )
    # Stored temperature exemplars choose one admissible scalar, not an acceptance set.
    if mode == "temperature":
        readings = []
        if not isinstance(expected, list) or len(expected) != len(args[0]):
            return False
        for method, values, result in zip(args[0], args[1], expected):
            if method == "Insert":
                readings.append(values[0])
                require(result is None, "Insert example must return null")
            elif method == "GetMode" and readings:
                counts = collections.Counter(readings)
                if type(result) is not int or counts[result] != max(counts.values()):
                    return False
            elif method == "GetMean" and readings:
                if abs(result - sum(readings) / len(readings)) > 1e-9:
                    return False
            elif (
                result != oracle(spec, [[method], [values]])[0]
                and not readings
                or method == "GetMin"
                and readings
                and result != min(readings)
                or method == "GetMax"
                and readings
                and result != max(readings)
            ):
                return False
        return True
    return expected == actual


def main():
    with contextlib.redirect_stdout(io.StringIO()):
        generate(check=True)
    catalog = load("interviewcake/catalog.json")
    metadata = load("interviewcake/provenance/source_metadata.json")
    facts = load("interviewcake/provenance/contracts.json")
    coverage = load("interviewcake/coverage.json")
    traces = load("scripts/interviewcake/walkthroughs.json")
    require(
        len(S) == len(catalog) == len(metadata) == len(facts["questions"]) == 41,
        "Exactly 41 coding entries are required",
    )
    require(len({s["id"] for s in S}) == 41, "IDs must be unique")
    require(
        [d["id"] for d in catalog]
        == [d["id"] for d in metadata]
        == [s["id"] for s in S],
        "Frozen inventory ordering changed",
    )
    require(
        [d["position"] for d in catalog] == list(range(1, 42)),
        "Positions must be contiguous",
    )
    require(
        all(m["classification"] == "csharp_coding" for m in metadata),
        "Non-coding source entries leaked",
    )
    forbidden = {
        "js-scope",
        "js-whats-wrong",
        "ticket-sales-site",
        "url-shortener",
        "two-egg-problem",
    }
    require(
        not forbidden.intersection(s["sourceId"] for s in S),
        "Excluded conceptual questions leaked",
    )
    require(
        facts["transferBatchesComplete"] == list(range(1, 8)),
        "All seven source-fact batches are required",
    )
    require(
        facts["archiveSha256"]
        == "aa6eb202de3cb17f7c034e2c86723005646908be774843da181acfd53b62d787",
        "Archive provenance changed",
    )
    provenance = (ROOT / "interviewcake/provenance/contracts.json").read_text(
        encoding="utf-8"
    )
    require(
        "/workspace/" not in provenance and "source_archive_entry" not in provenance,
        "Private archive pointers leaked",
    )
    require(
        len(coverage) == 205
        and len({(x["problemId"], x["language"]) for x in coverage}) == 205,
        "Solution coverage has omissions or duplicates",
    )
    total = 0
    for spec, definition in zip(S, catalog):
        rows = load("interviewcake/cases/" + spec["id"] + ".json")
        total += len(rows)
        require(
            len(rows) == definition["testCount"] >= 7,
            spec["id"] + " corpus count mismatch",
        )
        require(
            set(definition["starters"]) == set(LANGUAGES),
            spec["id"] + " missing typed starter",
        )
        require(
            len(definition["examples"]) == 3,
            spec["id"] + " must publish exactly three examples",
        )
        for i, (args, expected) in enumerate(spec["examplesData"]):
            require(
                same_result(spec, args, expected),
                spec["id"] + " mathematically incorrect example",
            )
            require(
                rows[i]["arguments"] == args and rows[i]["expected"] == expected,
                spec["id"] + " visible case mismatch",
            )
            require(
                json.loads(definition["examples"][i]["input"]) == args
                and json.loads(definition["examples"][i]["output"]) == expected,
                spec["id"] + " rendered example mismatch",
            )
        require(spec["id"] in traces, spec["id"] + " missing detailed trace")
        require(
            same_result(
                spec,
                traces[spec["id"]]["walkthroughCase"]["arguments"],
                traces[spec["id"]]["walkthroughCase"]["expected"],
            ),
            spec["id"] + " incorrect walkthrough case",
        )
        for lang in LANGUAGES:
            algorithms = load("scripts/interviewcake/algorithms_" + lang + ".json")
            record = algorithms[spec["id"]]
            code = (
                ROOT / "solutions" / lang / (spec["id"] + "." + EXT[lang])
            ).read_text(encoding="utf-8")
            wrong = (
                ROOT
                / "interviewcake/fixtures/incorrect"
                / lang
                / (spec["id"] + "." + EXT[lang])
            ).read_text(encoding="utf-8")
            require(
                code == full_source(spec, lang, record["code"]),
                spec["id"] + " displayed code not generated from actual algorithm",
            )
            require(
                wrong == full_source(spec, lang, record["incorrectCode"])
                and wrong != code
                and record["incorrectReason"],
                spec["id"] + " invalid negative fixture",
            )
            require(
                definition["starters"][lang]["starterCode"]
                == full_source(spec, lang, interfaces(spec, lang)["starter"]),
                spec["id"] + " stale starter",
            )
            notes = load(
                (
                    "solutions/notes/"
                    if lang == "csharp"
                    else "solutions/notes/" + lang + "/"
                )
                + spec["id"]
                + ".json"
            )
            require(
                all(
                    notes.get(k)
                    for k in [
                        "explanation",
                        "correctness",
                        "walkthrough",
                        "timeComplexity",
                        "spaceComplexity",
                        "edgeCases",
                        "attribution",
                    ]
                ),
                spec["id"] + " incomplete explanation",
            )
            require(
                "walkthroughCase" in notes,
                spec["id"] + " missing executable walkthrough",
            )
            require(len(code) < 40000, spec["id"] + " code exceeds website input limit")
    # Mathematical distinctions and added boundaries have direct executable evidence.
    indexed = {s["sourceId"]: s for s in S}
    require(
        oracle(indexed["balanced-binary-tree"], [[4, 2, None, 1, None, 0]]) is True,
        "Single-leaf chain must pass",
    )
    require(
        oracle(indexed["balanced-binary-tree"], [[4, 2, 7, 1, None, None, None, 0]])
        is False,
        "Depth-spread-two tree must fail",
    )
    require(
        oracle(indexed["rectangular-love"], [[1, 2, 6, 4], [4, 0, 5, 4]])
        == [4, 2, 3, 2],
        "Diagram rectangle math changed",
    )
    require(
        oracle(indexed["delete-node"], [[9, 4, 7, 2], 1]) == [9, 7, 2],
        "Diagram deletion math changed",
    )
    require(
        len(load("interviewcake/cases/interviewcake_cafe-order-checker.json")) == 28,
        "Missing explicit interleaving boundaries",
    )
    require(
        any(
            len(r["arguments"][0]) == 9999
            for r in load("interviewcake/cases/interviewcake_word-cloud.json")
        ),
        "Missing long-token regression",
    )
    assets = []
    ns = "{http://www.w3.org/2000/svg}"
    for path in sorted((ROOT / "interviewcake/diagrams").glob("*.svg")):
        content = path.read_bytes()
        web = ROOT / "EpiJudge.Web/wwwroot/interviewcake/diagrams" / path.name
        require(
            web.read_bytes() == content,
            "Offline asset differs from canonical " + path.name,
        )
        svg = ET.fromstring(content)
        require(
            svg.tag == ns + "svg"
            and svg.find(ns + "title") is not None
            and svg.find(ns + "desc") is not None,
            "Accessible original SVG required",
        )
        for node in svg.iter():
            require(
                node.tag not in (ns + "script", ns + "foreignObject", ns + "image"),
                "Unexpected executable/remote SVG content",
            )
            for attr, value in node.attrib.items():
                require(
                    not attr.lower().startswith("on"),
                    "Inline SVG event handler forbidden",
                )
                if attr.endswith("href"):
                    require(value.startswith("#"), "External SVG resource forbidden")
                require(
                    not re.search(r'url\(\s*["\x27]?(?:https?:|//)', value),
                    "External SVG CSS resource forbidden",
                )
        assets.append(
            {
                "path": str(path.relative_to(ROOT)),
                "sha256": hashlib.sha256(content).hexdigest(),
            }
        )
    require(len(assets) == 3, "Expected three independently authored diagrams")
    delete = ET.parse(ROOT / "interviewcake/diagrams/delete-node-aliases.svg").getroot()
    arrows = [
        p
        for group in delete.iter(ns + "g")
        if group.get("marker-end") == "url(#arrow)"
        for p in group.findall(ns + "path")
    ]
    require(len(arrows) == 6, "Every linked pointer must have its own arrowhead")
    rectangles = (
        ET.parse(ROOT / "interviewcake/diagrams/rectangle-overlap.svg")
        .getroot()
        .findall(ns + "rect")
    )
    require(
        any(
            r.get("x") == "245"
            and r.get("y") == "130"
            and r.get("width") == "135"
            and r.get("height") == "80"
            for r in rectangles
        ),
        "Rectangle drawing geometry mismatch",
    )
    print(
        json.dumps(
            {
                "questions": 41,
                "languages": 5,
                "displayedAlgorithms": 205,
                "incorrectFixtures": 205,
                "corpusCases": total,
                "diagramAssets": assets,
                "provenanceSha256": hashlib.sha256(provenance.encode()).hexdigest(),
                "status": "Content, math, provenance, reproducibility and offline asset checks passed; runtime acceptance is separate.",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
