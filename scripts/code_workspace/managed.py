"""Build clean EPI C#, JavaScript and Python callable workspace artifacts.

Only bank-owned, checked-in programs are split. Saved or submitted user code is
never inspected or rewritten by this generator. Reviewed Python entrypoints are
explicit in managed-roots.json; AST dependency analysis keeps algorithm helpers
visible and moves only supplied models and judge support into the envelope.
"""

from __future__ import annotations

import ast
import hashlib
import json
import symtable
from concurrent.futures import ThreadPoolExecutor
from functools import cache, lru_cache
from pathlib import Path

from common import ROOT, format_code, parse, text_of

LANGUAGES = ("csharp", "javascript", "python")
EXTENSIONS = {"csharp": "cs", "javascript": "js", "python": "py"}
CURATED = {"count_bits", "two_sum", "anagrams"}
PYTHON_PRIMITIVES = {"zero_one_random"}
PYTHON_MODEL_MODULES = {
    "list_node",
    "binary_tree_node",
    "bst_node",
    "binary_tree_with_parent_prototype",
    "posting_list_node",
    "doubly_list_node",
}
CSHARP_MODELS = {"BinaryTreeNode", "ListNode", "PostingListNode", "GraphVertex"}
JAVASCRIPT_MODELS = CSHARP_MODELS


def digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def descendants(node):
    yield node
    for child in node.named_children:
        yield from descendants(child)


def csharp_literal(argument, source: str) -> str:
    strings = [n for n in argument.named_children if n.type == "string_literal"]
    if len(strings) != 1:
        raise ValueError("A curated starter must be one ordinary C# string literal")
    return json.loads(text_of(strings[0], source))


def problems() -> list[dict]:
    """Read all 218 actual managed starters without running catalog generation."""
    result = json.loads(
        (ROOT / "EpiJudge.Runner/catalog.json").read_text(encoding="utf-8")
    )
    source = (ROOT / "EpiJudge.Runner/ProblemCatalog.cs").read_text(encoding="utf-8")
    tree = parse(source, "csharp")
    for node in descendants(tree.root_node):
        if node.type != "implicit_object_creation_expression":
            continue
        arguments = next(
            (c for c in node.named_children if c.type == "argument_list"), None
        )
        if arguments is None or len(arguments.named_children) < 10:
            continue
        positional = arguments.named_children
        first = next(
            (c for c in positional[0].named_children if c.type == "string_literal"),
            None,
        )
        if first is None:
            continue
        problem_id = json.loads(text_of(first, source))
        if problem_id not in CURATED:
            continue
        item = {
            "Id": problem_id,
            "Signature": csharp_literal(positional[6], source),
            "StarterCode": csharp_literal(positional[7], source),
        }
        for argument in positional[10:]:
            identifier = next(
                (c for c in argument.named_children if c.type == "identifier"), None
            )
            if identifier is None:
                continue
            key = text_of(identifier, source)
            if key in {
                "JsSignature",
                "JsStarterCode",
                "JsInvocation",
                "PySignature",
                "PyStarterCode",
                "PyInvocation",
                "PySourceFile",
            }:
                item[key] = csharp_literal(argument, source)
        result.append(item)
    if len(result) != 218 or len({p["Id"] for p in result}) != 218:
        raise ValueError(
            "Managed starter inventory must contain exactly 218 distinct EPI questions"
        )
    return sorted(result, key=lambda p: p["Id"])


@cache
def formatted(code: str, language: str) -> str:
    return format_code(code, language) if code.strip() else ""


def top_symbols(code: str, language: str) -> list[str]:
    tree = parse(code, language)
    kinds = (
        {"class_declaration", "method_declaration", "constructor_declaration"}
        if language == "csharp"
        else {"function_declaration", "class_declaration", "method_definition"}
    )
    names = []
    for node in descendants(tree.root_node):
        if node.type in kinds:
            name = node.child_by_field_name("name")
            if name is not None:
                names.append(text_of(name, code))
    return sorted(set(names))


def identifiers(code: str, language: str) -> set[str]:
    return {
        text_of(n, code)
        for n in descendants(parse(code, language).root_node)
        if n.type == "identifier"
    }


def parser_errors(code: str, language: str) -> list[str]:
    """Retain known grammar limitations; the real compiler is authoritative."""
    return sorted(
        " ".join(text_of(n, code).split())
        for n in descendants(parse(code, language).root_node)
        if n.type == "ERROR" or n.is_missing
    )


def csharp_references(code: str) -> list[dict]:
    needed = identifiers(code, "csharp") & CSHARP_MODELS
    references = []
    for filename in ("Nodes.cs", "JudgeJson.cs"):
        source = (ROOT / "EpiJudge.TestFramework" / filename).read_text(
            encoding="utf-8"
        )
        for node in parse(source, "csharp").root_node.named_children:
            if node.type != "class_declaration":
                continue
            name = node.child_by_field_name("name")
            if name is not None and text_of(name, source) in needed:
                symbol = text_of(name, source)
                references.append(
                    {
                        "title": "Supplied " + symbol,
                        "code": text_of(node, source),
                        "names": [symbol],
                    }
                )
    if {n for r in references for n in r["names"]} != needed:
        raise ValueError("Missing C# supplied model reference: " + repr(needed))
    return references


def csharp_visible(code: str) -> str:
    """Move only the known bank namespace directive out of owned editor code."""
    source = code.encode("utf-8")
    ranges = []
    for node in parse(code, "csharp").root_node.named_children:
        if (
            node.type == "using_directive"
            and text_of(node, source).strip() == "using EpiJudge.TestFramework;"
        ):
            ranges.append((node.start_byte, node.end_byte))
    end = 0
    output = []
    for start, finish in ranges:
        output.append(source[end:start])
        end = finish
    output.append(source[end:])
    return b"".join(output).decode("utf-8")


@lru_cache(maxsize=1)
def javascript_model_sources() -> dict[str, str]:
    source = (ROOT / "EpiJudge.Runner/EpiJavascriptHarness.js").read_text(
        encoding="utf-8"
    )
    output = {}
    for node in parse(source, "javascript").root_node.named_children:
        if node.type == "class_declaration":
            name = text_of(node.child_by_field_name("name"), source)
            if name in JAVASCRIPT_MODELS:
                output[name] = text_of(node, source)
    return output


def javascript_split(code: str) -> tuple[str, str]:
    source = code.encode("utf-8")
    visible, exports = [], []
    for node in parse(code, "javascript").root_node.named_children:
        expression = (
            node.named_children[0] if node.type == "expression_statement" else None
        )
        left = (
            expression.child_by_field_name("left") if expression is not None else None
        )
        if (
            expression is not None
            and expression.type == "assignment_expression"
            and left is not None
            and text_of(left, source) == "module.exports"
        ):
            exports.append(text_of(node, source))
        else:
            visible.append(text_of(node, source))
    if len(exports) != 1:
        raise ValueError(
            "Every owned EPI JavaScript module must have one explicit export binding"
        )
    return "\n\n".join(visible) + "\n", "\n" + "\n".join(exports) + "\n"


def javascript_documented_models(code: str) -> set[str]:
    """Read supplied types from bank-owned JSDoc, including existing-node APIs."""
    names = set()
    for node in parse(code, "javascript").root_node.named_children:
        if node.type != "comment":
            continue
        for line in text_of(node, code).splitlines():
            if (
                not any(tag in line for tag in ("@param", "@return"))
                or "{" not in line
                or "}" not in line
            ):
                continue
            type_text = line.split("{", 1)[1].split("}", 1)[0]
            words = "".join(
                character if character.isalnum() or character == "_" else " "
                for character in type_text
            ).split()
            names.update(set(words) & JAVASCRIPT_MODELS)
    return names


def python_bindings(node) -> set[str]:
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        return {node.name}
    if isinstance(node, ast.Import):
        return {a.asname or a.name.split(".")[0] for a in node.names}
    if isinstance(node, ast.ImportFrom):
        return {a.asname or a.name for a in node.names}
    if isinstance(node, (ast.Assign, ast.AnnAssign)):
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        return {
            n.id
            for target in targets
            for n in ast.walk(target)
            if isinstance(n, ast.Name)
        }
    return set()


def python_segment(source: str, node) -> str:
    lines = source.splitlines()
    start = min([node.lineno] + [d.lineno for d in getattr(node, "decorator_list", [])])
    return "\n".join(lines[start - 1 : node.end_lineno])


def referenced_globals(table) -> set[str]:
    result = {
        s.get_name() for s in table.get_symbols() if s.is_referenced() and s.is_global()
    }
    for child in table.get_children():
        result.update(referenced_globals(child))
    return result


def python_dependencies(code: str, nodes: dict[str, ast.AST]) -> dict[str, set[str]]:
    table = symtable.symtable(code, "owned.py", "exec")
    children = {c.get_name(): c for c in table.get_children()}
    result = {}
    for name, node in nodes.items():
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            used = referenced_globals(children[name])
            # Annotations/decorators/defaults execute in the enclosing scope.
            for field in (getattr(node, "returns", None), getattr(node, "args", None)):
                if field is not None:
                    used.update(
                        n.id
                        for n in ast.walk(field)
                        if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)
                    )
            for decorator in getattr(node, "decorator_list", []):
                used.update(
                    n.id
                    for n in ast.walk(decorator)
                    if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)
                )
            # Python 3.14 no longer reports names used only in local variable
            # annotations through symtable. They still describe the recorded
            # callable API, so derive annotation dependencies explicitly from
            # AST nodes in every nested function/method as well. This keeps
            # generation byte-identical across supported Python versions.
            annotation_fields = []
            for annotated in ast.walk(node):
                if isinstance(annotated, ast.AnnAssign):
                    annotation_fields.append(annotated.annotation)
                elif isinstance(annotated, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    annotation_fields.extend((annotated.args, annotated.returns))
            for field in annotation_fields:
                if field is not None:
                    used.update(
                        n.id
                        for n in ast.walk(field)
                        if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)
                    )
        else:
            used = {
                n.id
                for n in ast.walk(node)
                if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)
            }
        result[name] = used
    return result


def closure(
    roots: set[str], dependencies: dict[str, set[str]], stop: set[str] | None = None
) -> set[str]:
    found = set(roots)
    pending = list(roots)
    while pending:
        name = pending.pop()
        if name in (stop or set()):
            continue
        for other in dependencies.get(name, set()) & dependencies.keys():
            if other not in found:
                found.add(other)
                pending.append(other)
    return found


def python_reference(name: str, node, source: str) -> dict:
    if isinstance(node, ast.ImportFrom):
        alias = next(a for a in node.names if (a.asname or a.name) == name)
        model_source = (ROOT / "epi_judge_python" / (node.module + ".py")).read_text(
            encoding="utf-8"
        )
        model = next(
            n
            for n in ast.parse(model_source).body
            if isinstance(n, ast.ClassDef) and n.name == alias.name
        )
        constructor = next(
            n
            for n in model.body
            if isinstance(n, ast.FunctionDef) and n.name == "__init__"
        )
        # Display the callable data API rather than formatting/comparison machinery.
        code = (
            "class "
            + model.name
            + ":\n"
            + "\n".join(
                "    " + line
                for line in python_segment(model_source, constructor).splitlines()
            )
        )
        if name != alias.name:
            code += "\n\n" + name + " = " + alias.name
        return {"title": "Supplied " + name, "code": code + "\n", "names": [name]}
    if name in PYTHON_PRIMITIVES:
        return {
            "title": "Supplied unbiased bit source",
            "code": 'def zero_one_random() -> int:\n    """Return 0 or 1, each with probability one half."""\n    ...\n',
            "names": [name],
        }
    return {
        "title": "Supplied " + name,
        "code": python_segment(source, node) + "\n",
        "names": [name],
    }


def python_split(problem: dict, solution: str, roots: list[str]) -> dict:
    starter = problem["PyStarterCode"]
    starter_tree = ast.parse(starter)
    starter_nodes = {}
    for node in starter_tree.body:
        for name in python_bindings(node):
            starter_nodes[name] = node
    starter_dependencies = python_dependencies(starter, starter_nodes)
    starter_closure = closure(set(roots), starter_dependencies)
    solution_tree = ast.parse(solution)
    all_nodes = {}
    for node in solution_tree.body:
        for name in python_bindings(node):
            all_nodes[name] = node
    dependencies = python_dependencies(solution, all_nodes)
    if set(roots) - all_nodes.keys():
        raise ValueError(problem["Id"] + " missing reviewed Python algorithm root")
    algorithm_closure = closure(set(roots), dependencies)
    supplied = {
        name
        for name in algorithm_closure
        if name in PYTHON_PRIMITIVES
        or isinstance(all_nodes[name], ast.ClassDef)
        and name not in roots
        or isinstance(all_nodes[name], ast.ImportFrom)
        and all_nodes[name].module in PYTHON_MODEL_MODULES
        or isinstance(all_nodes[name], (ast.Assign, ast.AnnAssign))
    }
    # Constants genuinely belonging to an algorithm stay visible. Namedtuple
    # declarations describe supplied record APIs and belong in the reference.
    supplied = {
        name
        for name in supplied
        if not isinstance(all_nodes[name], (ast.Assign, ast.AnnAssign))
        or any(
            isinstance(n, ast.Call)
            and isinstance(n.func, (ast.Name, ast.Attribute))
            and (
                (isinstance(n.func, ast.Name) and n.func.id == "namedtuple")
                or (isinstance(n.func, ast.Attribute) and n.func.attr == "namedtuple")
            )
            for n in ast.walk(all_nodes[name])
        )
    }
    visible_names = algorithm_closure - supplied
    visible_nodes = {id(all_nodes[name]) for name in visible_names}
    target = problem["PyInvocation"]
    support_roots = {target} & all_nodes.keys()
    original_support = closure(
        {target} & starter_nodes.keys(), starter_dependencies, set(roots)
    )
    # Some concise owned solutions deliberately supply a helper missing from
    # the original validator (gray-code adjacency is one example). Such helpers
    # are needed by the retained original wrapper even when that wrapper is not
    # repeated in the independently authored algorithm module.
    support_roots.update(
        name
        for original_name in original_support - set(roots)
        for name in starter_dependencies.get(original_name, set())
        if name in all_nodes and name not in visible_names
    )
    # Keep the canonical comparator and validator dependencies when the current
    # tested solution defines them, but never pull an unrelated alternate algorithm.
    original_main = next(
        (
            n
            for n in solution_tree.body
            if isinstance(n, ast.If)
            and any(
                isinstance(x, ast.Name) and x.id == "__name__" for x in ast.walk(n.test)
            )
        ),
        None,
    )
    if original_main is not None:
        support_roots.update(
            n.id
            for n in ast.walk(original_main)
            if isinstance(n, ast.Name)
            and isinstance(n.ctx, ast.Load)
            and n.id in all_nodes
        )
    support_closure = closure(support_roots | supplied, dependencies, set(roots))
    support_names = support_closure - visible_names
    # The visible module retains only imports actually needed by algorithm code.
    # The canonical envelope retains imports needed by its validators/models.
    visible_source = (
        "\n\n".join(
            python_segment(solution, n)
            for n in solution_tree.body
            if id(n) in visible_nodes
        )
        + "\n"
    )
    visible_ids = {id(all_nodes[name]) for name in visible_names}
    support_ids = {id(all_nodes[name]) for name in support_names}
    # A model or validator can need the same import as the visible algorithm.
    # Importing twice is harmless and preserves declaration-time annotations.
    support_ids.update(
        id(all_nodes[name])
        for name in support_closure
        if isinstance(all_nodes[name], (ast.Import, ast.ImportFrom))
    )
    support_source = (
        "\n\n".join(
            python_segment(solution, n)
            for n in solution_tree.body
            if id(n) in support_ids
        )
        + "\n"
    )
    # Future annotations must precede all definitions after envelope composition.
    future_nodes = [
        n
        for n in solution_tree.body
        if isinstance(n, ast.ImportFrom) and n.module == "__future__"
    ]
    future_source = "\n".join(python_segment(solution, n) for n in future_nodes)
    if future_source:
        support_source = future_source + "\n\n" + support_source
    starter_roots = [
        n
        for n in starter_tree.body
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in roots
    ]
    if {n.name for n in starter_roots} != set(roots):
        raise ValueError(problem["Id"] + " missing Python starter roots")
    starter_source = (
        "\n\n".join(python_segment(starter, n) for n in starter_roots) + "\n"
    )
    # Standard-library imports used by algorithms belong with the editable code.
    # Starter annotations share those imports and supplied model bindings.
    imports = [
        n
        for n in solution_tree.body
        if id(n) in visible_ids and isinstance(n, (ast.Import, ast.ImportFrom))
    ]
    starter_import_parts = [python_segment(solution, n) for n in imports]
    additional_models = {
        name
        for name in starter_closure
        if name not in all_nodes
        and (
            isinstance(starter_nodes[name], ast.ClassDef)
            or isinstance(starter_nodes[name], ast.ImportFrom)
            and starter_nodes[name].module in PYTHON_MODEL_MODULES
            or isinstance(starter_nodes[name], (ast.Assign, ast.AnnAssign))
        )
    }
    extra_model_closure = closure(additional_models, starter_dependencies, set(roots))
    extra_model_ids = {id(starter_nodes[name]) for name in extra_model_closure}
    extra_prefix_parts = [
        python_segment(starter, n)
        for n in starter_tree.body
        if id(n) in extra_model_ids
    ]
    # Independently authored solutions sometimes omit annotations that are on
    # the original starter. Retain those starter-only typing imports explicitly.
    for node in starter_tree.body:
        if id(node) not in {id(starter_nodes[name]) for name in starter_closure}:
            continue
        if isinstance(node, (ast.Import, ast.ImportFrom)) and not (
            isinstance(node, ast.ImportFrom)
            and (
                node.module in PYTHON_MODEL_MODULES
                or (node.module or "").startswith("test_framework")
            )
        ):
            part = python_segment(starter, node)
            if part not in starter_import_parts:
                starter_import_parts.append(part)
    starter_imports = "\n".join(starter_import_parts)
    if starter_imports:
        starter_source = starter_imports + "\n\n" + starter_source
    # Imports in editable code cannot sit after prefix definitions if they are
    # future imports; they have already been moved to the support prelude.
    visible_source = (
        "\n\n".join(
            python_segment(solution, n)
            for n in solution_tree.body
            if id(n) in visible_ids and n not in future_nodes
        )
        + "\n"
    )
    references = [
        python_reference(name, all_nodes[name], solution) for name in sorted(supplied)
    ]
    references.extend(
        python_reference(name, starter_nodes[name], starter)
        for name in sorted(additional_models)
    )
    # Prefix definitions can reference the user's algorithm at call time. They
    # execute in the same module namespace and preserve framework node identity.
    extra_prefix = "\n\n".join(extra_prefix_parts)
    if future_source:
        support_source = support_source[len(future_source) :].lstrip()
    prefix = (
        "\n\n".join(
            part
            for part in (future_source, extra_prefix, support_source.rstrip())
            if part
        )
        + "\n\n"
    )
    if not prefix.strip():
        prefix = ""
    removed = sorted(
        name
        for name, node in all_nodes.items()
        if isinstance(node, (ast.FunctionDef, ast.ClassDef))
        and name not in visible_names
        and name not in support_names
    )
    return {
        "starterCode": starter_source,
        "solutionCode": visible_source,
        "prefix": prefix,
        "suffix": "",
        "references": references,
        "visibleSymbols": sorted(
            name
            for name in visible_names
            if isinstance(all_nodes[name], (ast.FunctionDef, ast.ClassDef))
        ),
        "hiddenSymbols": sorted(
            name
            for name in support_names
            if isinstance(all_nodes[name], (ast.FunctionDef, ast.ClassDef))
        ),
        "removedUnrelatedSymbols": removed,
        "signature": "\n".join(
            "class " + n.name
            if isinstance(n, ast.ClassDef)
            else "def "
            + n.name
            + "("
            + ast.unparse(n.args)
            + ")"
            + (" -> " + ast.unparse(n.returns) if n.returns else "")
            for n in starter_roots
        ),
    }


def make_entry(problem: dict, language: str, roots: list[str]) -> dict:
    problem_id = problem["Id"]
    path = Path("solutions") / language / (problem_id + "." + EXTENSIONS[language])
    solution = (ROOT / path).read_text(encoding="utf-8")
    starter_key = {
        "csharp": "StarterCode",
        "javascript": "JsStarterCode",
        "python": "PyStarterCode",
    }[language]
    signature_key = {
        "csharp": "Signature",
        "javascript": "JsSignature",
        "python": "PySignature",
    }[language]
    starter = problem[starter_key]
    item = {
        "problemId": problem_id,
        "language": language,
        "filename": "Solution.cs"
        if language == "csharp"
        else "solution." + EXTENSIONS[language],
        "signature": problem[signature_key],
        "starterCode": starter,
        "solutionCode": solution,
        "prefix": "",
        "suffix": "",
        "references": [],
        "visibleSymbols": [],
        "hiddenSymbols": [],
        "removedUnrelatedSymbols": [],
        "sourcePaths": [
            "EpiJudge.Runner/ProblemCatalog.cs"
            if problem_id in CURATED
            else "EpiJudge.Runner/catalog.json",
            path.as_posix(),
        ],
        "sourceSha256": {"starter": digest(starter), "solution": digest(solution)},
    }
    if language == "csharp":
        item["references"] = csharp_references(starter + "\n" + solution)
        item["starterCode"] = csharp_visible(starter)
        item["solutionCode"] = csharp_visible(solution)
        if item["references"]:
            item["prefix"] = "using EpiJudge.TestFramework;\n"
        item["visibleSymbols"] = top_symbols(solution, language)
    elif language == "javascript":
        starter_code, starter_exports = javascript_split(starter)
        solution_code, solution_exports = javascript_split(solution)
        if identifiers(starter_exports, language) != identifiers(
            solution_exports, language
        ):
            raise ValueError(problem_id + " JavaScript starter/solution exports differ")
        item.update(
            starterCode=starter_code,
            solutionCode=solution_code,
            suffix=solution_exports,
            visibleSymbols=top_symbols(solution_code, language),
        )
        needed = (
            identifiers(starter_code + "\n" + solution_code, language)
            & JAVASCRIPT_MODELS
        )
        needed.update(javascript_documented_models(starter_code + "\n" + solution_code))
        item["references"] = [
            {
                "title": "Supplied " + name,
                "code": javascript_model_sources()[name],
                "names": [name],
            }
            for name in sorted(needed)
        ]
    else:
        item.update(python_split(problem, solution, roots))
        item["sourcePaths"].extend(
            [
                "scripts/code_workspace/managed-roots.json",
                "epi_judge_python/" + problem["PySourceFile"],
            ]
        )
    item["starterCode"] = formatted(item["starterCode"], language)
    item["solutionCode"] = formatted(item["solutionCode"], language)
    for reference in item["references"]:
        reference["code"] = formatted(reference["code"], language)
    # The source envelope must parse as a normal legacy submission too.
    for kind in ("starterCode", "solutionCode"):
        program = item["prefix"] + item[kind] + item["suffix"]
        if language == "python":
            compile(program, "solution.py", "exec")
            if any(
                isinstance(n, ast.If)
                and any(
                    isinstance(x, ast.Name) and x.id == "__name__"
                    for x in ast.walk(n.test)
                )
                for n in ast.parse(item[kind]).body
            ):
                raise ValueError(problem_id + " exposes a Python judge entrypoint")
        elif parse(program, language).root_node.has_error:
            original = starter if kind == "starterCode" else solution
            # The pinned C# grammar incorrectly reserves the contextual keyword
            # `required` in a valid local assignment. The same checked-in source
            # is compiler-validated; formatting may not introduce another error.
            if language != "csharp" or parser_errors(
                program, language
            ) != parser_errors(original, language):
                raise ValueError(
                    problem_id + " invalid composed " + language + " program"
                )
    return item


def build() -> dict:
    roots = json.loads(
        (ROOT / "scripts/code_workspace/managed-roots.json").read_text(encoding="utf-8")
    )["roots"]
    inventory = problems()
    if set(roots) != {p["Id"] for p in inventory}:
        raise ValueError("Reviewed Python roots must cover all 218 live EPI questions")
    work = [(p, language, roots[p["Id"]]) for p in inventory for language in LANGUAGES]
    with ThreadPoolExecutor(max_workers=6) as executor:
        entries = list(executor.map(lambda args: make_entry(*args), work))
    if len(entries) != 654:
        raise ValueError("Managed workspace inventory must contain 654 distinct pairs")
    return {"schemaVersion": 1, "codeFormat": "callable-v1", "entries": entries}


def build_entries() -> list[dict]:
    """Central resource generation can combine this owned part without I/O."""
    return build()["entries"]


if __name__ == "__main__":
    output = build()
    path = ROOT / "workspace-code/parts/epi-managed.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        f"Recorded {len(output['entries'])} managed callable pairs / {len(output['entries']) * 2} visible artifacts."
    )
