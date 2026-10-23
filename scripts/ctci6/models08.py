"""Chapter-eight sequence bindings, retaining existing primitive envelopes."""

from textwrap import indent
from core import HEADERS, declaration, starter_body

COMBINATORIAL = ("8.4", "8.7", "8.8", "8.9")
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


def header(ref, language):
    return HEADERS[language] + (
        "#include <cstdint>\n"
        + (
            "#include <functional>\n#include <utility>\n"
            if ref in COMBINATORIAL
            else ""
        )
        if language == "cpp"
        else ""
    )


def declare(spec, language, body, class_name="Solution"):
    if spec["ref"] not in COMBINATORIAL or language == "javascript":
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
            ("const " if language == "cpp" and t in ("s", "ai") else "")
            + types[t]
            + ("&" if language == "cpp" and t in ("s", "ai") else "")
            + " "
            + n
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
    if spec["ref"] not in COMBINATORIAL:
        return starter_body(spec, language)
    return {
        "csharp": "return [];",
        "java": "return new ArrayList<>();",
        "cpp": "return {};",
        "python": "return []",
        "javascript": "return [];",
    }[language]
