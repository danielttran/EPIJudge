"""Require complete current evidence for every callable starter and solution.

This aggregation step uses only the Python standard library.  It does not run
compilers, parsers or algorithms, and never turns an unavailable check into a
pass.  A later current failure invalidates an older pass for the same scope.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
import unicodedata
from collections import Counter, defaultdict
from collections.abc import Callable
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LANGUAGES = ("csharp", "javascript", "python", "cpp", "java")
ROLES = ("starter", "solution")
COLLECTIONS = {"epi": 218, "blind75": 75, "interviewcake": 41}
FORMAT = "callable-v1"
ENTRY_LOCAL_METADATA = {
    "workspace-code/catalog.json",
    "EpiJudge.Runner/CallableCodeCatalog.cs",
}


class EvidenceError(ValueError):
    """A required acceptance scope is missing, stale or currently failing."""


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def digest_text(text: str) -> str:
    return digest_bytes(text.encode("utf-8"))


def file_sha(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def same_sha(actual, expected) -> bool:
    return (
        isinstance(actual, str)
        and isinstance(expected, str)
        and actual.upper() == expected.upper()
    )


def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise EvidenceError(
            f"Cannot read completed evidence {path}: {error}"
        ) from error


def require(condition, message):
    if not condition:
        raise EvidenceError(message)


def normalized_hashes(value) -> dict[str, str]:
    if not isinstance(value, dict) or not value:
        return {}
    if any(
        not isinstance(key, str) or not isinstance(sha, str)
        for key, sha in value.items()
    ):
        return {}
    return {key.replace("\\", "/"): sha.upper() for key, sha in value.items()}


def same_runtime_sources(
    actual, expected: dict, *, allow_entry_local_metadata=False
) -> bool:
    snapshot = normalized_hashes(actual)
    if snapshot.keys() != expected.keys():
        return False
    ignored = ENTRY_LOCAL_METADATA if allow_entry_local_metadata else set()
    return all(
        value == expected[name]
        for name, value in snapshot.items()
        if name not in ignored
    )


def older_composition_metadata(report: dict, expected: dict) -> bool:
    snapshot = normalized_hashes(report.get("sourceHashes"))
    return any(
        snapshot.get(name) != expected.get(name) for name in ENTRY_LOCAL_METADATA
    )


def path_hashes(root: Path, paths) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): file_sha(path) for path in sorted(set(paths))
    }


def runtime_hashes(root: Path) -> dict[str, str]:
    """Mirror SolutionsAudit's complete Runner/framework/runtime source set."""
    extensions = {".cs", ".csproj", ".json", ".js", ".h", ".txt"}
    paths = [
        path
        for path in (root / "EpiJudge.Runner").rglob("*")
        if path.is_file()
        and path.suffix in extensions
        and not {"obj", "bin"} & set(path.parts)
    ]
    paths += [
        path
        for path in (root / "EpiJudge.TestFramework").rglob("*.cs")
        if not {"obj", "bin"} & set(path.parts)
    ]
    for collection in ("blind75", "interviewcake"):
        paths += [
            path for path in (root / collection / "runtime").iterdir() if path.is_file()
        ]
        paths.append(root / collection / "catalog.json")
    if (root / "ctci6/catalog.json").exists():
        paths.extend(
            [
                root / "ctci6/catalog.json",
                root / "ctci6/practice/catalog.json",
                root / "ctci6/practice/coverage.json",
            ]
        )
    paths.append(root / "workspace-code/catalog.json")
    return path_hashes(root, paths)


def content_hashes(root: Path) -> dict[str, str]:
    paths = [
        root / "workspace-code/catalog.json",
        root / "workspace-code/coverage.json",
    ]
    paths += list((root / "workspace-code/parts").glob("*.json"))
    paths += list((root / "scripts/code_workspace").glob("*.py"))
    paths += list((root / "scripts/code_workspace").glob("*.json"))
    if (root / "ctci6/practice/catalog.json").exists():
        paths.extend(
            [
                root / "ctci6/catalog.json",
                root / "ctci6/practice/catalog.json",
                root / "ctci6/practice/coverage.json",
            ]
        )
    paths.append(root / "scripts/code_workspace/requirements.txt")
    return path_hashes(root, paths)


def compose(entry: dict, code: str) -> str:
    """Byte-for-byte equivalent to CallableCodeCatalog.Prepare(callable-v1)."""
    prefix = entry["prefix"]
    if prefix and not prefix.endswith("\n"):
        prefix += "\n"
    language = entry["language"]
    if language == "javascript":
        return prefix + "(() => {\n" + code + "\n" + entry["suffix"] + "\n})();\n"
    if language == "python":
        encoded = base64.b64encode(code.encode("utf-8")).decode("ascii")
        return (
            prefix
            + "\nexec(compile(__import__('base64').b64decode('"
            + encoded
            + "'), 'solution.py', 'exec'), globals())\n"
            + entry["suffix"]
        )
    if language == "java":
        code, imports = java_imports(code)
        if imports:
            insertion = prefix.find(";") + 1 if prefix.startswith("package ") else 0
            prefix = prefix[:insertion] + "\n" + imports + prefix[insertion:]
    if language in ("csharp", "cpp"):
        directive = '#line 1 "' + entry["filename"] + '"\n'
        reset = (
            "\n#line default\n"
            if language == "csharp"
            else '\n#line 1 "bank-support.cpp"\n'
        )
        return prefix + directive + code + reset + entry["suffix"]
    return prefix + code + "\n" + entry["suffix"]


def java_imports(source: str) -> tuple[str, str]:
    """Mirror the bank composer's lexical import envelope, including UTF-16 spans."""
    encoded = source.encode("utf-16-le", errors="surrogatepass")
    units = "".join(
        chr(int.from_bytes(encoded[i : i + 2], "little"))
        for i in range(0, len(encoded), 2)
    )
    position = 0
    spans = []

    def letter_or_digit(character):
        category = unicodedata.category(character)
        return category.startswith("L") or category == "Nd"

    def whitespace(character):
        return (
            unicodedata.category(character) in {"Zs", "Zl", "Zp"}
            or character in "\t\n\v\f\r\u0085"
        )

    def trivia():
        nonlocal position
        while position < len(units):
            if whitespace(units[position]):
                position += 1
            elif units.startswith("//", position):
                position += 2
                while position < len(units) and units[position] != "\n":
                    position += 1
            elif units.startswith("/*", position):
                end = units.find("*/", position + 2)
                if end < 0:
                    return False
                position = end + 2
            else:
                break
        return True

    while trivia():
        start = position
        keyword = "import"
        end = position + len(keyword)
        if not units.startswith(keyword, position) or (
            end < len(units) and (letter_or_digit(units[end]) or units[end] in "_$")
        ):
            break
        position = end
        completed = False
        while trivia() and position < len(units):
            character = units[position]
            position += 1
            if character == ";":
                spans.append((start, position))
                completed = True
                break
            if not letter_or_digit(character) and character not in "_$.*":
                break
        if not completed:
            break
    if not spans:
        return source, ""
    body = list(units)
    imports = []
    for start, end in spans:
        imports.append(units[start:end] + "\n")
        for index in range(start, end):
            if body[index] not in "\r\n":
                body[index] = " "

    def decode(value):
        return b"".join(ord(char).to_bytes(2, "little") for char in value).decode(
            "utf-16-le", errors="surrogatepass"
        )

    return decode(body), decode("".join(imports))


def integer(value) -> bool:
    return type(value) is int


def result_errors(row: dict, total: int, role: str) -> list[str]:
    result = row.get("result") or {}
    if not isinstance(result, dict):
        return ["missing judge result"]
    errors = []
    if row.get("success") is not True or row.get("failure") is not None:
        errors.append("execution reported failure")
    passed = result.get("Passed")
    if not integer(passed) or not 0 <= passed <= total:
        errors.append("invalid passed count")
    if result.get("Total") != total or not integer(result.get("Total")):
        errors.append(f"expected complete {total}-case corpus")
    status = result.get("Status")
    if role in ("solution", "correct"):
        if status != "Accepted" or passed != total:
            errors.append(f"correct algorithm was {status!r} ({passed}/{total})")
    elif role == "starter":
        if status == "Accepted":
            if passed != total:
                errors.append("starter claims Accepted without full acceptance")
        elif status in ("Wrong answer", "Runtime error"):
            if not isinstance(result.get("Cases"), list) or not result["Cases"]:
                errors.append("starter did not reach a real judge case")
            if not integer(passed) or passed >= total:
                errors.append("starter rejection has no failing case")
        else:
            errors.append(f"starter did not execute: {status!r}")
    elif role == "incorrect":
        if (
            status not in ("Wrong answer", "Runtime error")
            or not integer(passed)
            or passed >= total
        ):
            errors.append(f"incorrect fixture was not rejected by judging: {status!r}")
        if not isinstance(result.get("Cases"), list) or not result["Cases"]:
            errors.append("incorrect fixture did not reach a failing judge case")
    else:
        errors.append(f"unknown evidence role {role!r}")
    return errors


def collect_current_rows(
    paths,
    expected_keys: set,
    current_report: Callable,
    row_key: Callable,
    validate_row: Callable,
    section: str,
    label: str,
    root: Path,
):
    """Apply reports chronologically; an equal-time conflicting failure wins."""
    accepted = {}
    latest = {}
    issues = {}
    stale_reports = 0
    for path in sorted(paths, key=lambda p: (p.stat().st_mtime_ns, p.name)):
        report = read_json(path)
        require(
            isinstance(report, dict), f"{label}: malformed report object in {path.name}"
        )
        if not current_report(report):
            stale_reports += 1
            continue
        require(
            isinstance(report.get(section), list),
            f"{label}: missing {section} in {path.name}",
        )
        seen = set()
        report_sha = file_sha(path)
        stamp = path.stat().st_mtime_ns
        for index, row in enumerate(report[section]):
            require(
                isinstance(row, dict), f"{label}: malformed row {index} in {path.name}"
            )
            key = row_key(row)
            require(
                key in expected_keys, f"{label}: unexpected scope {key} in {path.name}"
            )
            require(key not in seen, f"{label}: duplicate scope {key} in {path.name}")
            seen.add(key)
            errors = validate_row(row, report)
            if errors is None:
                # A matching runtime snapshot can contain an older catalog
                # and composer. Different program bytes are stale, not a
                # failure of the current callable program.
                continue
            evidence = {
                "path": path.relative_to(root).as_posix(),
                "sha256": report_sha,
                "row": index,
            }
            previous = latest.get(key)
            # Artifact download timestamps can tie. A conflicting failure at
            # the same time must not disappear because of a filename sort.
            if not errors and previous and previous[0] == stamp and previous[1]:
                continue
            latest[key] = (stamp, bool(errors))
            if errors:
                accepted.pop(key, None)
                issues[key] = f"{path.name}: " + "; ".join(errors)
            else:
                accepted[key] = {"row": row, "evidence": evidence}
                issues.pop(key, None)
    missing = sorted(expected_keys - accepted.keys())
    if missing:
        details = [
            "/".join(key)
            + (": " + issues[key] if key in issues else ": missing current evidence")
            for key in missing[:24]
        ]
        raise EvidenceError(
            f"{label}: {len(missing)} missing/current failing scopes; "
            + " | ".join(details)
        )
    return accepted, stale_reports


def expected_collections(root: Path):
    result = dict(COLLECTIONS)
    path = root / "ctci6/catalog.json"
    if path.exists():
        rows = read_json(path)
        require(
            bool(rows)
            and all(
                row.get("collection") == "ctci6"
                and re.fullmatch(r"ctci6_[1-9]\d*_[1-9]\d*", row["id"])
                for row in rows
            )
            and len({row["id"] for row in rows}) == len(rows),
            "Invalid reviewed CtCI catalog",
        )
        result["ctci6"] = len(rows)
    return result


def inventory(root: Path):
    legacy = read_json(root / "solutions/coverage.json")
    collections = expected_collections(root)
    question_count = sum(collections.values())
    pair_count = question_count * len(LANGUAGES)
    artifact_count = pair_count * len(ROLES)
    require(
        legacy.get("questionCount") == question_count
        and legacy.get("collections") == collections,
        "Live inventory must preserve EPI218 + Blind75 75 + InterviewCake41",
    )
    require(
        set(legacy.get("languages", [])) == set(LANGUAGES),
        "Live inventory lacks five languages",
    )
    live = {(row["problemId"], row["language"]): row for row in legacy["entries"]}
    require(
        len(live) == len(legacy["entries"]) == pair_count,
        "Live inventory must enumerate all registered unique pairs",
    )
    questions = {key[0] for key in live}
    require(
        len(questions) == question_count
        and set(live) == {(pid, lang) for pid in questions for lang in LANGUAGES},
        "Live question/language product is incomplete",
    )
    counts = Counter()
    for pid in questions:
        memberships = {live[(pid, lang)]["collection"] for lang in LANGUAGES}
        require(len(memberships) == 1, f"Conflicting collection for {pid}")
        counts[next(iter(memberships))] += 1
    require(dict(counts) == collections, "Collection membership differs")
    document = read_json(root / "workspace-code/catalog.json")
    require(
        document.get("schemaVersion") == 1 and document.get("codeFormat") == FORMAT,
        "Unsupported callable catalog format",
    )
    entries = {(row["problemId"], row["language"]): row for row in document["entries"]}
    require(
        len(entries) == len(document["entries"]) == pair_count
        and entries.keys() == live.keys(),
        "Callable catalog does not cover every live pair",
    )
    coverage = read_json(root / "workspace-code/coverage.json")
    require(
        coverage.get("questions") == question_count
        and coverage.get("questionLanguagePairs") == pair_count
        and coverage.get("visibleArtifacts") == artifact_count
        and coverage.get("collections") == collections
        and set(coverage.get("roles", [])) == set(ROLES),
        "Callable coverage totals are incomplete",
    )
    artifacts = {
        (row["problemId"], row["language"], row["role"]): row
        for row in coverage["artifacts"]
    }
    expected = {(pid, lang, role) for pid, lang in entries for role in ROLES}
    require(
        len(artifacts) == len(coverage["artifacts"]) == artifact_count
        and artifacts.keys() == expected,
        "Coverage must enumerate all registered visible artifacts exactly once",
    )
    for key, artifact in artifacts.items():
        entry = entries[key[:2]]
        require(
            same_sha(artifact.get("codeSha256"), digest_text(entry[key[2] + "Code"])),
            "Coverage body is stale: " + "/".join(key),
        )
    return live, entries, artifacts


def corpus_file(root, live):
    collection, pid = live["collection"], live["problemId"]
    return root / (
        f"test_data/{pid}.tsv"
        if collection == "epi"
        else f"{collection}/cases/{pid}.json"
    )


def generator_evidence(parts: dict, generators: dict):
    require(
        generators.keys() == parts.keys(),
        "Content audit omitted a generator regeneration check",
    )
    for name, part in parts.items():
        row = generators[name]
        expected = digest_text(
            json.dumps(part["entries"], sort_keys=True, ensure_ascii=False)
        )
        require(
            row.get("success") is True
            and row.get("pairs") == len(part["entries"])
            and same_sha(row.get("savedSha256"), expected)
            and same_sha(row.get("generatedSha256"), expected),
            f"Generator regeneration is stale/failing: {name}",
        )


def content_evidence(root: Path, entries: dict, artifacts: dict):
    path = root / ".epi-runs/callable-content-audit.json"
    report = read_json(path)
    expected_hashes = content_hashes(root)
    require(
        normalized_hashes(report.get("inputHashes")) == expected_hashes,
        "Content audit input fingerprints are stale/incomplete; rerun full callable content audit",
    )
    require(
        report.get("passed") is True
        and report.get("complete") is True
        and not report.get("errors"),
        "Content/readability audit is incomplete or failing",
    )
    require(
        same_sha(
            report.get("scriptSha256"),
            expected_hashes["scripts/code_workspace/audit.py"],
        )
        and same_sha(
            report.get("catalogSha256"), expected_hashes["workspace-code/catalog.json"]
        )
        and same_sha(
            report.get("coverageSha256"),
            expected_hashes["workspace-code/coverage.json"],
        ),
        "Content audit does not fingerprint the current script/catalog/coverage",
    )
    rows = {
        (r["problemId"], r["language"], r["role"]): r
        for r in report.get("artifacts", [])
    }
    require(
        len(rows) == len(report.get("artifacts", [])) == len(artifacts)
        and rows.keys() == artifacts.keys(),
        "Content audit omitted/duplicated a visible artifact",
    )
    for key, row in rows.items():
        require(
            row.get("success") is True
            and not row.get("errors")
            and same_sha(row.get("codeSha256"), artifacts[key]["codeSha256"]),
            "Content/readability failure: " + "/".join(key),
        )
    refs = {
        (pid, lang, ref["title"], digest_text(ref["code"]))
        for (pid, lang), entry in entries.items()
        for ref in entry["references"]
    }
    reported_refs = {
        (r["problemId"], r["language"], r["title"], r["codeSha256"].upper())
        for r in report.get("references", [])
        if r.get("success") is True and not r.get("errors")
    }
    require(
        reported_refs == refs and len(report.get("references", [])) == len(refs),
        "Content audit omitted/failed a supplied-type reference",
    )
    parts = {
        p.stem: read_json(p) for p in (root / "workspace-code/parts").glob("*.json")
    }
    generators = {row["part"]: row for row in report.get("generators", [])}
    generator_evidence(parts, generators)
    return {
        "path": path.relative_to(root).as_posix(),
        "sha256": file_sha(path),
        "visibleArtifacts": len(rows),
        "referenceBlocks": len(refs),
        "sourceChanges": report.get("sourceChanges"),
        "inputHashes": expected_hashes,
    }


def harness_inventory(root: Path, entries: dict):
    path = root / ".epi-runs/solutions-harnesses.json"
    report = read_json(path)
    sources = runtime_hashes(root)
    require(
        normalized_hashes(report.get("sourceHashes")) == sources,
        "Compiled callable harness inventory is stale/incomplete; run SolutionsAudit --callable describe",
    )
    rows = {
        (row["problemId"], row["language"]): row["harnessSha256"]
        for row in report["harnesses"]
    }
    require(
        len(rows) == len(report["harnesses"]) == len(entries)
        and rows.keys() == entries.keys(),
        "Compiled harness inventory must contain every registered current pair",
    )
    return (
        sources,
        rows,
        {"path": path.relative_to(root).as_posix(), "sha256": file_sha(path)},
    )


def expected_fingerprints(root: Path, live: dict, entries: dict, harnesses: dict):
    expected = {}
    corpora = {}
    notes = {}
    for key, entry in entries.items():
        record = live[key]
        corpus = corpus_file(root, record)
        if corpus not in corpora:
            if record["collection"] == "epi":
                with corpus.open(encoding="utf-8") as source:
                    count = sum(1 for _ in source) - 1
            else:
                count = len(read_json(corpus))
            corpora[corpus] = count, file_sha(corpus)
        count, corpus_sha = corpora[corpus]
        note_path = root / record["notesPath"]
        if note_path not in notes:
            notes[note_path] = file_sha(note_path)
        require(
            integer(count) and count > 0 and count == record["testCount"],
            f"Corpus count differs for {key[0]}/{key[1]}",
        )
        for role in ROLES:
            code = entry[role + "Code"]
            expected[(*key, role)] = {
                "collection": record["collection"],
                "testCount": count,
                "codeSha256": digest_text(code),
                "composedCodeSha256": digest_text(compose(entry, code)),
                "notesSha256": notes[note_path],
                "corpusSha256": corpus_sha,
                "harnessSha256": harnesses[key],
            }
    return expected


def matrix_evidence(root, expected, source_hashes):
    def validate(row, report):
        key = row["problemId"], row["language"], row.get("role")
        target = expected[key]
        if older_composition_metadata(report, source_hashes) and any(
            not same_sha(row.get(name), target[name])
            for name in ("codeSha256", "composedCodeSha256")
        ):
            return None
        errors = result_errors(row, target["testCount"], key[2])
        if (
            row.get("displayedEmbeddedCode") is not True
            or row.get("codeFormat") != FORMAT
        ):
            errors.append("not exact displayed embedded callable code")
        if row.get("collection") != target["collection"]:
            errors.append("collection differs")
        for name in (
            "codeSha256",
            "composedCodeSha256",
            "notesSha256",
            "corpusSha256",
            "harnessSha256",
        ):
            if not same_sha(row.get(name), target[name]):
                errors.append(name + " is stale/mismatched")
        return errors

    return collect_current_rows(
        (root / ".epi-runs").glob("solutions-audit-callable-*.json"),
        set(expected),
        lambda r: same_runtime_sources(
            r.get("sourceHashes"), source_hashes, allow_entry_local_metadata=True
        ),
        lambda r: (r.get("problemId"), r.get("language"), r.get("role")),
        validate,
        "executions",
        "Full-corpus callable matrix",
        root,
    )


def normalized_case(row):
    fields = {str(key).lower(): value for key, value in row.items()}
    return {
        name: fields[name] for name in ("problemid", "arguments", "expected", "reason")
    }


def auxiliary_evidence(root, label, cases, paths, languages, expected, source_hashes):
    grouped = defaultdict(list)
    for case in cases:
        normalized = normalized_case(case)
        grouped[normalized["problemid"]].append(normalized)
    keys = {(pid, language) for pid in grouped for language in languages}
    fixture_hashes = path_hashes(root, paths)

    def validate(row, report):
        key = row["problemId"], row["language"]
        target = expected[(*key, "solution")]
        if older_composition_metadata(report, source_hashes) and any(
            not same_sha(row.get(name), target[name])
            for name in ("codeSha256", "composedCodeSha256")
        ):
            return None
        errors = result_errors(row, len(grouped[key[0]]), "solution")
        if row.get("codeFormat") != FORMAT:
            errors.append("not callable code")
        for name in ("codeSha256", "composedCodeSha256"):
            if not same_sha(row.get(name), target[name]):
                errors.append(name + " is stale/mismatched")
        try:
            if [normalized_case(case) for case in row.get("cases", [])] != grouped[
                key[0]
            ]:
                errors.append(
                    "executed boundary/walkthrough cases differ from complete current fixture"
                )
        except (KeyError, TypeError):
            errors.append("malformed executed fixture cases")
        return errors

    rows, stale = collect_current_rows(
        (root / ".epi-runs").glob(f"solutions-callable-{label}*.json"),
        keys,
        lambda r: (
            same_runtime_sources(
                r.get("sourceHashes"), source_hashes, allow_entry_local_metadata=True
            )
            and normalized_hashes(r.get("fixtureHashes")) == fixture_hashes
        ),
        lambda r: (r.get("problemId"), r.get("language")),
        validate,
        "executions",
        "Callable " + label,
        root,
    )
    return rows, {
        "questionLanguageExecutions": len(rows),
        "acceptedCaseEvaluations": sum(
            r["row"]["result"]["Total"] for r in rows.values()
        ),
        "staleReportsExcluded": stale,
    }


def archive_errors(archive: Path, row: dict, total: int, variant: str) -> list[str]:
    if not archive.is_file():
        return ["raw execution archive is missing"]
    errors = []
    if not same_sha(row.get("executionReportSha256"), file_sha(archive)):
        errors.append("raw execution archive checksum differs")
    raw = read_json(archive)
    if (
        not isinstance(raw, list)
        or len(raw) != total
        or row.get("executionReportRows") != total
        or not integer(row.get("executionReportRows"))
    ):
        errors.append("raw execution archive omitted corpus rows")
    elif any(
        not isinstance(case, dict) or "actual" not in {k.lower() for k in case}
        for case in raw
    ):
        errors.append("raw execution archive contains incomplete judge rows")
    elif variant == "correct":
        normalized = [{k.lower(): v for k, v in case.items()} for case in raw]
        if any(
            case.get("error") is not None or case.get("validationfailed") is True
            for case in normalized
        ):
            errors.append(
                "raw correct-algorithm rows contain errors/structural validation failures"
            )
    return errors


def interviewcake_evidence(root, live, entries, expected, harnesses):
    definitions = {
        row["id"]: row for row in read_json(root / "interviewcake/catalog.json")
    }
    require(
        len(definitions) == 41, "Interview Cake must contain41 runnable coding tasks"
    )
    keys = {
        (pid, lang, variant)
        for pid in definitions
        for lang in LANGUAGES
        for variant in ("starter", "correct", "incorrect")
    }
    required_headers = {
        "runnerSha256": file_sha(
            root / "EpiJudge.Runner/InterviewCakeSubmissionRunner.cs"
        ),
        "catalogSha256": file_sha(root / "interviewcake/catalog.json"),
        "callableCatalogSha256": file_sha(root / "workspace-code/catalog.json"),
    }

    def validate(row, report):
        pid, lang, variant = row["problemId"], row["language"], row["variant"]
        entry = entries[(pid, lang)]
        role = "solution" if variant == "correct" else variant
        code = (
            entry["incorrectCode"] if variant == "incorrect" else entry[role + "Code"]
        )
        total = live[(pid, lang)]["testCount"]
        errors = result_errors(row, total, variant)
        target = {
            "codeSha256": digest_text(code),
            "composedCodeSha256": digest_text(compose(entry, code)),
            "corpusSha256": expected[(pid, lang, "solution")]["corpusSha256"],
            "harnessSha256": harnesses[(pid, lang)],
        }
        if not same_sha(
            report.get("callableCatalogSha256"),
            required_headers["callableCatalogSha256"],
        ) and any(
            not same_sha(row.get(name), target[name])
            for name in ("codeSha256", "composedCodeSha256")
        ):
            return None
        if row.get("codeFormat") != FORMAT:
            errors.append("not callable fixture code")
        for name, value in target.items():
            if not same_sha(row.get(name), value):
                errors.append(name + " is stale/mismatched")
        run_id = report.get("runId")
        if (
            not isinstance(run_id, str)
            or not run_id
            or any(not (c.isalnum() or c in "-_") for c in run_id)
        ):
            return errors + ["invalid raw archive run identifier"]
        archive = (
            root
            / ".epi-runs/interviewcake-executions"
            / run_id
            / lang
            / f"{pid}-{variant}.json"
        )
        return errors + archive_errors(archive, row, total, variant)

    rows, stale = collect_current_rows(
        (root / ".epi-runs").glob("interviewcake-audit-callable-*.json"),
        keys,
        lambda r: (
            all(
                same_sha(r.get(name), value)
                for name, value in required_headers.items()
                if name != "callableCatalogSha256"
            )
            and isinstance(r.get("callableCatalogSha256"), str)
            and len(r["callableCatalogSha256"]) == 64
        ),
        lambda r: (r.get("problemId"), r.get("language"), r.get("variant")),
        validate,
        "evidence",
        "Interview Cake callable fixtures",
        root,
    )
    for (pid, lang, variant), record in rows.items():
        run_id = read_json(root / record["evidence"]["path"])["runId"]
        archive = (
            root
            / ".epi-runs/interviewcake-executions"
            / run_id
            / lang
            / f"{pid}-{variant}.json"
        )
        record["archive"] = {
            "path": archive.relative_to(root).as_posix(),
            "sha256": file_sha(archive),
            "rows": record["row"]["executionReportRows"],
        }
    return rows, {
        "questions": 41,
        "questionLanguagePairs": 205,
        "fixtureExecutions": len(rows),
        "variants": ["starter", "correct", "incorrect"],
        "archivedExecutionRows": sum(r["archive"]["rows"] for r in rows.values()),
        "staleReportsExcluded": stale,
        "failures": 0,
    }


def evidence_rows(records):
    rows = []
    for key, record in sorted(records.items()):
        source = record["row"]
        row = {
            name: source[name]
            for name in (
                "problemId",
                "language",
                "collection",
                "role",
                "variant",
                "codeFormat",
                "codeSha256",
                "composedCodeSha256",
                "notesSha256",
                "corpusSha256",
                "harnessSha256",
            )
            if name in source
        }
        result = source["result"]
        row.update(
            success=True,
            status=result["Status"],
            passed=result["Passed"],
            total=result["Total"],
            evidence=record["evidence"],
        )
        if "archive" in record:
            row["archive"] = record["archive"]
        rows.append(row)
    return rows


def accept(root: Path):
    live, entries, artifacts = inventory(root)
    content = content_evidence(root, entries, artifacts)
    sources, harnesses, harness_proof = harness_inventory(root, entries)
    expected = expected_fingerprints(root, live, entries, harnesses)
    matrix, excluded = matrix_evidence(root, expected, sources)
    paths = sorted((root / "scripts/solutions").glob("boundaries-*.json"))
    cases = [case for path in paths for case in read_json(path)]
    original_cases = [
        case
        for path in paths
        if not path.name.startswith("boundaries-clarity")
        for case in read_json(path)
    ]
    require(
        len(original_cases) == 114
        and len({row["problemId"] for row in original_cases}) == 68,
        "Additive boundaries must retain114 cases across68 questions",
    )
    boundaries, boundary_summary = auxiliary_evidence(
        root, "boundaries", cases, paths, LANGUAGES, expected, sources
    )
    walkthroughs = {}
    walkthrough_summary = {
        "questionLanguageExecutions": 0,
        "acceptedCaseEvaluations": 0,
        "staleReportsExcluded": 0,
    }
    for language in LANGUAGES:
        note_paths = [
            root / live[(pid, language)]["notesPath"]
            for pid in sorted({key[0] for key in live})
        ]
        walkthrough_cases = [
            {
                "problemId": path.stem,
                **read_json(path)["walkthroughCase"],
                "reason": "Original solution walkthrough",
            }
            for path in note_paths
        ]
        rows, counts = auxiliary_evidence(
            root,
            "walkthroughs",
            walkthrough_cases,
            note_paths,
            (language,),
            expected,
            sources,
        )
        walkthroughs.update(rows)
        for key in walkthrough_summary:
            walkthrough_summary[key] += counts[key]
    fixtures, fixture_summary = interviewcake_evidence(
        root, live, entries, expected, harnesses
    )
    summary = {
        "questions": len({key[0] for key in entries}),
        "questionLanguagePairs": len(entries),
        "solutionLanguagePairs": len(entries),
        "starterLanguagePairs": len(entries),
        "visibleArtifacts": len(artifacts),
        "languages": list(LANGUAGES),
        "collections": expected_collections(root),
        "acceptedCaseEvaluations": sum(
            record["row"]["result"]["Total"]
            for key, record in matrix.items()
            if key[2] == "solution"
        ),
        "additiveBoundaries": boundary_summary,
        "originalWalkthroughs": walkthrough_summary,
        "interviewCakeFixtures": fixture_summary,
        "catalogSha256": file_sha(root / "workspace-code/catalog.json"),
        "coverageSha256": file_sha(root / "workspace-code/coverage.json"),
        "codeFormat": FORMAT,
        "staleMatrixReportsExcluded": excluded,
        "failures": 0,
    }
    require(
        sum(row["testCount"] for row in live.values() if row["collection"] != "ctci6")
        == 2048335
        and summary["acceptedCaseEvaluations"]
        == sum(row["testCount"] for row in live.values()),
        "Original corpus must retain 2048335 evaluations and every new collection case must also pass",
    )
    require(
        boundary_summary["acceptedCaseEvaluations"] == len(cases) * len(LANGUAGES)
        and walkthrough_summary["acceptedCaseEvaluations"] == len(entries),
        "Boundary/walkthrough acceptance totals are incomplete",
    )
    require(
        fixture_summary["fixtureExecutions"] == 615
        and fixture_summary["archivedExecutionRows"] == 13245,
        "Interview Cake fixture/archive totals are incomplete",
    )
    return {
        "schemaVersion": 1,
        "summary": summary,
        "contentAudit": content,
        "compiledHarnessInventory": harness_proof,
        "sourceHashes": sources,
        "sourceFingerprintPolicy": {
            "currentRuntimeFilesRequired": sorted(set(sources) - ENTRY_LOCAL_METADATA),
            "entryLocalCompositionMetadata": sorted(ENTRY_LOCAL_METADATA),
            "rationale": "An older catalog/composer snapshot is usable only when the exact displayed and composed program hashes match the current entry. All other Runner/framework/runtime sources and harnesses must be current. Old different program bytes are excluded; later failures of the current program invalidate older passes.",
        },
        "executions": evidence_rows(matrix),
        "boundaries": evidence_rows(boundaries),
        "walkthroughs": evidence_rows(walkthroughs),
        "interviewCakeFixtures": evidence_rows(fixtures),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = accept(args.root)
    except (EvidenceError, KeyError, TypeError, OSError) as error:
        print(f"Callable acceptance incomplete: {error}")
        return 1
    target = args.output or args.root / "workspace-code/validation-results.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(target.name + ".tmp")
    temporary.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    temporary.replace(target)
    print(json.dumps(result["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
