"""Generate clean EPI C++/Java callables and bank-owned execution envelopes.

Only checked-in source is parsed.  Existing user programs retain the legacy
runner path; this module never reads or rewrites a draft.  Tree-sitter ranges
identify declarations, supplied models, annotations and algorithm dependencies.
The validated owned solution supplies every hidden judge body.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    from .common import ROOT, format_code, parse, text_of
except ImportError:
    from common import ROOT, format_code, parse, text_of


COMMENTS = {"comment", "line_comment", "block_comment"}
JAVA_TYPES = {
    "class_declaration",
    "enum_declaration",
    "interface_declaration",
    "record_declaration",
}
CPP_TYPES = {"class_specifier", "struct_specifier", "enum_specifier"}
IDENTIFIERS = {
    "identifier",
    "type_identifier",
    "namespace_identifier",
    "field_identifier",
}
JUDGE_NAMES = {
    "main",
    "GenericTest",
    "GenericTestMain",
    "TimedExecutor",
    "TestFailure",
    "SerializationTrait",
    "EpiTest",
    "EpiTestComparator",
    "EpiUserType",
    "CheckSequenceIsUniformlyRandom",
    "CheckSequenceIsUniformlyRandomWrapper",
}
SUPPLIED_PRIMITIVES = {
    ("cpp", "uniform_random_number"): {"ZeroOneRandom"},
    ("java", "uniform_random_number"): {"zeroOneRandom"},
}


def walk(node):
    yield node
    for child in node.named_children:
        yield from walk(child)


def identifiers(node, source: str) -> set[str]:
    return {text_of(n, source) for n in walk(node) if n.type in IDENTIFIERS}


def name_of(node, source: str) -> str | None:
    """Read a declared name from grammar fields, never textual source matching."""
    name = node.child_by_field_name("name")
    if name is not None:
        return text_of(name, source)
    if node.type == "namespace_definition":
        return None
    declarator = node.child_by_field_name("declarator")
    if declarator is not None:
        return declarator_name(declarator, source)
    if node.type == "template_declaration":
        for child in reversed(node.named_children):
            found = name_of(child, source)
            if found:
                return found
    return None


def declarator_name(node, source: str) -> str | None:
    if node.type in IDENTIFIERS | {"operator_name", "destructor_name"}:
        return text_of(node, source)
    if node.type == "qualified_identifier":
        return text_of(node.child_by_field_name("name"), source)
    declarator = node.child_by_field_name("declarator")
    if declarator is not None:
        return declarator_name(declarator, source)
    for child in node.named_children:
        if child.type not in {
            "parameter_list",
            "argument_list",
            "template_argument_list",
        }:
            found = declarator_name(child, source)
            if found:
                return found
    return None


def annotation_names(node, source: str) -> set[str]:
    return {
        text_of(n.child_by_field_name("name"), source)
        for n in walk(node)
        if n.type in {"annotation", "marker_annotation"}
        and n.child_by_field_name("name") is not None
    }


def without_annotations(node, source: str, names: set[str]) -> str:
    edits = [
        (n.start_byte, n.end_byte)
        for n in walk(node)
        if n.type in {"annotation", "marker_annotation"}
        and n.child_by_field_name("name") is not None
        and text_of(n.child_by_field_name("name"), source) in names
    ]
    data = source.encode("utf-8")
    cursor = node.start_byte
    parts = []
    for start, end in sorted(edits):
        parts.append(data[cursor:start])
        cursor = end
    parts.append(data[cursor : node.end_byte])
    return b"".join(parts).decode("utf-8").strip()


@dataclass
class Declaration:
    node: Any
    name: str | None
    names: set[str]
    code: str
    refs: set[str]
    is_type: bool
    is_function: bool


def declaration(node, source: str, language: str) -> Declaration:
    name = name_of(node, source)
    names = {name} if name else set()
    if language == "java" and node.type == "field_declaration":
        names = {
            text_of(n.child_by_field_name("name"), source)
            for n in node.named_children
            if n.type == "variable_declarator"
        }
    if node.type == "namespace_definition" and name != "test_framework":
        body = node.child_by_field_name("body")
        if body is not None:
            names |= {name_of(n, source) for n in body.named_children} - {None}
    code = text_of(node, source).strip()
    if language == "cpp" and node.type in CPP_TYPES:
        code += ";"
    is_type = node.type in (JAVA_TYPES if language == "java" else CPP_TYPES)
    if language == "cpp" and node.type == "template_declaration":
        is_type = any(n.type in CPP_TYPES for n in node.named_children)
    return Declaration(
        node,
        name,
        names,
        code,
        identifiers(node, source),
        is_type,
        node.type
        in {"function_definition", "method_declaration", "constructor_declaration"}
        or (
            node.type == "template_declaration"
            and any(n.type == "function_definition" for n in node.named_children)
        ),
    )


def function_node(node):
    if node.type in {
        "function_definition",
        "method_declaration",
        "constructor_declaration",
    }:
        return node
    if node.type == "template_declaration":
        return next(
            (n for n in node.named_children if n.type == "function_definition"), None
        )
    return None


def signature_identifiers(node, source: str) -> set[str]:
    fn = function_node(node)
    if fn is not None:
        body = fn.child_by_field_name("body")
        return {
            text_of(n, source)
            for n in walk(fn)
            if n.type in IDENTIFIERS and (body is None or n.end_byte <= body.start_byte)
        }
    return set()


def require_tree(source: str, language: str, label: str):
    tree = parse(source, language)
    if tree.root_node.has_error:
        errors = [
            f"{n.type}@{n.start_point.row + 1}:{n.start_point.column + 1}"
            for n in walk(tree.root_node)
            if n.type == "ERROR" or n.is_missing
        ]
        raise ValueError(f"Cannot parse {label}: {errors[:8]}")
    return tree


def cpp_scope(tree, source: str):
    # Huffman is the sole named algorithm namespace in the live EPI inventory.
    # Anonymous helper namespaces remain atomic dependency declarations.
    for node in tree.root_node.named_children:
        if node.type == "namespace_definition" and "TODO" in text_of(node, source):
            name = node.child_by_field_name("name")
            if name is not None and text_of(name, source) != "test_framework":
                return node, node.child_by_field_name("body")
    return tree.root_node, tree.root_node


def java_scope(tree, source: str):
    classes = [
        n for n in tree.root_node.named_children if n.type == "class_declaration"
    ]
    for node in classes:
        if "TODO" in text_of(node, source):
            return node, node.child_by_field_name("body")
    raise ValueError("The original Java starter has no TODO-containing class.")


def matching_scope(
    tree, source: str, language: str, starter_container, starter_source: str
):
    if language == "cpp" and starter_container.type == "translation_unit":
        return tree.root_node, tree.root_node
    target = name_of(starter_container, starter_source)
    expected_type = starter_container.type
    found = next(
        (
            n
            for n in tree.root_node.named_children
            if n.type == expected_type and name_of(n, source) == target
        ),
        None,
    )
    if found is None:
        raise ValueError(f"Missing solution scope {target}")
    return found, found.child_by_field_name("body")


def declarations(body, source: str, language: str) -> list[Declaration]:
    excluded = COMMENTS | {
        "package_declaration",
        "import_declaration",
        "preproc_include",
        "using_declaration",
    }
    return [
        declaration(n, source, language)
        for n in body.named_children
        if n.type not in excluded
        and not (n.type == "expression_statement" and text_of(n, source).strip() == ";")
    ]


def algorithm_roots(starter_decls: list[Declaration]) -> set[str]:
    roots = set()
    for decl in starter_decls:
        if "TODO" in decl.code:
            roots |= decl.names
    if not roots:
        raise ValueError("No algorithm declarations contain TODO anchors.")
    return roots


def choose_algorithms(
    decls: list[Declaration],
    roots: set[str],
    starter_decls: list[Declaration],
    language: str,
    problem_id: str,
    source: str,
):
    by_name: dict[str, list[int]] = {}
    for i, decl in enumerate(decls):
        for name in decl.names:
            by_name.setdefault(name, []).append(i)
    missing = roots - by_name.keys()
    if missing:
        raise ValueError(
            f"{problem_id}/{language}: solution misses algorithm roots {missing}"
        )
    selected = {i for root in roots for i in by_name[root]}
    supplied = set()
    root_signatures = set()
    for i in selected:
        root_signatures |= signature_identifiers(decls[i].node, source)
    # A model is supplied only if it exists in the original starter and forms
    # part of the public input/output API.  Algorithm-only helper types stay
    # visible even when the original starter happened to predeclare them.
    for i, decl in enumerate(decls):
        if decl.is_type and decl.name in root_signatures and not decl.names & roots:
            supplied.add(i)
    primitive_names = SUPPLIED_PRIMITIVES.get((language, problem_id), set())
    supplied |= {i for i, decl in enumerate(decls) if decl.names & primitive_names}
    # A constructor and its field dependencies belong to an outer stateful
    # algorithm class, rather than to the bank's serialization adapters.
    if language == "java" and any(
        d.node.type == "constructor_declaration" for d in decls
    ):
        selected |= {
            i for i, d in enumerate(decls) if d.node.type == "constructor_declaration"
        }
    changed = True
    while changed:
        changed = False
        refs = set().union(*(decls[i].refs for i in selected))
        for ref in refs:
            for i in by_name.get(ref, []):
                if i not in selected and i not in supplied:
                    if decls[i].name == "main":
                        raise ValueError("An algorithm unexpectedly depends on main.")
                    selected.add(i)
                    changed = True
    return selected, supplied


def java_test_adapter(decl: Declaration, source: str) -> str | None:
    node = decl.node
    if node.type != "method_declaration" or "EpiTest" not in annotation_names(
        node, source
    ):
        return None
    body = node.child_by_field_name("body")
    name = node.child_by_field_name("name")
    params = node.child_by_field_name("parameters")
    result = node.child_by_field_name("type")
    arguments = [
        text_of(n.child_by_field_name("name"), source)
        for n in params.named_children
        if n.type in {"formal_parameter", "spread_parameter"}
    ]
    data = source.encode("utf-8")
    header = (
        data[node.start_byte : name.start_byte]
        + b"__bankCase"
        + data[name.end_byte : body.start_byte]
    ).decode("utf-8")
    invocation = f"{decl.name}({', '.join(arguments)})"
    statement = (
        invocation + ";"
        if text_of(result, source) == "void"
        else "return " + invocation + ";"
    )
    return header + "{\n" + statement + "\n}"


def declaration_signature(decl: Declaration, source: str, language: str) -> list[str]:
    fn = function_node(decl.node)
    if fn is not None:
        body = fn.child_by_field_name("body")
        if body is not None:
            # Byte range of the body is used, not a textual brace search.
            initializer = next(
                (n for n in fn.named_children if n.type == "field_initializer_list"),
                None,
            )
            end = initializer.start_byte if initializer is not None else body.start_byte
            prefix = source.encode("utf-8")[fn.start_byte : end].decode("utf-8")
            for annotation in [
                n for n in walk(fn) if n.type in {"annotation", "marker_annotation"}
            ]:
                if annotation.end_byte <= body.start_byte:
                    prefix = prefix.replace(text_of(annotation, source), "")
            return [" ".join(prefix.split()).rstrip()]
    if decl.is_type:
        body = decl.node.child_by_field_name("body")
        api = []
        if body is not None:
            public = language == "java"
            for member in body.named_children:
                if member.type == "access_specifier":
                    public = text_of(member, source) == "public"
                if member.type in {
                    "function_definition",
                    "method_declaration",
                    "constructor_declaration",
                    "declaration",
                    "field_declaration",
                }:
                    if language == "java":
                        mods = next(
                            (n for n in member.named_children if n.type == "modifiers"),
                            None,
                        )
                        public = mods is None or "private" not in text_of(mods, source)
                    if public and function_node(member) is not None:
                        api += declaration_signature(
                            declaration(member, source, language), source, language
                        )
        return [f"{decl.name}: " + "; ".join(api)]
    return []


def refs_for(decls: list[Declaration], supplied: set[int], source: str, language: str):
    refs = []
    for i in sorted(supplied):
        decl = decls[i]
        code = without_annotations(
            decl.node, source, {"EpiUserType", "EpiTest", "EpiTestComparator"}
        )
        if language == "cpp" and decl.node.type in CPP_TYPES:
            code += ";"
        refs.append(
            {
                "title": f"Provided {decl.name}",
                "code": format_code(code, language),
                "names": sorted(decl.names),
            }
        )
    return refs


def model_outline(node, source: str, language: str) -> str:
    """Show relevant fields/constructors, not equality/printing/framework code."""
    original = node
    if node.type == "template_declaration":
        node = next(n for n in node.named_children if n.type in CPP_TYPES)
    body = node.child_by_field_name("body")
    name = name_of(node, source)
    data = source.encode("utf-8")
    header = data[original.start_byte : body.start_byte].decode("utf-8")
    if language == "java":
        superclass = node.child_by_field_name("superclass")
        if superclass is not None:
            header = (
                data[original.start_byte : superclass.start_byte]
                + data[superclass.end_byte : body.start_byte]
            ).decode("utf-8")
    fields = []
    for member in body.named_children:
        if (
            member.type == "field_declaration"
            and not any(n.type == "function_declarator" for n in walk(member))
            or member.type == "constructor_declaration"
            or member.type == "function_definition"
            and name_of(member, source) == name
        ):
            fields.append(text_of(member, source))
    return (
        "// Relevant fields and constructors of the supplied type.\n"
        + header
        + "{\n"
        + ("public:\n" if language == "cpp" and node.type == "class_specifier" else "")
        + "\n\n".join(fields)
        + "\n}"
        + (";" if language == "cpp" else "")
    )


def external_references(
    roots: list[Declaration], source: str, language: str, existing: set[str]
):
    needed = set().union(*(signature_identifiers(d.node, source) for d in roots))
    needed &= {"ListNode", "BinaryTreeNode", "BinaryTree", "BstNode", "PostingListNode"}
    needed -= existing
    refs = []
    if language == "cpp":
        tree = parse(source, language)
        paths = []
        for node in tree.root_node.named_children:
            if node.type == "preproc_include":
                path_node = node.child_by_field_name("path")
                if path_node is not None and path_node.type == "string_literal":
                    raw = text_of(path_node, source)
                    path = ROOT / "epi_judge_cpp" / raw[1:-1]
                    if path.is_file() and path.parent == ROOT / "epi_judge_cpp":
                        paths.append(path)
    else:
        paths = [
            ROOT / "epi_judge_java/epi" / (name + ".java") for name in sorted(needed)
        ]
    for path in paths:
        text = path.read_text(encoding="utf-8")
        # Supplied C++ headers use trailing declaration macros.  Parse the
        # complete known header, then select its concrete model declaration;
        # macro expansion is irrelevant to this read-only type reference.
        tree = parse(text, language)
        for node in tree.root_node.named_children:
            declared = name_of(node, text)
            if declared in needed and (
                node.type in JAVA_TYPES | CPP_TYPES
                or node.type == "template_declaration"
            ):
                refs.append(
                    {
                        "title": f"Provided {declared} — fields and constructors",
                        "code": format_code(
                            model_outline(node, text, language), language
                        ),
                        "names": [declared],
                        "sourcePath": path.relative_to(ROOT).as_posix(),
                        "sourceSha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                    }
                )
                needed.remove(declared)
    if needed:
        raise ValueError(f"Missing supplied model references {needed}/{language}")
    return refs


def renamed_code(decl: Declaration, source: str, replacements: dict[str, str]) -> str:
    """Rename known bank-owned AST identifiers; never inspect user code."""
    data = source.encode("utf-8")
    cursor = decl.node.start_byte
    parts = []
    for node in walk(decl.node):
        if node.type in IDENTIFIERS and text_of(node, source) in replacements:
            parts.append(data[cursor : node.start_byte])
            parts.append(replacements[text_of(node, source)].encode("utf-8"))
            cursor = node.end_byte
    parts.append(data[cursor : decl.node.end_byte])
    result = b"".join(parts).decode("utf-8")
    if decl.node.type in CPP_TYPES:
        result += ";"
    return result


def hidden_partition(
    decls: list[Declaration],
    selected: set[int],
    supplied: set[int],
    roots: set[str],
    source: str,
    language: str,
):
    """Keep the reachable judge and isolate helpers shared with its checks.

    A checker must not accidentally call an editable algorithm helper (for
    example Gray Code's one-bit predicate).  Its private, renamed bank copy
    preserves the validated checker and also lets a minimal starter compile.
    Unused demonstration algorithms are omitted from the hidden envelope.
    """
    by_name: dict[str, set[int]] = {}
    for i, decl in enumerate(decls):
        for name in decl.names:
            by_name.setdefault(name, set()).add(i)
    hidden = set(range(len(decls))) - selected
    active = {
        i
        for i in hidden
        if decls[i].name == "main"
        or i in supplied
        or (decls[i].name is not None and decls[i].name.startswith("operator"))
        or (
            language == "java"
            and annotation_names(decls[i].node, source)
            & {"EpiTest", "EpiTestComparator", "EpiTestExpectedType"}
        )
        or not decls[i].is_function
    }
    clones = set()
    changed = True
    while changed:
        changed = False
        refs = set().union(*(decls[i].refs for i in active | clones))
        for name in refs - roots:
            for i in by_name.get(name, set()):
                if i in hidden and i not in active:
                    active.add(i)
                    changed = True
                elif (
                    i in selected
                    and i not in clones
                    and decls[i].node.type != "constructor_declaration"
                ):
                    clones.add(i)
                    changed = True
    replacements = {name: "__bank_" + name for i in clones for name in decls[i].names}
    # Some bank-only operation records have methods that use the submitted
    # stateful class.  Keep those records (and serializers depending on them)
    # after the user declaration, rather than moving them into its prelude.
    selected_names = set().union(*(decls[i].names for i in selected))
    needs_after = {i for i in active if decls[i].refs & selected_names}
    changed = True
    while changed:
        changed = False
        late_names = set().union(*(decls[i].names for i in needs_after))
        for i in active - needs_after:
            if decls[i].refs & late_names:
                needs_after.add(i)
                changed = True
    before, after = [], []
    for i, decl in enumerate(decls):
        if i in active:
            code = renamed_code(decl, source, replacements)
            if i not in needs_after and (
                decl.is_type
                or i in supplied
                or decl.node.type in {"namespace_definition", "alias_declaration"}
                or (not decl.is_function and decl.name != "main")
            ):
                before.append(code)
            else:
                after.append(code)
    clone_code = [renamed_code(decls[i], source, replacements) for i in sorted(clones)]
    # Declarations precede any checker using them.  C++ definition ordering is
    # retained, including original forward declarations in the dependency set.
    after = clone_code + after
    for i in selected:
        adapter = java_test_adapter(decls[i], source) if language == "java" else None
        if adapter:
            after.insert(0, adapter)
    return before, after


def stub_method(node, source: str, language: str) -> str:
    body = node.child_by_field_name("body")
    if body is None:
        return text_of(node, source)
    data = source.encode("utf-8")
    header = data[node.start_byte : body.start_byte].decode("utf-8")
    if language == "java":
        header_node = node
        for annotation in [
            n
            for n in walk(header_node)
            if n.type in {"annotation", "marker_annotation"}
            and n.end_byte <= body.start_byte
        ]:
            if text_of(annotation.child_by_field_name("name"), source) in {
                "EpiTest",
                "EpiTestComparator",
                "EpiUserType",
            }:
                header = header.replace(text_of(annotation, source), "")
        statement = 'throw new UnsupportedOperationException("Implement this method");'
    else:
        # Constructor member initializers are implementation, not callable API.
        initializer = next(
            (n for n in node.named_children if n.type == "field_initializer_list"), None
        )
        if initializer is not None:
            header = data[node.start_byte : initializer.start_byte].decode("utf-8")
        statement = 'throw std::logic_error("Implement this method");'
    return (
        header.strip()
        + " {\n    // Write your solution here.\n    "
        + statement
        + "\n}"
    )


def stub_declaration(decl: Declaration, source: str, language: str) -> str:
    fn = function_node(decl.node)
    if fn is not None:
        return stub_method(fn, source, language)
    if decl.is_type:
        node = decl.node
        body = node.child_by_field_name("body")
        if body is None:
            raise ValueError(f"Algorithm class {decl.name} has no body.")
        data = source.encode("utf-8")
        header = data[node.start_byte : body.start_byte].decode("utf-8")
        public = language == "java" or node.type == "struct_specifier"
        members = []
        for member in body.named_children:
            if member.type == "access_specifier":
                public = text_of(member, source) == "public"
            elif function_node(member) is not None:
                if language == "java":
                    mods = next(
                        (n for n in member.named_children if n.type == "modifiers"),
                        None,
                    )
                    public = mods is None or "private" not in text_of(mods, source)
                if public:
                    members.append(stub_method(function_node(member), source, language))
        return (
            header
            + "{\n"
            + ("public:\n" if language == "cpp" else "")
            + "\n\n".join(members)
            + "\n}"
            + (";" if language == "cpp" else "")
        )
    raise ValueError(
        f"Unsupported algorithm root declaration {decl.name}/{decl.node.type}"
    )


def split_entry(row: dict[str, Any]) -> dict[str, Any]:
    language, problem_id = row["language"], row["problemId"]
    starter_path = (
        ROOT
        / ("epi_judge_cpp" if language == "cpp" else "epi_judge_java/epi")
        / row["filename"]
    )
    solution_path = ROOT / row["codePath"]
    starter_source = starter_path.read_text(encoding="utf-8")
    solution_source = solution_path.read_text(encoding="utf-8")
    starter_tree = require_tree(starter_source, language, str(starter_path))
    solution_tree = require_tree(solution_source, language, str(solution_path))
    scope = cpp_scope if language == "cpp" else java_scope
    starter_container, starter_body = scope(starter_tree, starter_source)
    container, body = matching_scope(
        solution_tree, solution_source, language, starter_container, starter_source
    )
    sdecls = declarations(starter_body, starter_source, language)
    decls = declarations(body, solution_source, language)
    roots = algorithm_roots(sdecls)
    selected, supplied = choose_algorithms(
        decls, roots, sdecls, language, problem_id, solution_source
    )
    selected_names = set().union(*(decls[i].names for i in selected))
    # Build an empty scaffold from the canonical callable API.  This avoids
    # stale upstream type aliases and includes newly required state-reset APIs,
    # without giving a starter any algorithm implementation or helper bodies.
    starter_roots = [
        d
        for d in decls
        if d.names & roots and (d.is_type or function_node(d.node) is not None)
    ]
    if language == "java":
        starter_roots += [d for d in decls if d.node.type == "constructor_declaration"]
    starter_stubs = {
        id(d): stub_declaration(d, solution_source, language) for d in starter_roots
    }
    starter_code = "\n\n".join(starter_stubs.values())
    if language == "cpp":
        # Canonical return/parameter types may use a local alias. Retain just
        # the aliases needed by the empty public API, including alias chains;
        # implementation-only helper declarations still stay out of starters.
        refs = identifiers(parse(starter_code, language).root_node, starter_code)
        aliases = set()
        changed = True
        while changed:
            changed = False
            for i, decl in enumerate(decls):
                if (
                    i in selected
                    and i not in aliases
                    and decl.node.type in {"alias_declaration", "type_definition"}
                    and decl.names & refs
                ):
                    aliases.add(i)
                    refs |= decl.refs
                    changed = True
        starter_code = "\n\n".join(
            d.code if i in aliases else starter_stubs[id(d)]
            for i, d in enumerate(decls)
            if i in aliases or id(d) in starter_stubs
        )
    solution_code = "\n\n".join(
        without_annotations(
            d.node, solution_source, {"EpiTest", "EpiUserType", "EpiTestComparator"}
        )
        + (";" if language == "cpp" and d.node.type in CPP_TYPES else "")
        for i, d in enumerate(decls)
        if i in selected
    )
    starter_code = format_code(starter_code, language)
    solution_code = format_code(solution_code, language)

    # Put supplied declarations before the snippet, then preserve every hidden
    # function/checker in the validated solution after it.  Function prototypes
    # selected by dependency closure remain visible in their original order.
    before, after = hidden_partition(
        decls, selected, supplied, roots, solution_source, language
    )
    source_data = solution_source.encode("utf-8")
    if container.type == "translation_unit":
        imports = list(
            dict.fromkeys(
                [
                    text_of(n, solution_source)
                    for n in container.named_children
                    if n.type in {"preproc_include", "using_declaration"}
                ]
                + [
                    text_of(n, starter_source)
                    for n in starter_container.named_children
                    if n.type in {"preproc_include", "using_declaration"}
                ]
            )
        )
        prefix = (
            "#include <stdexcept>\n"
            + "\n".join(imports)
            + "\n\n"
            + "\n\n".join(before)
            + "\n\n"
        )
        suffix = "\n\n" + "\n\n".join(after) + "\n"
    else:
        prefix = source_data[: container.start_byte].decode("utf-8")
        if language == "java":
            existing_imports = {
                text_of(n, solution_source)
                for n in solution_tree.root_node.named_children
                if n.type == "import_declaration"
            }
            prefix += (
                "\n".join(
                    text_of(n, starter_source)
                    for n in starter_tree.root_node.named_children
                    if n.type == "import_declaration"
                    and text_of(n, starter_source) not in existing_imports
                )
                + "\n"
            )
        prefix += (
            source_data[container.start_byte : body.start_byte + 1].decode("utf-8")
            + "\n"
        )
        prefix += "\n\n".join(before) + "\n\n"
        suffix = "\n\n" + "\n\n".join(after) + "\n"
        suffix += source_data[body.end_byte - 1 :].decode("utf-8")
    if language == "cpp":
        prefix += '#line 1 "solution.cpp"\n'
        suffix = '\n#line 1 "judge.cpp"\n' + suffix
    signature = "; ".join(
        sig
        for d in starter_roots
        for sig in declaration_signature(d, solution_source, language)
    )
    hidden_names = set().union(
        *(d.names for i, d in enumerate(decls) if i not in selected)
    )
    references = refs_for(decls, supplied, solution_source, language)
    referenced_names = set().union(*(set(r["names"]) for r in references))
    references += external_references(
        starter_roots, solution_source, language, referenced_names
    )
    referenced_names = set().union(*(set(r["names"]) for r in references))
    entry = {
        "problemId": problem_id,
        "language": language,
        "filename": row["filename"],
        "signature": signature,
        "starterCode": starter_code,
        "solutionCode": solution_code,
        "prefix": prefix,
        "suffix": suffix,
        "references": references,
        "visibleSymbols": sorted(selected_names),
        "hiddenSymbols": sorted(hidden_names),
        "sourcePaths": [
            starter_path.relative_to(ROOT).as_posix(),
            solution_path.relative_to(ROOT).as_posix(),
        ]
        + [r["sourcePath"] for r in references if "sourcePath" in r],
        "sourceSha256": {
            "starter": hashlib.sha256(starter_path.read_bytes()).hexdigest(),
            "solution": hashlib.sha256(solution_path.read_bytes()).hexdigest(),
        },
        "removedUnrelatedSymbols": sorted(hidden_names - referenced_names),
    }
    selfcheck(entry)
    return entry


def selfcheck(entry):
    for kind in ("starterCode", "solutionCode"):
        code = entry[kind]
        tree = parse(
            ("class __Visible {\n" + code + "\n}")
            if entry["language"] == "java"
            else code,
            entry["language"],
        )
        if tree.root_node.has_error:
            raise ValueError(
                f"Invalid visible {kind}: {entry['problemId']}/{entry['language']}"
            )
        leaked = (
            identifiers(
                tree.root_node,
                ("class __Visible {\n" + code + "\n}")
                if entry["language"] == "java"
                else code,
            )
            & JUDGE_NAMES
        )
        if leaked:
            raise ValueError(
                f"Visible judge glue {leaked}: {entry['problemId']}/{entry['language']}/{kind}"
            )
        if any(len(line) > 120 for line in code.splitlines()):
            raise ValueError(
                f"Unreadable long line: {entry['problemId']}/{entry['language']}/{kind}"
            )
        require_tree(
            entry["prefix"] + code + entry["suffix"],
            entry["language"],
            f"composed {entry['problemId']}/{entry['language']}/{kind}",
        )


def build_entries():
    rows = json.loads((ROOT / "solutions/coverage.json").read_text(encoding="utf-8"))[
        "entries"
    ]
    selected = [
        r for r in rows if r["collection"] == "epi" and r["language"] in {"cpp", "java"}
    ]
    if len(selected) != 436:
        raise ValueError(f"Expected 436 EPI native pairs, got {len(selected)}")
    return [split_entry(row) for row in selected]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, default=ROOT / "workspace-code/parts/epi-native.json"
    )
    parser.add_argument(
        "--problem",
        action="append",
        help="Diagnostic subset; not valid as final inventory.",
    )
    args = parser.parse_args()
    if args.problem:
        rows = json.loads(
            (ROOT / "solutions/coverage.json").read_text(encoding="utf-8")
        )["entries"]
        entries = [
            split_entry(r)
            for r in rows
            if r["collection"] == "epi"
            and r["language"] in {"cpp", "java"}
            and r["problemId"] in args.problem
        ]
    else:
        entries = build_entries()
    data = {"schemaVersion": 1, "codeFormat": "callable-v1", "entries": entries}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    pending_output = args.output.with_name(args.output.name + ".tmp")
    pending_output.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    pending_output.replace(args.output)
    print(
        f"Generated {len(entries)} native pairs/{len(entries) * 2} visible artifacts: {args.output}"
    )


if __name__ == "__main__":
    main()
