"""Audit every bank-owned starter and solution shown in the practice workspace.

This gate never reads user drafts.  Syntax/symbol inspection is a presentation
check, not a replacement for compiling and executing the composed submissions.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib
import importlib.util
import json
import re
import shutil
import subprocess
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from functools import cache, lru_cache
from pathlib import Path

from common import ROOT, format_code, parse, text_of

LANGUAGES = {"csharp", "javascript", "python", "cpp", "java"}
ROLES = ("starter", "solution")
JUDGE_IDENTIFIERS = {
    "GenericTest",
    "GenericTestMain",
    "WebGenericTestMain",
    "generic_test",
    "TimedExecutor",
    "TestFailure",
    "enable_executor_hook",
    "run_func_with_retries",
    "SerializationTrait",
    "EpiTest",
    "EpiTestComparator",
    "EpiUserType",
    "__bankCase",
    "CheckSequenceIsUniformlyRandom",
    "CheckSequenceIsUniformlyRandomWrapper",
    "check_sequence_is_uniformly_random",
    "check_sequence_is_uniformly_random_wrapper",
}
IDENTIFIER_NODES = {
    "identifier",
    "type_identifier",
    "namespace_identifier",
    "field_identifier",
    "property_identifier",
}
TYPE_NODES = {
    "class_declaration",
    "struct_declaration",
    "record_declaration",
    "enum_declaration",
    "interface_declaration",
    "class_specifier",
    "struct_specifier",
    "enum_specifier",
}
CALLABLE_NODES = {
    "function_definition",
    "function_declaration",
    "method_declaration",
    "method_definition",
    "constructor_declaration",
    "local_function_statement",
}
IMPORT_NODES = {
    "using_directive",
    "using_declaration",
    "import_declaration",
    "preproc_include",
    "package_declaration",
}
HELPER_CONTAINERS = {"Probe", "TreeAlgorithms", "ListAlgorithms", "GraphAlgorithms"}
BLIND_MODELS = {"ListNode", "TreeNode", "Node"}
CAKE_MODELS = {
    "LinkedListNode",
    "BinaryTreeNode",
    "GraphNode",
    "Meeting",
    "Rectangle",
    "CakeType",
    "FilePaths",
    "InfinityException",
    "RandomSource",
}


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def walk(node):
    yield node
    for child in node.named_children:
        yield from walk(child)


def declared_name(node, source: str) -> str | None:
    name = node.child_by_field_name("name")
    if name is not None:
        return text_of(name, source)
    declarator = node.child_by_field_name("declarator")
    if declarator is not None:
        return declared_name(declarator, source)
    if node.type in IDENTIFIER_NODES:
        return text_of(node, source)
    if node.type == "qualified_identifier":
        return declared_name(node.child_by_field_name("name"), source)
    for child in node.named_children:
        if child.type in {
            "variable_declarator",
            "init_declarator",
            "function_declarator",
        }:
            return declared_name(child, source)
    return None


def parsed(code: str, language: str):
    # EPI Java intentionally shows class members rather than its hidden driver.
    source = "class __Audit {\n" + code + "\n}\n" if language == "java" else code
    tree = parse(source, language)
    container = tree.root_node
    if language == "java":
        outer = next(
            node
            for node in container.named_children
            if node.type == "class_declaration"
        )
        container = outer.child_by_field_name("body")
    return source, tree, container


def parser_errors(code: str, language: str) -> list[dict]:
    if language == "python":
        try:
            ast.parse(code)
            return []
        except SyntaxError as error:
            return [{"kind": "SyntaxError", "text": error.msg, "line": error.lineno}]
    source, tree, _ = parsed(code, language)
    return [
        {
            "kind": node.type,
            "text": text_of(node, source),
            "line": node.start_point.row + (0 if language == "java" else 1),
        }
        for node in walk(tree.root_node)
        if node.type == "ERROR" or node.is_missing
    ]


def syntax_exception(
    entry: dict, role: str, errors: list[dict], original: str
) -> list[dict]:
    """One pinned grammar bug is recorded, not silently treated as validation."""
    if (entry["problemId"], entry["language"], role) != (
        "string_decompositions_into_dictionary_words",
        "csharp",
        "solution",
    ):
        return []
    expected = [("ERROR", "required")]
    observed = [(error["kind"], error["text"]) for error in errors]
    prior = [
        (error["kind"], error["text"]) for error in parser_errors(original, "csharp")
    ]
    if observed == prior == expected:
        return [
            {
                "reason": "Pinned C# grammar treats the valid contextual identifier required as a keyword.",
                "originalAndFormattedErrors": errors,
                "requiredIndependentCheck": "The .NET 10 full execution matrix must compile this exact artifact.",
            }
        ]
    return []


def facts(code: str, language: str) -> dict:
    if language == "python":
        tree = ast.parse(code)
        names = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
        names |= {
            node.attr for node in ast.walk(tree) if isinstance(node, ast.Attribute)
        }
        imports = [
            node for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom))
        ]
        import_paths = [
            node.module or "" for node in imports if isinstance(node, ast.ImportFrom)
        ]
        import_paths += [
            name.name
            for node in imports
            if isinstance(node, ast.Import)
            for name in node.names
        ]
        definitions = {
            node.name
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        }
        top_types = {node.name for node in tree.body if isinstance(node, ast.ClassDef)}
        main_guard = any(
            isinstance(node, ast.If)
            and any(
                isinstance(child, ast.Constant) and child.value == "__main__"
                for child in ast.walk(node.test)
            )
            for node in tree.body
        )
        return {
            "identifiers": names,
            "definitions": definitions,
            "topTypes": top_types,
            "frameworkImports": [
                name for name in import_paths if "test_framework" in name
            ],
            "main": main_guard or bool(definitions & {"main", "Main"}),
            "exports": False,
        }
    source, tree, container = parsed(code, language)
    nodes = list(walk(tree.root_node))
    names = {text_of(node, source) for node in nodes if node.type in IDENTIFIER_NODES}
    definitions = {
        name
        for node in nodes
        if node.type in TYPE_NODES | CALLABLE_NODES
        if (name := declared_name(node, source)) and name != "__Audit"
    }
    top_types = {
        name
        for node in container.named_children
        if node.type in TYPE_NODES
        if (name := declared_name(node, source))
    }
    imports = [text_of(node, source) for node in nodes if node.type in IMPORT_NODES]
    exports = any(
        node.type in {"member_expression", "member_access_expression"}
        and text_of(node, source).replace(" ", "") == "module.exports"
        for node in nodes
    )
    return {
        "identifiers": names,
        "definitions": definitions,
        "topTypes": top_types,
        "frameworkImports": [
            value
            for value in imports
            if "test_framework" in value or "EpiJudge.TestFramework" in value
        ],
        "main": bool(definitions & {"main", "Main"}),
        "exports": exports,
    }


def helper_calls(
    code: str, language: str, container: str, *, internal: bool
) -> set[str]:
    if language == "python":
        result = set()
        for node in ast.walk(ast.parse(code)):
            qualifiers = {container, "self", "cls"} if internal else {container}
            if (
                isinstance(node, ast.Attribute)
                and isinstance(node.value, ast.Name)
                and node.value.id in qualifiers
            ):
                result.add(node.attr)
            elif (
                internal
                and isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
            ):
                result.add(node.func.id)
        return result
    source, tree, _ = parsed(code, language)
    result = set()
    for node in walk(tree.root_node):
        if node.type in {
            "member_expression",
            "member_access_expression",
            "qualified_identifier",
            "method_reference",
        }:
            obj = (
                node.child_by_field_name("object")
                or node.child_by_field_name("expression")
                or node.child_by_field_name("scope")
            )
            name = node.child_by_field_name("property") or node.child_by_field_name(
                "name"
            )
            if (
                node.type == "method_reference"
                and (obj is None or name is None)
                and len(node.named_children) >= 2
            ):
                obj, name = node.named_children[0], node.named_children[-1]
            qualifiers = {container, "this"} if internal else {container}
            if (
                obj is not None
                and name is not None
                and text_of(obj, source) in qualifiers
            ):
                result.add(text_of(name, source))
        if node.type == "method_invocation":
            name, obj = (
                node.child_by_field_name("name"),
                node.child_by_field_name("object"),
            )
            if name is not None and (
                (obj is not None and text_of(obj, source) == container)
                or (internal and obj is None)
            ):
                result.add(text_of(name, source))
        elif node.type in {"call_expression", "invocation_expression"}:
            function = node.child_by_field_name("function")
            if function is None:
                function = next(iter(node.named_children), None)
            if function is None:
                continue
            if function.type in {
                "member_expression",
                "member_access_expression",
                "qualified_identifier",
            }:
                obj = (
                    function.child_by_field_name("object")
                    or function.child_by_field_name("expression")
                    or function.child_by_field_name("scope")
                )
                name = function.child_by_field_name(
                    "property"
                ) or function.child_by_field_name("name")
                qualifiers = {container, "this"} if internal else {container}
                if (
                    obj is not None
                    and name is not None
                    and text_of(obj, source) in qualifiers
                ):
                    result.add(text_of(name, source))
            elif internal and function.type == "identifier":
                result.add(text_of(function, source))
    return result


def helper_dependencies(code: str, language: str) -> tuple[list[str], list[dict]]:
    """Reject an unused Probe library, including unreachable methods in a used one."""
    errors, decisions = [], []
    if language == "python":
        module = ast.parse(code)
        containers = [
            (node.name, node)
            for node in module.body
            if isinstance(node, ast.ClassDef) and node.name in HELPER_CONTAINERS
        ]
        defined = {name for name, _ in containers}
        for helper in HELPER_CONTAINERS - defined:
            if helper_calls(code, language, helper, internal=False):
                errors.append(f"Missing visible algorithm helper container: {helper}")
        for name, node in containers:
            methods = {
                child.name: ast.unparse(child)
                for child in node.body
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef))
            }
            other = ast.unparse(
                ast.Module(
                    body=[child for child in module.body if child is not node],
                    type_ignores=[],
                )
            )
            references = helper_calls(other, language, name, internal=False)
            roots = references & methods.keys()
            if references - methods.keys():
                errors.append(
                    f"Missing visible helper members in {name}: {sorted(references - methods.keys())}"
                )
            reachable = set(roots)
            pending = list(roots)
            while pending:
                for dependency in (
                    helper_calls(methods[pending.pop()], language, name, internal=True)
                    & methods.keys()
                ):
                    if dependency not in reachable:
                        reachable.add(dependency)
                        pending.append(dependency)
            unused = sorted(methods.keys() - reachable)
            if not roots or unused:
                errors.append(
                    f"Unneeded helper library members in {name}: {unused or sorted(methods)}"
                )
            decisions.append(
                {
                    "container": name,
                    "entryCalls": sorted(roots),
                    "reachableMethods": sorted(reachable),
                    "declaredMethods": sorted(methods),
                }
            )
        return errors, decisions
    source, _tree, container = parsed(code, language)
    declared_containers = {
        declared_name(node, source) for node in container.named_children
    }
    for helper in HELPER_CONTAINERS - declared_containers:
        if helper_calls(code, language, helper, internal=False):
            errors.append(f"Missing visible algorithm helper container: {helper}")
    for node in container.named_children:
        name = declared_name(node, source)
        if name not in HELPER_CONTAINERS:
            continue
        body = node.child_by_field_name("body")
        if language == "javascript":
            declaration = next(
                (
                    child
                    for child in node.named_children
                    if child.type == "variable_declarator"
                ),
                None,
            )
            body = (
                declaration.child_by_field_name("value")
                if declaration is not None
                else body
            )
        if body is None:
            continue
        methods = {}
        for member in body.named_children:
            if member.type not in CALLABLE_NODES:
                continue
            member_name = declared_name(member, source)
            if member_name:
                methods.setdefault(member_name, []).append(text_of(member, source))
        # Remove only the known owned declaration's range, not any user source.
        data = source.encode("utf-8")
        other = (data[: node.start_byte] + data[node.end_byte :]).decode("utf-8")
        references = helper_calls(other, language, name, internal=False)
        roots = references & methods.keys()
        if references - methods.keys():
            errors.append(
                f"Missing visible helper members in {name}: {sorted(references - methods.keys())}"
            )
        reachable = set(roots)
        pending = list(roots)
        while pending:
            for member in methods[pending.pop()]:
                for dependency in (
                    helper_calls(member, language, name, internal=True) & methods.keys()
                ):
                    if dependency not in reachable:
                        reachable.add(dependency)
                        pending.append(dependency)
        unused = sorted(methods.keys() - reachable)
        if not roots or unused:
            errors.append(
                f"Unneeded helper library members in {name}: {unused or sorted(methods)}"
            )
        decisions.append(
            {
                "container": name,
                "entryCalls": sorted(roots),
                "reachableMethods": sorted(reachable),
                "declaredMethods": sorted(methods),
            }
        )
    return errors, decisions


@lru_cache(maxsize=1)
def isolated_contracts():
    catalogs = {}
    for collection in ("blind75", "interviewcake"):
        rows = json.loads(
            (ROOT / collection / "catalog.json").read_text(encoding="utf-8")
        )
        catalogs.update({row["id"]: row for row in rows})
    # Type facts come from authored specs, not the generated reference decision.
    sys.path.insert(0, str(ROOT / "scripts/blind75"))
    blind = importlib.util.spec_from_file_location(
        "audit_blind_specs", ROOT / "scripts/blind75/specs.py"
    )
    blind_module = importlib.util.module_from_spec(blind)
    blind.loader.exec_module(blind_module)
    cake = importlib.util.spec_from_file_location(
        "audit_cake_specs", ROOT / "scripts/interviewcake/specs.py"
    )
    cake_module = importlib.util.module_from_spec(cake)
    cake.loader.exec_module(cake_module)
    specs = {row["id"]: row for row in blind_module.SPECS + cake_module.S}
    return catalogs, specs


@lru_cache(maxsize=1)
def ctci_contracts():
    return {
        row["id"]: row
        for row in json.loads((ROOT / "ctci6/practice/catalog.json").read_text())
    }


def expected_references(entry: dict) -> set[str] | None:
    problem_id = entry["problemId"]
    if problem_id.startswith("ctci6_"):
        row = ctci_contracts()[problem_id]
        if row["batch"] == 2:
            return {"LinkedListNode"}
        if row["ref"] == "10.4":
            return {"Listy"}
        if row["batch"] == 3:
            return {"BankError"} | (
                {"IntStack"}
                if row["ref"] == "3.5"
                else {"Animal"}
                if row["ref"] == "3.6"
                else set()
            )
        return set()
    if not problem_id.startswith(("blind75_", "interviewcake_")):
        return None
    _, specs = isolated_contracts()
    spec = specs[problem_id]
    kinds = {parameter["type"] for parameter in spec["params"]} | {spec["result"]}
    names = set()
    if problem_id.startswith("blind75_"):
        if kinds & {"list", "lists"}:
            names.add("ListNode")
        if kinds & {"tree", "tree_node"}:
            names.add("TreeNode")
        if "graph" in kinds:
            names.add("Node")
    else:
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
        names |= {name for kind, name in mapping.items() if kind in kinds}
        if spec["mode"] in {"shuffle", "rand5", "rand7"}:
            names.add("RandomSource")
        if problem_id == "interviewcake_cake-thief":
            names.add("InfinityException")
    return names


def isolated_roots(entry: dict) -> set[str] | None:
    problem_id, language = entry["problemId"], entry["language"]
    if problem_id.startswith("ctci6_"):
        row = ctci_contracts()[problem_id]
        return {
            row["method"]
            if row["result"] == "state" or language in ("python", "javascript")
            else "Solution"
        }
    if not problem_id.startswith(("blind75_", "interviewcake_")):
        return None
    spec = isolated_contracts()[1][problem_id]
    if problem_id.startswith("interviewcake_"):
        return {spec["className"]}
    state = {
        "strings_codec": "Codec",
        "tree_codec": "Codec",
        "trie": "Trie",
        "dictionary": "WordDictionary",
        "median": "MedianFinder",
    }.get(spec["mode"])
    if language in {"csharp", "cpp", "java"}:
        return {state or "Solution"}
    if state:
        return {state}
    method = spec["method"]
    if language == "python":
        return {
            re.sub(r"(?<!^)(?=[A-Z])", "_", method)
            .lower()
            .replace("b_s_t", "bst")
            .replace("l_i_s", "lis")
        }
    return {method[0].lower() + method[1:]}


def top_units(code: str, language: str) -> list[tuple[set[str], set[str]]]:
    """Whole top-level declarations form an over-approximate global symbol graph.

    Nested algorithm classes remain atomic; the separately checked Probe-family
    graph proves method-level trimming for those formerly universal libraries.
    """
    units = []
    if language == "python":
        for node in ast.parse(code).body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                names = {node.name}
            elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                targets = (
                    node.targets if isinstance(node, ast.Assign) else [node.target]
                )
                names = {
                    child.id
                    for target in targets
                    for child in ast.walk(target)
                    if isinstance(child, ast.Name)
                }
            else:
                continue
            refs = {
                child.id
                for child in ast.walk(node)
                if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Load)
            }
            units.append((names, refs))
        return units
    source, _, container = parsed(code, language)
    pending = list(container.named_children)
    while pending:
        node = pending.pop(0)
        if node.type in IMPORT_NODES or node.type in {
            "comment",
            "line_comment",
            "block_comment",
            "empty_statement",
        }:
            continue
        name = declared_name(node, source)
        if node.type == "namespace_definition" and name is None:
            body = node.child_by_field_name("body")
            if body is not None:
                pending[0:0] = list(body.named_children)
            continue
        if name is None:
            continue
        refs = {
            text_of(child, source)
            for child in walk(node)
            if child.type in IDENTIFIER_NODES
        }
        units.append(({name}, refs))
    return units


def isolated_global_dependencies(
    entry: dict, code: str, role: str
) -> tuple[list[str], dict | None]:
    roots = isolated_roots(entry)
    if roots is None:
        return [], None
    units = top_units(code, entry["language"])
    definitions = {name: refs for names, refs in units for name in names}
    errors = []
    if not roots <= definitions.keys():
        errors.append(
            "Callable entry definitions are missing: "
            + ", ".join(sorted(roots - definitions.keys()))
        )
    reachable = set(roots)
    pending = list(roots & definitions.keys())
    while pending:
        for dependency in definitions[pending.pop()] & definitions.keys():
            if dependency not in reachable:
                reachable.add(dependency)
                pending.append(dependency)
    extra = definitions.keys() - reachable
    if extra:
        errors.append(
            "Unrelated top-level algorithm declarations: " + ", ".join(sorted(extra))
        )
    if role == "starter" and definitions.keys() != roots:
        errors.append("Starter must contain only the callable task class/functions")
    # These known bank algorithm helpers must be visible when referenced, not
    # silently moved into an execution envelope to make an incomplete view run.
    refs = set().union(*(values for _, values in units)) if units else set()
    missing = (refs & {"word_exists", "component_count"}) - definitions.keys()
    if missing:
        errors.append(
            "Algorithm helpers are hidden or missing: " + ", ".join(sorted(missing))
        )
    return errors, {
        "roots": sorted(roots),
        "declaredSymbols": sorted(definitions),
        "reachableSymbols": sorted(reachable),
    }


@lru_cache(maxsize=1)
def managed_starters():
    from managed import problems

    return {problem["Id"]: problem for problem in problems()}


def original_code(entry: dict, role: str) -> str:
    if role == "solution":
        path = next(
            path for path in entry["sourcePaths"] if path.startswith("solutions/")
        )
        return (ROOT / path).read_text(encoding="utf-8")
    problem_id, language = entry["problemId"], entry["language"]
    if problem_id.startswith("ctci6_"):
        source = ctci_contracts()[problem_id]["languages"][language]
        return source["prefix"] + source["starterCode"] + source["suffix"]
    if problem_id.startswith(("blind75_", "interviewcake_")):
        return isolated_contracts()[0][problem_id]["starters"][language]["starterCode"]
    if language in {"cpp", "java"}:
        return (ROOT / entry["sourcePaths"][0]).read_text(encoding="utf-8")
    key = {
        "csharp": "StarterCode",
        "javascript": "JsStarterCode",
        "python": "PyStarterCode",
    }[language]
    return managed_starters()[problem_id][key]


def audit_artifact(
    entry: dict, role: str, *, check_format: bool = True, original: str | None = None
) -> dict:
    code, language = entry[role + "Code"], entry["language"]
    errors, exceptions = [], []
    if not code.strip() or len(code) > 40000:
        errors.append("Visible code must contain between 1 and 40000 characters")
    syntax = parser_errors(code, language)
    if syntax:
        exceptions = syntax_exception(entry, role, syntax, original or "")
        if not exceptions:
            errors.append(
                "Visible syntax errors: " + json.dumps(syntax, ensure_ascii=False)
            )
    information = facts(code, language) if language != "python" or not syntax else None
    dependencies = []
    global_dependencies = None
    if information:
        forbidden = sorted(information["identifiers"] & JUDGE_IDENTIFIERS)
        if forbidden:
            errors.append("Judge identifiers are visible: " + ", ".join(forbidden))
        if information["frameworkImports"]:
            errors.append(
                "Judge-framework imports are visible: "
                + ", ".join(information["frameworkImports"])
            )
        if information["main"]:
            errors.append("A judge/program main entry point is visible")
        if information["exports"]:
            errors.append("JavaScript export glue is visible")
        supplied = (
            BLIND_MODELS
            if entry["problemId"].startswith("blind75_")
            else CAKE_MODELS
            if entry["problemId"].startswith("interviewcake_")
            else {"LinkedListNode", "IntStack", "Animal", "BankError", "Listy"}
            if entry["problemId"].startswith("ctci6_")
            else set()
        )
        duplicated_models = sorted(information["topTypes"] & supplied)
        if duplicated_models:
            errors.append(
                "Bank-supplied models must be read-only references: "
                + ", ".join(duplicated_models)
            )
        helper_errors, dependencies = helper_dependencies(code, language)
        errors.extend(helper_errors)
        global_errors, global_dependencies = isolated_global_dependencies(
            entry, code, role
        )
        errors.extend(global_errors)
    if check_format:
        try:
            if format_code(code, language) != code:
                errors.append("Visible code is not in the pinned readable format")
        except (RuntimeError, OSError) as error:
            errors.append(str(error))
    long_lines = [
        {"line": number, "length": len(line), "text": line}
        for number, line in enumerate(code.splitlines(), 1)
        if len(line) > 120
    ]
    # No blanket width exception. A future unavoidable literal needs an explicit,
    # reviewed policy; every current artifact fits this limit after formatting.
    if long_lines:
        errors.append(
            "Visible lines exceed 120 columns: "
            + json.dumps(long_lines, ensure_ascii=False)
        )
    return {
        "problemId": entry["problemId"],
        "language": language,
        "role": role,
        "codeSha256": digest(code),
        "sourceChanged": original is not None and original != code,
        "originalSha256": digest(original) if original is not None else None,
        "lines": len(code.splitlines()),
        "maximumLineLength": max(map(len, code.splitlines()), default=0),
        "syntaxExceptions": exceptions,
        "helperDependencies": dependencies,
        "globalDependencies": global_dependencies,
        "errors": errors,
        "success": not errors,
    }


def audit_references(entry: dict, *, check_format: bool = True) -> list[dict]:
    actual = {name for reference in entry["references"] for name in reference["names"]}
    expected = expected_references(entry)
    results = []
    if expected is not None and actual != expected:
        results.append(
            {
                "problemId": entry["problemId"],
                "language": entry["language"],
                "title": "Required reference inventory",
                "errors": [f"Expected only {sorted(expected)}, got {sorted(actual)}"],
                "success": False,
            }
        )
    for reference in entry["references"]:
        code = reference["code"]
        errors = []
        information = facts(code, entry["language"])
        forbidden = information["identifiers"] & JUDGE_IDENTIFIERS
        if (
            forbidden
            or information["frameworkImports"]
            or information["main"]
            or information["exports"]
        ):
            errors.append("Judge glue is present in a supplied-type/API reference")
        if (
            "RandomSource" in reference["names"]
            and "Draw" in information["definitions"]
        ):
            errors.append(
                "Judge-only random injection must not be exposed in the reference"
            )
        syntax = parser_errors(code, entry["language"])
        syntax_exceptions = reference_syntax_exception(
            reference, entry["language"], syntax
        )
        if syntax and not syntax_exceptions:
            errors.append(
                "Reference syntax errors: " + json.dumps(syntax, ensure_ascii=False)
            )
        if check_format and format_code(code, entry["language"]) != code:
            errors.append("Reference is not in the pinned readable format")
        if any(len(line) > 120 for line in code.splitlines()):
            errors.append("Reference line exceeds 120 columns")
        results.append(
            {
                "problemId": entry["problemId"],
                "language": entry["language"],
                "title": reference["title"],
                "names": reference["names"],
                "codeSha256": digest(code),
                "errors": errors,
                "success": not errors,
            }
        )
        results[-1]["syntaxExceptions"] = syntax_exceptions
    return results


def audit_envelope(entry: dict) -> dict:
    """Unused algorithm libraries must be removed, not merely hidden from view."""
    prefix, code, suffix = entry["prefix"], entry["solutionCode"], entry["suffix"]
    source = prefix + code + suffix
    errors, hidden_libraries = [], []
    begin = len(prefix.encode("utf-8"))
    end = begin + len(code.encode("utf-8"))
    if entry["language"] == "python":
        tree = ast.parse(source)
        lines = source.splitlines(keepends=True)
        for node in tree.body:
            if not isinstance(
                node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
            ):
                continue
            if node.name not in HELPER_CONTAINERS | {"word_exists", "component_count"}:
                continue
            start = (
                len("".join(lines[: node.lineno - 1]).encode("utf-8")) + node.col_offset
            )
            finish = (
                len("".join(lines[: node.end_lineno - 1]).encode("utf-8"))
                + node.end_col_offset
            )
            if start < begin or finish > end:
                hidden_libraries.append(node.name)
    else:
        tree = parse(source, entry["language"])
        for node in walk(tree.root_node):
            if node.type not in TYPE_NODES | {
                "namespace_definition",
                "lexical_declaration",
                "variable_declaration",
            }:
                continue
            name = declared_name(node, source)
            if name in HELPER_CONTAINERS and (
                node.start_byte < begin or node.end_byte > end
            ):
                hidden_libraries.append(name)
    if hidden_libraries:
        errors.append(
            "Algorithm libraries are hidden in judge support: "
            + ", ".join(sorted(set(hidden_libraries)))
        )
    return {
        "problemId": entry["problemId"],
        "language": entry["language"],
        "prefixSha256": digest(prefix),
        "suffixSha256": digest(suffix),
        "hiddenAlgorithmLibraries": sorted(set(hidden_libraries)),
        "errors": errors,
        "success": not errors,
    }


@cache
def compile_list_node_reference(code: str) -> dict:
    compiler = shutil.which("g++") or shutil.which("clang++")
    if not compiler:
        raise RuntimeError(
            "A C++17 compiler is required to validate the supplied ListNode reference grammar exception"
        )
    source = (
        "#include <memory>\nusing std::shared_ptr;\n"
        + code
        + "\nint main() { ListNode<int> node; return node.data; }\n"
    )
    command = [compiler, "-std=c++17", "-fsyntax-only", "-x", "c++", "-"]
    result = subprocess.run(
        command,
        input=source,
        text=True,
        encoding="utf-8",
        capture_output=True,
        timeout=30,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(
            "C++17 rejected supplied ListNode reference: " + result.stderr
        )
    return {
        "compiler": Path(compiler).name,
        "flags": command[1:],
        "sourceSha256": digest(source),
        "exitCode": result.returncode,
    }


def reference_syntax_exception(
    reference: dict, language: str, errors: list[dict]
) -> list[dict]:
    if language != "cpp" or reference.get("names") != ["ListNode"] or len(errors) != 1:
        return []
    error = errors[0]
    if (error["kind"], error["text"]) != ("type_identifier", ""):
        return []
    code = reference["code"]
    line = code.splitlines()[error["line"] - 1]
    if (
        "ListNode(T data = {}," not in line
        or reference.get("sourcePath") != "epi_judge_cpp/list_node.h"
    ):
        return []
    source = (ROOT / reference["sourcePath"]).read_text(encoding="utf-8")
    if digest(source) != reference.get("sourceSha256"):
        return []
    constructor = "ListNode(T data = {}, shared_ptr<ListNode<T>> next = nullptr)"
    if "".join(constructor.split()) not in "".join(source.split()):
        return []
    compiled = compile_list_node_reference(code)
    return [
        {
            "reason": "Pinned C++ grammar inserts a missing type token at the valid T data = {} default argument.",
            "parserErrors": errors,
            "referenceSha256": digest(code),
            "sourcePath": reference["sourcePath"],
            "sourceSha256": reference["sourceSha256"],
            "independentCompilerCheck": compiled,
        }
    ]


def regeneration_checks(parts: dict) -> list[dict]:
    results = []
    for name, module_name in [
        ("epi-native", "native"),
        ("epi-managed", "managed"),
        ("isolated", "isolated"),
        *([("ctci6", "ctci")] if "ctci6" in parts else []),
    ]:
        module = importlib.import_module(module_name)
        generated = module.build_entries()
        expected = parts[name]["entries"]
        success = generated == expected
        results.append(
            {
                "part": name,
                "pairs": len(generated),
                "success": success,
                "generatedSha256": digest(
                    json.dumps(generated, sort_keys=True, ensure_ascii=False)
                ),
                "savedSha256": digest(
                    json.dumps(expected, sort_keys=True, ensure_ascii=False)
                ),
            }
        )
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--no-regeneration",
        action="store_true",
        help="Development probe only; produces incomplete acceptance evidence",
    )
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    from build import PARTS, build

    report = {
        "schemaVersion": 1,
        "passed": False,
        "complete": False,
        "artifacts": [],
        "references": [],
        "envelopes": [],
        "errors": [],
    }
    target = ROOT / ".epi-runs/callable-content-audit.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        catalog_path = ROOT / "workspace-code/catalog.json"
        coverage_path = ROOT / "workspace-code/coverage.json"
        input_paths = [catalog_path, coverage_path]
        input_paths += sorted((ROOT / "workspace-code/parts").glob("*.json"))
        input_paths += sorted((ROOT / "scripts/code_workspace").glob("*.py"))
        input_paths += sorted((ROOT / "scripts/code_workspace").glob("*.json"))
        if (ROOT / "ctci6/practice/catalog.json").exists():
            input_paths += [
                ROOT / "ctci6/catalog.json",
                ROOT / "ctci6/practice/catalog.json",
                ROOT / "ctci6/practice/coverage.json",
            ]
        input_paths.append(ROOT / "scripts/code_workspace/requirements.txt")
        source_hashes = {
            str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in input_paths
        }
        report["inputHashes"] = source_hashes
        report["catalogSha256"] = source_hashes["workspace-code/catalog.json"]
        report["coverageSha256"] = source_hashes["workspace-code/coverage.json"]
        report["scriptSha256"] = source_hashes["scripts/code_workspace/audit.py"]
        document, coverage = build()
        for filename, expected in [
            ("catalog.json", document),
            ("coverage.json", coverage),
        ]:
            actual = json.loads(
                (ROOT / "workspace-code" / filename).read_text(encoding="utf-8")
            )
            if actual != expected:
                raise ValueError(
                    f"Stale or incomplete callable artifact: workspace-code/{filename}"
                )
        parts = {
            name: json.loads(
                (ROOT / "workspace-code/parts" / (name + ".json")).read_text(
                    encoding="utf-8"
                )
            )
            for name in list(PARTS)
            + (["ctci6"] if "ctci6" in coverage["collections"] else [])
        }
        entries = document["entries"]
        tasks = []
        for entry in entries:
            for role in ROLES:
                original = original_code(entry, role)
                if digest(original) != entry["sourceSha256"][role]:
                    raise ValueError(
                        f"Original source fingerprint mismatch: {entry['problemId']}/{entry['language']}/{role}"
                    )
                tasks.append((entry, role, original))
        print(
            f"Auditing all {len(tasks)} visible artifacts and their supplied references.",
            flush=True,
        )

        def check_task(task):
            entry, role, original = task
            return audit_artifact(entry, role, original=original)

        with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
            report["artifacts"] = list(pool.map(check_task, tasks))
            references = list(pool.map(audit_references, entries))
            report["references"] = [row for group in references for row in group]
            report["envelopes"] = list(pool.map(audit_envelope, entries))
        print(
            "Completed every syntax, visibility, dependency, reference and formatting check; regenerating every registered source part.",
            flush=True,
        )
        report["generators"] = (
            [] if args.no_regeneration else regeneration_checks(parts)
        )
        report["inventory"] = {
            "questions": len({entry["problemId"] for entry in entries}),
            "questionLanguagePairs": len(entries),
            "visibleArtifacts": len(tasks),
            "collections": coverage["collections"],
            "artifactsByLanguage": dict(
                Counter(row["language"] for row in report["artifacts"])
            ),
        }
        report["sourceChanges"] = {
            "changed": sum(row["sourceChanged"] for row in report["artifacts"]),
            "alreadyIdentical": sum(
                not row["sourceChanged"] for row in report["artifacts"]
            ),
        }
        report["referenceBlocks"] = len(report["references"])
        report["syntaxExceptions"] = [
            {
                "problemId": row["problemId"],
                "language": row["language"],
                "role": row.get("role"),
                "referenceTitle": row.get("title"),
                "codeSha256": row["codeSha256"],
                "decision": exception,
            }
            for section in ("artifacts", "references")
            for row in report[section]
            for exception in row.get("syntaxExceptions", [])
        ]
        report["questions"] = report["inventory"]["questions"]
        report["visibleArtifacts"] = report["inventory"]["visibleArtifacts"]
        report["complete"] = not args.no_regeneration
        changed_inputs = [
            name
            for name, expected_sha in source_hashes.items()
            if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != expected_sha
        ]
        if changed_inputs:
            report["errors"].append(
                "Inputs changed during the audit: " + ", ".join(changed_inputs)
            )
        report["passed"] = (
            not report["errors"]
            and report["complete"]
            and all(
                row["success"]
                for section in ("artifacts", "references", "envelopes", "generators")
                for row in report[section]
            )
        )
    except Exception as error:  # noqa: BLE001 - record unexpected audit failures before exiting nonzero.
        report["errors"].append(f"{type(error).__name__}: {error}")
    finally:
        target.write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    failures = [
        row
        for section in ("artifacts", "references", "envelopes", "generators")
        for row in report.get(section, [])
        if not row["success"]
    ]
    print(
        json.dumps(
            {
                "passed": report["passed"],
                "complete": report["complete"],
                "inventory": report.get("inventory"),
                "sourceChanges": report.get("sourceChanges"),
                "failedChecks": len(failures),
                "errors": report["errors"],
                "firstFailures": failures[:15],
                "report": str(target.relative_to(ROOT)),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
