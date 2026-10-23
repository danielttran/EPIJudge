"""Run theme and local formatter browser audits in an isolated practice profile."""

import argparse
import subprocess
from pathlib import Path

from verify_blind75_http import Server, create_run_directory

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dll", type=Path, required=True)
    args = parser.parse_args()
    directory = create_run_directory(ROOT)
    server = Server(args.dll.resolve(), directory)
    try:
        for script in (
            "verify_theme_browser.cjs",
            "verify_format_browser.cjs",
            "verify_solution_language_browser.cjs",
        ):
            subprocess.run(
                ["node", str(ROOT / "scripts" / script), server.base],
                cwd=ROOT,
                check=True,
                timeout=360,
            )
    finally:
        server.close()


if __name__ == "__main__":
    main()
