"""Run the real SAST gate: regressions must change its process exit status."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
RULES = ROOT / '07_PRIMARY_PROJECT/.semgrep.yml'


class TestSemgrepGate(unittest.TestCase):
    def scan(self, source, config=RULES):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'app.py'
            target.write_text(source)
            report = Path(directory) / 'results.sarif'
            result = subprocess.run(
                ['bash', str(ROOT / 'scripts/run_semgrep.sh'), str(target),
                 str(report), str(config)], cwd=ROOT, text=True,
                capture_output=True, timeout=120,
                env={**os.environ, 'SEMGREP_SEND_METRICS': 'off'},
            )
            return result

    def test_unprotected_sync_route_fails(self):
        result = self.scan('@app.get("/private")\ndef route(): pass\n')
        self.assertEqual(result.returncode, 1, result.stderr)

    def test_unprotected_async_route_fails(self):
        result = self.scan('@app.post("/private")\nasync def route(): pass\n')
        self.assertEqual(result.returncode, 1, result.stderr)

    def test_protected_routes_and_nonroutes_pass(self):
        result = self.scan('''from fastapi import Depends
@app.get("/private")
def route(auth: dict = Depends(verify_jwt_token)): pass
@app.post("/private")
async def route_async(auth: dict = Depends(verify_jwt_token)): pass
@app.get("/healthz")
def health(): pass
@asynccontextmanager
async def lifespan(app): yield
@app.middleware("http")
async def middleware(request, call_next): pass
''')
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_missing_rules_fail(self):
        result = self.scan('x = 1\n', ROOT / 'missing-rules.yml')
        self.assertNotEqual(result.returncode, 0)

    def test_parse_error_fails(self):
        result = self.scan('@app.get("/private")\ndef broken(:\n')
        self.assertNotEqual(result.returncode, 0)


if __name__ == '__main__':
    unittest.main()
