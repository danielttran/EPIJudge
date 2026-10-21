"""Pinned parsing/formatting tools for bank-owned callable code generation.

These helpers inspect checked-in source only. User drafts are never parsed,
rewritten, reformatted, or migrated by the generator.
"""

import importlib
import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LANGUAGE_MODULES = {
    "csharp": "tree_sitter_c_sharp",
    "cpp": "tree_sitter_cpp",
    "java": "tree_sitter_java",
    "javascript": "tree_sitter_javascript",
}
EXTENSIONS = {
    "csharp": "cs",
    "cpp": "cpp",
    "java": "java",
    "javascript": "js",
    "python": "py",
}


def parse(code: str, language: str):
    from tree_sitter import Language, Parser

    grammar = importlib.import_module(LANGUAGE_MODULES[language])
    parser = Parser(Language(grammar.language()))
    return parser.parse(code.encode("utf-8"))


def text_of(node, source: str | bytes) -> str:
    data = source.encode("utf-8") if isinstance(source, str) else source
    return data[node.start_byte : node.end_byte].decode("utf-8")


def format_code(code: str, language: str) -> str:
    """Format an owned artifact deterministically; fail instead of omitting it."""
    env = os.environ.copy()
    if language == "python":
        ruff_root = env.get("CODE_WORKSPACE_RUFF", "/workspace/toolchains/ruff-pkg")
        if Path(ruff_root).is_dir():
            env["PYTHONPATH"] = ruff_root + os.pathsep + env.get("PYTHONPATH", "")
        command = [
            shutil.which("python3") or "python",
            "-m",
            "ruff",
            "format",
            "--line-length",
            "100",
            "--stdin-filename",
            "solution.py",
            "-",
        ]
    elif language == "javascript":
        command = [
            shutil.which("node") or "node",
            str(ROOT / "epijudge.client/node_modules/prettier/bin/prettier.cjs"),
            "--parser",
            "babel",
            "--print-width",
            "100",
        ]
    else:
        compiler_format = env.get("CODE_WORKSPACE_CLANG_FORMAT") or shutil.which(
            "clang-format"
        )
        if not compiler_format:
            candidate = Path(
                "/workspace/toolchains/clang-format-pkg/clang_format/data/bin/clang-format"
            )
            if candidate.is_file():
                compiler_format = str(candidate)
        if not compiler_format:
            raise RuntimeError("Install clang-format for callable code generation.")
        style = "Microsoft" if language == "csharp" else "Google"
        command = [
            compiler_format,
            "--assume-filename=solution." + EXTENSIONS[language],
            "-style={BasedOnStyle: " + style + ", ColumnLimit: 100, "
            "AllowShortFunctionsOnASingleLine: None, AllowShortBlocksOnASingleLine: Never, "
            "AllowShortIfStatementsOnASingleLine: Never, AllowShortLoopsOnASingleLine: false}",
        ]
    result = subprocess.run(
        command,
        input=code,
        text=True,
        encoding="utf-8",
        capture_output=True,
        env=env,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(f"{language} formatter failed: {result.stderr}")
    return result.stdout.rstrip() + "\n"
