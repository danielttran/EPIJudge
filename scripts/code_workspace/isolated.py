"""Generate callable-only views for the independently authored collections.

Only checked-in bank sources are parsed. Legacy submissions and user drafts are
never passed through this generator. The explicit prefix/suffix envelope lets
the existing judge execute new callable code without changing model identity.
"""

from __future__ import annotations

import argparse
import ast
import collections
import copy
import hashlib
import json
import os
import sys
import tempfile
from functools import cache
from pathlib import Path

from common import ROOT, format_code, parse, text_of

LANGUAGES = ("csharp", "javascript", "python", "cpp", "java")
EXTENSIONS = {
    "csharp": "cs",
    "javascript": "js",
    "python": "py",
    "cpp": "cpp",
    "java": "java",
}
BLIND_MODELS = ("ListNode", "TreeNode", "Node")
CAKE_MODELS = (
    "LinkedListNode",
    "BinaryTreeNode",
    "GraphNode",
    "Meeting",
    "Rectangle",
    "CakeType",
    "FilePaths",
    "InfinityException",
    "RandomSource",
)
PY_HELPERS = ("word_exists", "component_count")
IMPORT_NODES = {
    "using_directive",
    "import_declaration",
    "preproc_include",
    "using_declaration",
}
IDENTIFIERS = {
    "identifier",
    "type_identifier",
    "namespace_identifier",
    "property_identifier",
}


def digest(source: str) -> str:
    return hashlib.sha256(source.encode("utf-8")).hexdigest()


@cache
def formatted(source: str, language: str) -> str:
    return format_code(source, language)


def children(node):
    yield node
    for child in node.named_children:
        yield from children(child)


def literal_assignment(path: Path, name: str):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == name for t in node.targets
        ):
            return ast.literal_eval(node.value)
    raise ValueError(f"Missing literal {name} in {path}")


def ts_name(node, source: str) -> str | None:
    name = node.child_by_field_name("name")
    if name is not None:
        return text_of(name, source)
    if node.type in {"lexical_declaration", "variable_declaration"}:
        declaration = next(
            (c for c in node.named_children if c.type == "variable_declarator"), None
        )
        return ts_name(declaration, source) if declaration is not None else None
    if node.type == "function_definition":
        declarator = node.child_by_field_name("declarator")
        while declarator is not None:
            if declarator.type in {"identifier", "field_identifier", "operator_name"}:
                return text_of(declarator, source)
            declarator = declarator.child_by_field_name("declarator")
    return None


def ts_segment(node, source: str, language: str) -> str:
    value = text_of(node, source)
    if language == "cpp" and node.type in {"class_specifier", "struct_specifier"}:
        # The C++ grammar excludes the declaration's trailing semicolon.
        value += ";"
    return value


def renamed(code: str, language: str, old: str, new: str) -> str:
    data = code.encode("utf-8")
    tree = parse(code, language)
    replacements = [
        (n.start_byte, n.end_byte)
        for n in children(tree.root_node)
        if n.type in IDENTIFIERS and text_of(n, data) == old
    ]
    for start, end in sorted(replacements, reverse=True):
        data = data[:start] + new.encode("utf-8") + data[end:]
    return data.decode("utf-8")


def helper_name(spec: dict, collection: str) -> str:
    kinds = {p["type"] for p in spec["params"]} | {spec["result"]}
    if kinds & {"list", "lists", "node"}:
        return "ListAlgorithms"
    if "graph" in kinds:
        return "GraphAlgorithms"
    return "TreeAlgorithms"


def ts_calls(code: str, language: str, *, external: bool) -> set[str]:
    """Resolve helper references, including callbacks and recursive calls.

    A qualified method passed as a value (for example flatMap(Probe.nodes)) is
    just as necessary as a direct invocation. Inspect syntax references rather
    than only call-expression callees.
    """
    tree = parse(code, language)
    result = set()
    for node in children(tree.root_node):
        if language == "java" and node.type == "method_invocation":
            name = node.child_by_field_name("name")
            obj = node.child_by_field_name("object")
            qualifier = text_of(obj, code) if obj is not None else ""
            if name is not None and (
                qualifier == "Probe" or (not external and not qualifier)
            ):
                result.add(text_of(name, code))
        elif language == "java" and node.type == "method_reference":
            named = node.named_children
            if len(named) >= 2 and text_of(named[0], code) == "Probe":
                result.add(text_of(named[-1], code))
        elif language == "javascript" and node.type == "member_expression":
            obj = node.child_by_field_name("object")
            prop = node.child_by_field_name("property")
            if obj is not None and prop is not None:
                qualifier = text_of(obj, code)
                if qualifier == "Probe" or (not external and qualifier == "this"):
                    result.add(text_of(prop, code))
        elif language == "cpp" and node.type == "qualified_identifier":
            scope = node.child_by_field_name("scope")
            name = node.child_by_field_name("name")
            if (
                scope is not None
                and name is not None
                and text_of(scope, code) == "Probe"
            ):
                result.add(text_of(name, code))
        elif language == "cpp" and not external and node.type == "call_expression":
            function = node.child_by_field_name("function")
            if function is not None and function.type == "identifier":
                result.add(text_of(function, code))
    return result


def probe_members(node, source: str, language: str):
    if language == "javascript":
        declaration = next(
            c for c in node.named_children if c.type == "variable_declarator"
        )
        body = declaration.child_by_field_name("value")
        assert body is not None and body.type == "object"
        return [c for c in body.named_children if c.type == "method_definition"]
    body = node.child_by_field_name("body")
    assert body is not None, (language, node.type)
    expected = "function_definition" if language == "cpp" else "method_declaration"
    return [c for c in body.named_children if c.type == expected]


def prune_probe(node, source: str, language: str, entry_code: str, replacement: str):
    members = probe_members(node, source, language)
    by_name = collections.defaultdict(list)
    for member in members:
        name = ts_name(member, source)
        assert name, (language, member.type, text_of(member, source)[:80])
        by_name[name].append(member)
    needed = ts_calls(entry_code, language, external=True) & by_name.keys()
    pending = list(needed)
    while pending:
        name = pending.pop()
        for member in by_name[name]:
            for dependency in (
                ts_calls(text_of(member, source), language, external=False)
                & by_name.keys()
            ):
                if dependency not in needed:
                    needed.add(dependency)
                    pending.append(dependency)
    removed = ["Probe." + name for name in by_name if name not in needed]
    if not needed:
        return "", [], removed
    selected = [text_of(m, source) for m in members if ts_name(m, source) in needed]
    if language == "javascript":
        code = "const Probe = {\n" + ",\n".join(selected) + "\n};\n"
    elif language == "cpp":
        code = "namespace Probe {\n" + "\n\n".join(selected) + "\n}\n"
    else:
        code = "class Probe {\n" + "\n\n".join(selected) + "\n}\n"
    code = renamed(code, language, "Probe", replacement)
    return (
        code,
        [replacement] + [replacement + "." + name for name in sorted(needed)],
        removed,
    )


def python_split(source: str, models: tuple[str, ...], replacement: str):
    tree = ast.parse(source)
    imports = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom))]
    definitions = [
        n
        for n in tree.body
        if isinstance(n, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    other = [
        n
        for n in tree.body
        if n not in imports
        and n not in definitions
        and not (
            isinstance(n, ast.Expr)
            and isinstance(n.value, ast.Constant)
            and isinstance(n.value.value, str)
        )
    ]
    assert not other, [(type(n).__name__, ast.unparse(n)[:80]) for n in other]
    roots = [n for n in definitions if n.name not in {*models, "Probe", *PY_HELPERS}]
    probe = next((n for n in definitions if n.name == "Probe"), None)
    helpers = {n.name: n for n in definitions if n.name in PY_HELPERS}
    names = {
        n.id
        for root in roots
        for n in ast.walk(root)
        if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)
    }
    selected_helpers = []
    selected_symbols = [n.name for n in roots]
    removed = []
    if probe is not None:
        methods = {
            n.name: n
            for n in probe.body
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        needed = {
            n.attr
            for root in roots
            for n in ast.walk(root)
            if isinstance(n, ast.Attribute)
            and isinstance(n.value, ast.Name)
            and n.value.id == "Probe"
        } & methods.keys()
        pending = list(needed)
        while pending:
            method = methods[pending.pop()]
            for n in ast.walk(method):
                if (
                    isinstance(n, ast.Attribute)
                    and isinstance(n.value, ast.Name)
                    and n.value.id == "Probe"
                    and n.attr in methods
                    and n.attr not in needed
                ):
                    needed.add(n.attr)
                    pending.append(n.attr)
        removed.extend("Probe." + name for name in methods if name not in needed)
        if needed:
            selected = copy.deepcopy(probe)
            selected.body = [
                m
                for m in selected.body
                if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef))
                and m.name in needed
            ]
            selected.name = replacement
            selected_helpers.append(selected)
            selected_symbols += [replacement] + [
                replacement + "." + n for n in sorted(needed)
            ]
    needed_helpers = names & helpers.keys()
    pending = list(needed_helpers)
    while pending:
        for n in ast.walk(helpers[pending.pop()]):
            if (
                isinstance(n, ast.Name)
                and isinstance(n.ctx, ast.Load)
                and n.id in helpers
                and n.id not in needed_helpers
            ):
                needed_helpers.add(n.id)
                pending.append(n.id)
    selected_helpers.extend(
        copy.deepcopy(n) for name, n in helpers.items() if name in needed_helpers
    )
    selected_symbols += sorted(needed_helpers)
    removed += sorted(helpers.keys() - needed_helpers)
    body = ast.Module(body=copy.deepcopy(roots) + selected_helpers, type_ignores=[])

    class RenameProbe(ast.NodeTransformer):
        def visit_Name(self, node):
            if node.id == "Probe":
                node.id = replacement
            return node

    body = ast.fix_missing_locations(RenameProbe().visit(body))
    code = ast.unparse(body) + "\n"
    import_code = [
        ast.unparse(n)
        for n in imports
        if not isinstance(n, ast.ImportFrom) or n.module != "__future__"
    ]
    return code, import_code, selected_symbols, removed


def ts_split(source: str, language: str, models: tuple[str, ...], replacement: str):
    tree = parse(source, language)
    assert not tree.root_node.has_error, (language, "Invalid owned source")
    imports = []
    roots = []
    symbols = []
    probe = None
    for node in tree.root_node.named_children:
        name = ts_name(node, source)
        if node.type in IMPORT_NODES:
            imports.append(text_of(node, source))
        elif name in models or node.type in {
            "comment",
            "line_comment",
            "block_comment",
        }:
            continue
        elif name == "Probe":
            probe = node
        elif (
            node.type == "expression_statement"
            and text_of(node, source).lstrip().startswith("module.exports")
            or (
                language == "javascript"
                and node.type == "expression_statement"
                and text_of(node, source) in {'"use strict";', "'use strict';"}
            )
        ):
            continue
        elif (
            language == "javascript"
            and node.type == "lexical_declaration"
            and name in {"fs", "path"}
        ):
            # Interview Cake's fixed standard-library imports live in support.
            continue
        elif node.type in {
            "class_declaration",
            "class_specifier",
            "function_declaration",
            "struct_specifier",
        }:
            assert name, (language, node.type)
            roots.append(ts_segment(node, source, language))
            symbols.append(name)
        else:
            raise ValueError(
                f"Unclassified owned {language} node {node.type}: {text_of(node, source)[:100]}"
            )
    root_code = "\n\n".join(roots) + "\n"
    removed = []
    if probe is not None:
        helper, helper_symbols, removed = prune_probe(
            probe, source, language, root_code, replacement
        )
        if helper:
            # C++ class inline method names must resolve at their definitions.
            root_code = (
                helper + "\n" + root_code
                if language == "cpp"
                else root_code + "\n" + helper
            )
            root_code = renamed(root_code, language, "Probe", replacement)
            symbols += helper_symbols
    return root_code, imports, symbols, removed


def split(source: str, language: str, models: tuple[str, ...], replacement: str):
    return (
        python_split(source, models, replacement)
        if language == "python"
        else ts_split(source, language, models, replacement)
    )


def header_parts(header: str, language: str, models: tuple[str, ...]):
    """Keep canonical support whole but index exact model declarations for docs."""
    if language == "python":
        tree = ast.parse(header)
        refs = {}
        for node in tree.body:
            if isinstance(node, ast.ClassDef) and node.name in models:
                refs[node.name] = (
                    ast.unparse(ast.Module(body=[node], type_ignores=[])) + "\n"
                )
        imports = [
            ast.unparse(n)
            for n in tree.body
            if isinstance(n, (ast.Import, ast.ImportFrom))
        ]
        support = (
            ast.unparse(
                ast.Module(
                    body=[
                        n
                        for n in tree.body
                        if not isinstance(n, (ast.Import, ast.ImportFrom))
                    ],
                    type_ignores=[],
                )
            )
            + "\n"
        )
        return imports, support, refs
    tree = parse(header, language)
    assert not tree.root_node.has_error, (language, "Invalid canonical support")
    refs = {}
    imports = []
    support = []
    for node in tree.root_node.named_children:
        name = ts_name(node, header)
        if node.type in IMPORT_NODES:
            imports.append(text_of(node, header))
        elif node.type not in {"comment", "line_comment", "block_comment"}:
            support.append(ts_segment(node, header, language))
            if name in models:
                refs[name] = ts_segment(node, header, language)
    assert set(refs) == set(models), (language, set(refs), set(models))
    return imports, "\n\n".join(support) + "\n", refs


def support_envelope(
    header: str, imports: list[str], language: str, models: tuple[str, ...]
):
    canonical_imports, support, _ = header_parts(header, language, models)
    unique = {}
    for item in canonical_imports + imports:
        if (
            language == "python"
            and item.startswith("from __future__")
            and any(x.startswith("from __future__") for x in unique.values())
        ):
            continue
        unique.setdefault("".join(item.split()), item.rstrip())
    directives = "\n".join(unique.values())
    if language in {"csharp", "java"}:
        # User imports must precede all declarations. These languages resolve
        # later type declarations, so supplied models belong after user code.
        return formatted(directives, language) + "\n", "\n" + formatted(
            support, language
        )
    return formatted(directives + "\n\n" + support, language) + "\n", ""


def support_prefix(
    header: str, imports: list[str], language: str, models: tuple[str, ...]
):
    return support_envelope(header, imports, language, models)[0]


def required_models(spec: dict, collection: str) -> list[str]:
    kinds = {p["type"] for p in spec["params"]} | {spec["result"]}
    if collection == "blind75":
        required = set()
        if kinds & {"list", "lists"}:
            required.add("ListNode")
        if kinds & {"tree", "tree_node"}:
            required.add("TreeNode")
        if "graph" in kinds:
            required.add("Node")
        return [name for name in BLIND_MODELS if name in required]
    mapping = {
        "tree": "BinaryTreeNode",
        "list": "LinkedListNode",
        "node": "LinkedListNode",
        "graph": "GraphNode",
        "meetings": "Meeting",
        "rect": "Rectangle",
        "cakes": "CakeType",
        "pairs": "FilePaths",
    }
    required = {mapping[kind] for kind in kinds if kind in mapping}
    if spec["mode"] in {"shuffle", "rand5", "rand7"}:
        required.add("RandomSource")
    if spec["sourceId"] == "cake-thief":
        required.add("InfinityException")
    return [name for name in CAKE_MODELS if name in required]


def random_reference(spec: dict, language: str) -> str:
    """Document only the allowed primitive, not the private injection mechanism."""
    method = {"shuffle": "GetRandom", "rand5": "Rand7", "rand7": "Rand5"}[spec["mode"]]
    params = (
        {
            "csharp": "int lower, int upper",
            "java": "int lower, int upper",
            "cpp": "int lower, int upper",
            "python": "lower: int, upper: int",
            "javascript": "lower, upper",
        }[language]
        if spec["mode"] == "shuffle"
        else ""
    )
    contract = (
        "Uniform independent integer, inclusive bounds."
        if spec["mode"] == "shuffle"
        else "Uniform independent integer in 1.."
        + ("7." if spec["mode"] == "rand5" else "5.")
    )
    if language == "csharp":
        code = f"// Provided API: {contract}\npublic static class RandomSource {{ public static extern int {method}({params}); }}\n"
    elif language == "java":
        code = f"// Provided API: {contract}\nclass RandomSource {{ public static native int {method}({params}); }}\n"
    elif language == "cpp":
        code = f"// Provided API: {contract}\nstruct RandomSource {{ static int {method}({params}); }};\n"
    elif language == "javascript":
        code = f"// Provided API: {contract}\nclass RandomSource {{ static {method}({params}) {{ /* supplied by the judge */ }} }}\n"
    else:
        code = f'class RandomSource:\n    @staticmethod\n    def {method}({params}) -> int:\n        """Provided API: {contract}"""\n        ...\n'
    return formatted(code, language)


def references_for(spec: dict, collection: str, language: str, header: str):
    models = BLIND_MODELS if collection == "blind75" else CAKE_MODELS
    _, _, declarations = header_parts(header, language, models)
    result = []
    for name in required_models(spec, collection):
        code = (
            random_reference(spec, language)
            if name == "RandomSource"
            else formatted(declarations[name], language)
        )
        result.append({"title": "Provided " + name, "code": code, "names": [name]})
    return result


def validate_entry(entry: dict, collection: str, spec: dict):
    language = entry["language"]
    models = BLIND_MODELS if collection == "blind75" else CAKE_MODELS
    expected = set(required_models(spec, collection))
    actual = {name for reference in entry["references"] for name in reference["names"]}
    assert actual == expected, (entry["problemId"], language, expected, actual)
    if language in {"csharp", "java"}:
        assert all(
            node.type in IMPORT_NODES
            for node in parse(entry["prefix"], language).root_node.named_children
        ), (entry["problemId"], language, "Declarations before user imports")
    for key in (
        "starterCode",
        "solutionCode",
        *(("incorrectCode",) if "incorrectCode" in entry else ()),
    ):
        code = entry[key]
        if language == "python":
            tree = ast.parse(code)
            top_names = {
                n.name
                for n in tree.body
                if isinstance(n, (ast.ClassDef, ast.FunctionDef))
            }
        else:
            tree = parse(code, language)
            assert not tree.root_node.has_error, (
                entry["problemId"],
                language,
                key,
                "parse error",
            )
            top_names = {ts_name(n, code) for n in tree.root_node.named_children}
        assert not (top_names & set(models)), (
            entry["problemId"],
            language,
            key,
            top_names & set(models),
        )
        assert "module.exports" not in code and "Probe" not in code, (
            entry["problemId"],
            language,
            key,
        )
        for marker in (
            "GenericTestMain",
            "runFromAnnotations",
            "cases.json",
            "results.json",
            "int main(",
            "static void main(",
        ):
            assert marker not in code, (entry["problemId"], language, key, marker)
        composed = entry["prefix"] + code + entry["suffix"]
        if language == "python":
            ast.parse(composed)
        else:
            assert not parse(composed, language).root_node.has_error, (
                entry["problemId"],
                language,
                key,
                "Composed program parse error",
            )
    # No old helper algorithm may survive unnoticed in the composed program.
    for name in entry["removedUnrelatedSymbols"]:
        if name.startswith("Probe."):
            assert (
                "Probe" not in entry["prefix"] + entry["solutionCode"] + entry["suffix"]
            )
    assert set(entry["hiddenSymbols"]) == set(models)


def build_entries() -> list[dict]:
    headers = {
        "blind75": literal_assignment(ROOT / "scripts/blind75/generate.py", "HEADERS"),
        "interviewcake": literal_assignment(
            ROOT / "scripts/interviewcake/banktypes.py", "HEADER"
        ),
    }
    entries = []
    for collection in ("blind75", "interviewcake"):
        catalog_path = ROOT / collection / "catalog.json"
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        incorrect_sources = (
            {
                language: json.loads(
                    (
                        ROOT
                        / "scripts/interviewcake"
                        / ("algorithms_" + language + ".json")
                    ).read_text(encoding="utf-8")
                )
                for language in LANGUAGES
            }
            if collection == "interviewcake"
            else {}
        )
        assert len(catalog) == (75 if collection == "blind75" else 41)
        models = BLIND_MODELS if collection == "blind75" else CAKE_MODELS
        for index, spec in enumerate(catalog):
            for language in LANGUAGES:
                starter = spec["starters"][language]
                solution_path = (
                    ROOT
                    / "solutions"
                    / language
                    / (spec["id"] + "." + EXTENSIONS[language])
                )
                original_solution = solution_path.read_text(encoding="utf-8")
                replacement = helper_name(spec, collection)
                starter_code, starter_imports, starter_symbols, starter_removed = split(
                    starter["starterCode"], language, models, replacement
                )
                solution_code, solution_imports, solution_symbols, solution_removed = (
                    split(original_solution, language, models, replacement)
                )
                header = headers[collection][language]
                prefix, suffix = support_envelope(
                    header, starter_imports + solution_imports, language, models
                )
                if language == "javascript":
                    entry_symbol = spec.get("className") or {
                        "strings_codec": "Codec",
                        "tree_codec": "Codec",
                        "trie": "Trie",
                        "dictionary": "WordDictionary",
                        "median": "MedianFinder",
                    }.get(spec["mode"])
                    if entry_symbol is None:
                        entry_symbol = spec["method"][0].lower() + spec["method"][1:]
                    suffix = (
                        "\nmodule.exports = { "
                        + ", ".join([*models, entry_symbol])
                        + " };\n"
                    )
                entry = {
                    "problemId": spec["id"],
                    "language": language,
                    "filename": starter["filename"],
                    "signature": starter["signature"],
                    "starterCode": formatted(starter_code, language),
                    "solutionCode": formatted(solution_code, language),
                    "prefix": prefix,
                    "suffix": suffix,
                    "references": references_for(spec, collection, language, header),
                    "visibleSymbols": sorted(set(starter_symbols + solution_symbols)),
                    "hiddenSymbols": list(models),
                    "sourcePaths": [
                        catalog_path.relative_to(ROOT).as_posix(),
                        solution_path.relative_to(ROOT).as_posix(),
                    ],
                    "sourceSha256": {
                        "starter": digest(starter["starterCode"]),
                        "solution": digest(original_solution),
                    },
                    "removedUnrelatedSymbols": sorted(
                        set(
                            starter_removed
                            + solution_removed
                            + list(set(models) - set(required_models(spec, collection)))
                        )
                    ),
                }
                if collection == "interviewcake":
                    entry["incorrectCode"] = formatted(
                        incorrect_sources[language][spec["id"]]["incorrectCode"],
                        language,
                    )
                    entry["sourcePaths"].append(
                        "scripts/interviewcake/algorithms_" + language + ".json"
                    )
                validate_entry(entry, collection, spec)
                entries.append(entry)
            if (index + 1) % 15 == 0:
                print(
                    f"Prepared {collection} {index + 1}/{len(catalog)} questions",
                    file=sys.stderr,
                    flush=True,
                )
    assert (
        len(entries) == 580
        and len({(e["problemId"], e["language"]) for e in entries}) == 580
    )
    return entries


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", type=Path, default=ROOT / "workspace-code/parts/isolated.json"
    )
    options = parser.parse_args()
    entries = build_entries()
    payload = {"schemaVersion": 1, "codeFormat": "callable-v1", "entries": entries}
    options.output.parent.mkdir(parents=True, exist_ok=True)
    # Readers must never observe a partially written catalog during regeneration.
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=options.output.parent,
            delete=False,
        ) as temporary:
            temporary_path = Path(temporary.name)
            temporary.write(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
            temporary.flush()
            os.fsync(temporary.fileno())
        temporary_path.replace(options.output)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
    print(
        f"Prepared {len(entries)} callable pairs / {len(entries) * 2} visible artifacts: {options.output}"
    )


if __name__ == "__main__":
    main()
