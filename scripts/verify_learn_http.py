"""Run Learn acceptance against a genuinely isolated local profile."""

import argparse
import hashlib
import json
import subprocess
import tempfile
import traceback
from pathlib import Path

from verify_blind75_http import Server, request
from verify_learn_inventory import audit

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dll", type=Path, required=True)
    parser.add_argument("--browser", action="store_true")
    parser.add_argument("--layout", action="store_true")
    args = parser.parse_args()
    result = audit()
    result["passed"] = False
    paths = [
        path for path in (ROOT / "epijudge.client/src").rglob("*") if path.is_file()
    ]
    paths += [
        Path(__file__),
        ROOT / "scripts/verify_learn_browser.cjs",
        ROOT / "scripts/verify_learn_layout.cjs",
        args.dll.resolve(),
        ROOT / "epijudge.client/dist/index.html",
    ]
    fingerprint = lambda: {
        str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in paths
    }
    result["inputHashes"] = fingerprint()
    folder = ROOT / ".epi-runs"
    folder.mkdir(parents=True, exist_ok=True)
    directory = Path(tempfile.mkdtemp(prefix="learn-http-", dir=folder))
    server = None
    try:
        server = Server(args.dll.resolve(), directory)
        for route in [
            "/learn",
            "/learn?topic=trees-graphs",
            "/learn/reading-shared-state",
            "/reading/reading-parent-pointer-lca",
            "/practice?problem=lowest_common_ancestor",
        ]:
            status, body, _ = request(server.base, route)
            assert status == 200 and b"<html" in body.lower(), route
        status, problems, _ = request(server.base, "/api/problems")
        assert status == 200 and len(problems) == 334
        if args.browser:
            subprocess.run(
                ["node", str(ROOT / "scripts/verify_learn_browser.cjs"), server.base],
                cwd=ROOT,
                check=True,
            )
        if args.layout:
            subprocess.run(
                ["node", str(ROOT / "scripts/verify_learn_layout.cjs"), server.base],
                cwd=ROOT,
                check=True,
            )
        result.update(
            passed=True,
            deepLinks=5,
            isolatedProfile=str(directory),
            browserRequested=args.browser,
            layoutRequested=args.layout,
        )
        assert result["inputHashes"] == fingerprint(), (
            "Inputs changed during acceptance"
        )
    except Exception:
        result["passed"] = False
        result["error"] = traceback.format_exc()
        raise
    finally:
        (folder / "learn-http.json").write_text(
            json.dumps(result, indent=2) + "\n", encoding="utf-8"
        )
        if server:
            server.close()


if __name__ == "__main__":
    main()
