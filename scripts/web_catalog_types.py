"""Shared TSV-to-C# type helpers for the website catalog."""
from typing import List, Optional


def split_types(value: str) -> List[str]:
    parts = []
    depth = 0
    start = 0
    for index, character in enumerate(value):
        if character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
        elif character == "," and depth == 0:
            parts.append(value[start:index].strip())
            start = index + 1
    parts.append(value[start:].strip())
    return parts


def inner_type(value: str, name: str) -> Optional[str]:
    prefix = name + "("
    if value.startswith(prefix) and value.endswith(")"):
        return value[len(prefix):-1]
    return None


def csharp_type(grammar: str, nullable_node: bool = True) -> str:
    primitive = {
        "bool": "bool",
        "float": "double",
        "int": "int",
        "long": "long",
        "string": "string",
    }
    if grammar in primitive:
        return primitive[grammar]
    inner = inner_type(grammar, "array")
    if inner is not None:
        return f"List<{csharp_type(inner)}>"
    inner = inner_type(grammar, "set")
    if inner is not None:
        return f"HashSet<{csharp_type(inner)}>"
    inner = inner_type(grammar, "binary_tree")
    if inner is not None:
        suffix = "?" if nullable_node else ""
        return f"BinaryTreeNode<{csharp_type(inner)}>{suffix}"
    inner = inner_type(grammar, "linked_list")
    if inner is not None:
        suffix = "?" if nullable_node else ""
        return f"ListNode<{csharp_type(inner)}>{suffix}"
    inner = inner_type(grammar, "tuple")
    if inner is not None:
        parts = split_types(inner)
        if not 2 <= len(parts) <= 4:
            raise ValueError(f"Unsupported tuple type: {grammar}")
        return f"({', '.join(csharp_type(part) for part in parts)})"
    if grammar == "void":
        return "void"
    raise ValueError(f"Unsupported type in catalog: {grammar}")
