"""Real local formatter regression tests; no student algorithms are executed."""

import ast
import json
import os
import shutil
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from formatter import InvalidCode, format_draft, syntax


class DraftFormatterTests(unittest.TestCase):
    def test_real_formatters_are_idempotent_and_keep_comments_and_literals(self):
        cases = {
            "javascript": 'function f(x){/* keep */return "a  b"+x}',
            "python": 'def f( x ):\n # keep\n return "a  b"+x',
            "cpp": '#include "z.h"\n#include "a.h"\nint f(){/* keep */return 2;}',
            "java": "public static int f(){/* keep */return 2;}",
        }
        for language, source in cases.items():
            with self.subTest(language=language):
                result = format_draft(source, language, "callable-v1")
                self.assertNotEqual(source, result)
                self.assertEqual(result, format_draft(result, language, "callable-v1"))
                self.assertIn("keep", result)
                if language == "cpp":
                    self.assertLess(result.index('"z.h"'), result.index('"a.h"'))
                if language == "python":
                    self.assertEqual(
                        ast.dump(ast.parse(source)), ast.dump(ast.parse(result))
                    )
                if language == "java":
                    self.assertEqual(
                        syntax(source, language, "callable-v1"),
                        syntax(result, language, "callable-v1"),
                    )

    def test_invalid_and_incomplete_code_is_rejected_before_formatting(self):
        for language, source in {
            "javascript": "function f( {",
            "python": "def f(:",
            "cpp": "int f( {",
            "java": "static int f( {",
        }.items():
            with (
                self.subTest(language=language),
                patch("formatter.format_code") as tool,
            ):
                with self.assertRaises(InvalidCode):
                    format_draft(source, language, "callable-v1")
                tool.assert_not_called()

    def test_java_full_program_and_python_multiline_literal(self):
        source = "import java.util.*;\nclass X{static int f(){return 2;}}"
        self.assertIn("class X", format_draft(source, "java", "legacy-v1"))
        source = 'x="""a\n  b\n"""\n'
        self.assertEqual(
            ast.dump(ast.parse(source)),
            ast.dump(ast.parse(format_draft(source, "python", "callable-v1"))),
        )

    def test_formatter_failure_propagates_without_returning_a_replacement(self):
        with (
            patch("formatter.format_code", side_effect=RuntimeError("missing tool")),
            self.assertRaises(RuntimeError),
        ):
            format_draft("x=1", "python", "callable-v1")

    def test_unexpected_token_changes_are_refused(self):
        with (
            patch("formatter.format_code", return_value="x = 2\n"),
            self.assertRaises(InvalidCode),
        ):
            format_draft("x=1", "python", "callable-v1")

    def test_cli_unicode_survives_ascii_only_console(self):
        source = 'name="你好 🌟"'
        result = subprocess.run(
            [sys.executable, str(Path(__file__).with_name("formatter.py"))],
            input=json.dumps(
                {"language": "python", "code": source, "codeFormat": "callable-v1"}
            ),
            text=True,
            encoding="ascii",
            capture_output=True,
            check=True,
            env={**os.environ, "PYTHONIOENCODING": "ascii"},
        )
        code = json.loads(result.stdout)["code"]
        self.assertEqual(ast.dump(ast.parse(source)), ast.dump(ast.parse(code)))

    def test_javascript_uses_configured_local_node(self):
        with patch.dict(os.environ, {"EPI_NODE_PATH": shutil.which("node")}):
            self.assertIn(
                "return 1;",
                format_draft("function f(){return 1}", "javascript", "callable-v1"),
            )
