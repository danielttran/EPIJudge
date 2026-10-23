"""Local, opt-in draft formatting. Never executes code or writes draft files."""

import ast
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

from common import EXTENSIONS, format_code, parse, text_of


class InvalidCode(ValueError):
    pass


def syntax(code, language, code_format):
    if language == "python":
        try:
            return ast.parse(code)
        except SyntaxError as error:
            raise InvalidCode(f"Line {error.lineno}: {error.msg}") from error
    source = (
        "class __Format {\n" + code + "\n}"
        if language == "java" and code_format == "callable-v1"
        else code
    )
    root = parse(source, language).root_node
    stack = [root]
    leaves = []
    while stack:
        node = stack.pop()
        if node.type == "ERROR" or node.is_missing:
            line = max(1, node.start_point.row + (0 if source != code else 1))
            raise InvalidCode(f"Incomplete or invalid syntax near line {line}.")
        if node.children:
            stack.extend(reversed(node.children))
        elif node.type != "comment":
            leaves.append((node.type, text_of(node, source)))
    return leaves


def format_draft(code, language, code_format):
    if language not in EXTENSIONS or code_format not in ("callable-v1", "legacy-v1"):
        raise InvalidCode("Choose a supported language and code format.")
    if not isinstance(code, str) or not code.strip() or len(code) > 40000:
        raise InvalidCode("Enter between 1 and 40,000 characters of code.")
    before = syntax(code, language, code_format)
    node = os.environ.get("EPI_NODE_PATH")
    if language == "javascript" and node and os.path.isfile(node):
        from common import ROOT

        result = subprocess.run(
            [
                node,
                str(ROOT / "epijudge.client/node_modules/prettier/bin/prettier.cjs"),
                "--parser",
                "babel",
                "--print-width",
                "100",
            ],
            input=code,
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=True,
        )
        formatted = result.stdout
    elif language in ("python", "javascript"):
        formatted = format_code(code, language)
    else:
        executable = os.environ.get("CODE_WORKSPACE_CLANG_FORMAT") or shutil.which(
            "clang-format"
        )
        if (
            not executable
            and (package := importlib.util.find_spec("clang_format"))
            and package.origin
        ):
            candidate = (
                Path(package.origin).parent
                / "data"
                / "bin"
                / ("clang-format.exe" if os.name == "nt" else "clang-format")
            )
            if candidate.is_file():
                executable = str(candidate)
        if not executable:
            candidate = "/workspace/toolchains/clang-format-pkg/clang_format/data/bin/clang-format"
            if os.path.isfile(candidate):
                executable = candidate
        if not executable:
            raise FileNotFoundError("clang-format is not installed.")
        style = "Microsoft" if language == "csharp" else "Google"
        result = subprocess.run(
            [
                executable,
                "--assume-filename=solution." + EXTENSIONS[language],
                "-style={BasedOnStyle: " + style + ", ColumnLimit: 100, "
                "SortIncludes: Never, SortUsingDeclarations: Never, "
                "BreakStringLiterals: false, ReflowComments: Never, "
                "AllowShortFunctionsOnASingleLine: None, "
                "AllowShortBlocksOnASingleLine: Never, "
                "AllowShortIfStatementsOnASingleLine: Never, "
                "AllowShortLoopsOnASingleLine: false}",
            ],
            input=code,
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=True,
        )
        formatted = result.stdout
    after = syntax(formatted, language, code_format)
    if language == "python":
        if ast.dump(before) != ast.dump(after):
            raise InvalidCode(
                "Formatting changed the syntax tree; code was left unchanged."
            )
    elif language != "javascript" and before != after:
        raise InvalidCode("Formatting changed code tokens; code was left unchanged.")
    if len(formatted) > 40000:
        raise InvalidCode(
            "Formatted code exceeds 40,000 characters. Code was not changed."
        )
    return formatted


def main():
    try:
        request = json.load(sys.stdin)
        code = format_draft(request["code"], request["language"], request["codeFormat"])
        result = {"code": code}
    except (InvalidCode, SyntaxError) as error:
        result = {"error": "invalid", "message": str(error)}
    except (
        ImportError,
        OSError,
        RuntimeError,
        subprocess.SubprocessError,
        ValueError,
        KeyError,
        TypeError,
    ):
        # Dependency/process errors must not include the user's source in diagnostics.
        result = {
            "error": "unavailable",
            "message": "Local formatter unavailable. Install scripts/code_workspace/requirements.txt with the server's Python and run npm ci in epijudge.client. Code was not changed.",
        }
    print(json.dumps(result, ensure_ascii=True))


if __name__ == "__main__":
    main()
