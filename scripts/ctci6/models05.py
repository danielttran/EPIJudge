"""Explicit floating, sequence and packed-byte callable bindings."""

from textwrap import indent
from core import declaration, starter_body

KINDS = {
    "csharp": {
        "d": "double",
        "ai": "int[]",
        "bytes": "byte[]",
        "i": "int",
        "s": "string",
        "void": "void",
    },
    "java": {
        "d": "double",
        "ai": "int[]",
        "bytes": "byte[]",
        "i": "int",
        "s": "String",
        "void": "void",
    },
    "cpp": {
        "d": "double",
        "ai": "std::vector<int>",
        "bytes": "std::vector<std::uint8_t>",
        "i": "int",
        "s": "std::string",
        "void": "void",
    },
    "python": {
        "d": "float",
        "ai": "list[int]",
        "bytes": "bytearray",
        "i": "int",
        "s": "str",
        "void": "None",
    },
}


def declare(spec, language, body, class_name="Solution"):
    if spec["ref"] in ("5.1", "5.6", "5.7"):
        return declaration(spec, language, body, class_name)
    if language == "javascript":
        return declaration(spec, language, body, class_name)
    kinds = KINDS[language]
    if language == "python":
        signature = (
            "def "
            + spec["method"]
            + "("
            + ", ".join(n + ": " + kinds[t] for n, t in spec["params"])
            + ") -> "
            + kinds[spec["result"]]
        )
        return signature, signature + ":\n" + indent(body or "pass", "    ") + "\n"
    signature = (
        kinds[spec["result"]]
        + " "
        + spec["method"]
        + "("
        + ", ".join(
            kinds[t] + ("&" if language == "cpp" and t == "bytes" else "") + " " + n
            for n, t in spec["params"]
        )
        + ")"
    )
    method = (
        ("public " if language != "cpp" else "")
        + signature
        + " {\n"
        + indent(body, "    ")
        + "\n}"
    )
    return signature, (
        "public class " if language == "csharp" else "class "
    ) + class_name + " {\n" + ("public:\n" if language == "cpp" else "") + indent(
        method, "    "
    ) + ("\n};\n" if language == "cpp" else "\n}\n")


def neutral(spec, language):
    if spec["result"] == "ai":
        return {
            "csharp": "return [];",
            "java": "return new int[0];",
            "cpp": "return {};",
            "python": "return []",
            "javascript": "return [];",
        }[language]
    return starter_body(spec, language)
