"""
Automated Integration & Security Tests — FastAPI Microservice Authentication
Validates Bearer JWT enforcement, negative failure paths, and OWASP security headers.
"""

import time
import unittest

from fastapi.testclient import TestClient
from containers.app.main import app, JWT_SECRET
from containers.app.jwt_validator import create_token


class TestApiAuthentication(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_healthz_unauthenticated(self):
        """Verifies that /healthz is publicly accessible without credentials."""
        resp = self.client.get("/healthz")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["status"], "healthy")

    def test_protected_endpoint_missing_token_returns_401(self):
        """Verifies that accessing /api/v1/data without Authorization header is rejected."""
        resp = self.client.get("/api/v1/data")
        self.assertEqual(resp.status_code, 401)
        self.assertIn("Bearer", resp.headers.get("WWW-Authenticate", ""))

    def test_protected_endpoint_invalid_token_returns_401(self):
        """Verifies that a malformed or forged JWT is rejected."""
        headers = {"Authorization": "Bearer invalid.token.signature"}
        resp = self.client.get("/api/v1/data", headers=headers)
        self.assertEqual(resp.status_code, 401)

    def test_protected_endpoint_expired_token_returns_401(self):
        """Verifies that an expired JWT token is rejected."""
        expired_payload = {
            "sub": "expired-user",
            "exp": time.time() - 3600
        }
        token = create_token(expired_payload, JWT_SECRET)
        headers = {"Authorization": f"Bearer {token}"}
        resp = self.client.get("/api/v1/data", headers=headers)
        self.assertEqual(resp.status_code, 401)
        self.assertIn("expired", resp.json()["detail"].lower())

    def test_protected_endpoint_valid_token_returns_200(self):
        """Verifies that a legitimately signed JWT returns 200 with verified claims."""
        valid_payload = {
            "sub": "audited-engineer-01",
            "role": "security-architect",
            "exp": time.time() + 3600
        }
        token = create_token(valid_payload, JWT_SECRET)
        headers = {"Authorization": f"Bearer {token}"}
        resp = self.client.get("/api/v1/data", headers=headers)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["auth"], "Bearer-JWT-Verified")
        self.assertEqual(data["subject"], "audited-engineer-01")

    def test_owasp_security_headers_present(self):
        """Verifies that hardened security headers are returned on all responses."""
        resp = self.client.get("/healthz")
        self.assertEqual(resp.headers.get("X-Content-Type-Options"), "nosniff")
        self.assertEqual(resp.headers.get("X-Frame-Options"), "DENY")
        self.assertIn("default-src 'self'", resp.headers.get("Content-Security-Policy", ""))
        self.assertIn("max-age=31536000", resp.headers.get("Strict-Transport-Security", ""))


if __name__ == "__main__":
    unittest.main()
