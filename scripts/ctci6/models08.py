"""Chapter-eight sequence bindings, retaining existing primitive envelopes."""

from textwrap import indent
from core import HEADERS, declaration, starter_body

BASICS = ("8.1", "8.5", "8.11")
TYPES = {
    "csharp": dict(
        i="int", s="string", ai="int[]", sets="List<List<int>>", strings="List<string>"
    ),
    "java": dict(
        i="int",
        s="String",
        ai="int[]",
        sets="List<List<Integer>>",
        strings="List<String>",
    ),
    "cpp": dict(
        i="int",
        s="std::string",
        ai="std::vector<int>",
        sets="std::vector<std::vector<int>>",
        strings="std::vector<std::string>",
    ),
    "python": dict(
        i="int", s="str", ai="list[int]", sets="list[list[int]]", strings="list[str]"
    ),
}

for _language in TYPES:
    TYPES[_language]["as"] = {"csharp": "string[]", "java": "String[]", "cpp": "std::vector<std::string>", "python": "list[str]"}[_language]
    TYPES[_language]["arrangements"] = TYPES[_language]["sets"]
    TYPES[_language]["path"] = TYPES[_language]["sets"]
    TYPES[_language]["b"] = {
        "csharp": "bool",
        "java": "boolean",
        "cpp": "bool",
        "python": "bool",
    }[_language]
    TYPES[_language]["aai"] = {
        "csharp": "int[][]",
        "java": "int[][]",
        "cpp": "std::vector<std::vector<int>>",
        "python": "list[list[int]]",
    }[_language]


def header(ref, language):
    return HEADERS[language] + (
        "#include <cstdint>\n"
        + ("#include <functional>\n#include <utility>\n" if ref not in BASICS else "")
        if language == "cpp"
        else ""
    )


def declare(spec, language, body, class_name="Solution"):
    if spec["ref"] in BASICS or language == "javascript":
        return declaration(spec, language, body, class_name)
    types = TYPES[language]
    if language == "python":
        signature = (
            "def "
            + spec["method"]
            + "("
            + ", ".join(n + ": " + types[t] for n, t in spec["params"])
            + ") -> "
            + types[spec["result"]]
        )
        return signature, signature + ":\n" + indent(body or "pass", "    ") + "\n"
    signature = (
        types[spec["result"]]
        + " "
        + spec["method"]
        + "("
        + ", ".join(
            ("const " if language == "cpp" and t in ("s", "ai", "aai", "as") and not (index == 0 and spec["mutation"] in ("screen", "first-array")) else "")
            + types[t]
            + ("&" if language == "cpp" and t in ("s", "ai", "aai", "as") else "")
            + " "
            + n
            for index, (n, t) in enumerate(spec["params"])
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
    if spec["result"] not in ("sets", "strings", "arrangements", "path", "aai"):
        return starter_body(spec, language)
    if spec["result"] == "aai" and language == "java":
        return "return new int[0][];"
    return {
        "csharp": "return [];",
        "java": "return new ArrayList<>();",
        "cpp": "return {};",
        "python": "return []",
        "javascript": "return [];",
    }[language]
