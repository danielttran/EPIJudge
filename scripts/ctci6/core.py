"""Typed independent authoring support. No user drafts are parsed or rewritten."""

from pathlib import Path
from textwrap import indent

ROOT = Path(__file__).resolve().parents[2]
LANGUAGES = ("csharp", "javascript", "python", "cpp", "java")
EXT = dict(csharp="cs", javascript="js", python="py", cpp="cpp", java="java")
TYPES = {
    "csharp": dict(
        s="string", i="int", b="bool", chars="char[]", aai="int[][]", void="void"
    ),
    "java": dict(
        s="String", i="int", b="boolean", chars="char[]", aai="int[][]", void="void"
    ),
    "cpp": dict(
        s="std::string",
        i="int",
        b="bool",
        chars="std::vector<char>",
        aai="std::vector<std::vector<int>>",
        void="void",
    ),
    "python": dict(
        s="str",
        i="int",
        b="bool",
        chars="list[str]",
        aai="list[list[int]]",
        void="None",
    ),
}
HEADERS = {
    "csharp": "using System;\nusing System.Collections.Generic;\nusing System.Text;\n",
    "java": "import java.util.*;\n",
    "cpp": "#include <algorithm>\n#include <array>\n#include <string>\n#include <vector>\n",
    "python": "",
    "javascript": "'use strict';\n",
}


def declaration(spec, language, body, class_name="Solution"):
    name, params, result = spec["method"], spec["params"], spec["result"]
    if language == "python":
        signature = (
            "def "
            + name
            + "("
            + ", ".join(n + ": " + TYPES[language][t] for n, t in params)
            + ") -> "
            + TYPES[language][result]
        )
        return signature, signature + ":\n" + indent(body or "pass", "    ") + "\n"
    if language == "javascript":
        signature = "function " + name + "(" + ", ".join(n for n, _ in params) + ")"
        return signature, signature + " {\n" + indent(body, "  ") + "\n}\n"
    types = TYPES[language]
    typed = []
    for n, t in params:
        prefix, suffix = (
            ("const ", "&")
            if language == "cpp" and t == "s"
            else ("", "&")
            if language == "cpp" and t in ("chars", "aai")
            else ("", "")
        )
        typed.append(prefix + types[t] + suffix + " " + n)
    signature = types[result] + " " + name + "(" + ", ".join(typed) + ")"
    method = (
        ("public " if language != "cpp" else "")
        + signature
        + " {\n"
        + indent(body, "    ")
        + "\n}"
    )
    code = ("public class " if language == "csharp" else "class ") + class_name + " {\n"
    if language == "cpp":
        code += "public:\n"
    return signature, code + indent(method, "    ") + (
        "\n};\n" if language == "cpp" else "\n}\n"
    )


def starter_body(spec, language):
    result = spec["result"]
    if result == "void":
        return "pass" if language == "python" else "// Write your solution here."
    value = (
        "False"
        if result == "b" and language == "python"
        else "false"
        if result == "b"
        else '""'
        if result == "s"
        else "0"
    )
    return "return " + value + ("" if language == "python" else ";")
