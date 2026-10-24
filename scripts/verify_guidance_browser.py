"""Launch the built app with isolated practice storage and verify guidance in Chromium."""
import subprocess
import tempfile
from pathlib import Path
from verify_blind75_http import Server, ROOT

if __name__ == '__main__':
    directory = Path(tempfile.mkdtemp(prefix='epi-guidance-'))
    server = Server(ROOT / 'EpiJudge.Web/bin/Release/net10.0/EpiJudge.Web.dll', directory)
    try:
        subprocess.run(['node', str(ROOT / 'scripts/verify_guidance_browser.cjs'), server.base], check=True, timeout=600)
    finally:
        server.close()
