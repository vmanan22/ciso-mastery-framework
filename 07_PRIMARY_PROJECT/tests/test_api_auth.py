"""
Automated Integration & Security Tests — FastAPI Microservice Authentication
Validates Bearer JWT enforcement, standard RFC 7519 claims (sub, exp, iss, aud), negative failure paths, and OWASP security headers.
"""

import os
import time
import unittest

# Set test environment credentials before importing app modules
os.environ["JWT_SECRET"] = "test-e2e-jwt-secret-key-12345"
os.environ["JWT_ISSUER"] = "clos-auth-service"
os.environ["JWT_AUDIENCE"] = "clos-api"

JWT_ISSUER = os.environ["JWT_ISSUER"]
JWT_AUDIENCE = os.environ["JWT_AUDIENCE"]

from fastapi.testclient import TestClient
from containers.app.main import app
from containers.app.jwt_validator import create_token


class TestApiAuthentication(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.secret = os.environ["JWT_SECRET"]
        cls.client = TestClient(app)
        cls.client.__enter__()
        cls.addClassCleanup(cls.client.__exit__, None, None, None)

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
            "exp": time.time() - 3600,
            "iss": JWT_ISSUER,
            "aud": JWT_AUDIENCE,
        }
        token = create_token(expired_payload, self.secret)
        headers = {"Authorization": f"Bearer {token}"}
        resp = self.client.get("/api/v1/data", headers=headers)
        self.assertEqual(resp.status_code, 401)
        self.assertIn("expired", resp.json()["detail"].lower())

    def test_protected_endpoint_missing_sub_returns_401(self):
        """Verifies that a JWT without 'sub' claim is rejected."""
        payload = {
            "role": "security-engineer",
            "exp": time.time() + 3600,
            "iss": JWT_ISSUER,
            "aud": JWT_AUDIENCE,
        }
        token = create_token(payload, self.secret)
        headers = {"Authorization": f"Bearer {token}"}
        resp = self.client.get("/api/v1/data", headers=headers)
        self.assertEqual(resp.status_code, 401)
        self.assertIn("sub", resp.json()["detail"].lower())

    def test_protected_endpoint_mismatched_issuer_returns_401(self):
        """Verifies that a JWT with an unexpected issuer is rejected."""
        payload = {
            "sub": "audited-engineer-01",
            "exp": time.time() + 3600,
            "iss": "untrusted-issuer",
            "aud": JWT_AUDIENCE,
        }
        token = create_token(payload, self.secret)
        headers = {"Authorization": f"Bearer {token}"}
        resp = self.client.get("/api/v1/data", headers=headers)
        self.assertEqual(resp.status_code, 401)
        self.assertIn("iss", resp.json()["detail"].lower())

    def test_protected_endpoint_mismatched_audience_returns_401(self):
        """Verifies that a JWT intended for another audience is rejected."""
        payload = {
            "sub": "audited-engineer-01",
            "exp": time.time() + 3600,
            "iss": JWT_ISSUER,
            "aud": "wrong-service-audience",
        }
        token = create_token(payload, self.secret)
        headers = {"Authorization": f"Bearer {token}"}
        resp = self.client.get("/api/v1/data", headers=headers)
        self.assertEqual(resp.status_code, 401)
        self.assertIn("aud", resp.json()["detail"].lower())

    def test_protected_endpoint_valid_token_returns_200(self):
        """Verifies that a legitimately signed JWT with all required claims returns 200."""
        valid_payload = {
            "sub": "audited-engineer-01",
            "role": "security-architect",
            "exp": time.time() + 3600,
            "iss": JWT_ISSUER,
            "aud": JWT_AUDIENCE,
        }
        token = create_token(valid_payload, self.secret)
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

    def test_startup_fails_when_jwt_secret_missing(self):
        """Verifies that missing JWT_SECRET aborts startup with a critical configuration error."""
        original = os.environ.pop("JWT_SECRET", None)
        try:
            with self.assertRaises(RuntimeError) as ctx:
                with TestClient(app):
                    self.fail("Startup should reject missing authentication configuration")
            self.assertIn("JWT_SECRET", str(ctx.exception))
        finally:
            if original:
                os.environ["JWT_SECRET"] = original

    def test_startup_fails_when_jwt_issuer_missing(self):
        """Verifies that missing JWT_ISSUER aborts startup with a critical configuration error."""
        original = os.environ.pop("JWT_ISSUER", None)
        try:
            with self.assertRaises(RuntimeError) as ctx:
                with TestClient(app):
                    self.fail("Startup should reject missing authentication configuration")
            self.assertIn("JWT_ISSUER", str(ctx.exception))
        finally:
            if original:
                os.environ["JWT_ISSUER"] = original

    def test_startup_fails_when_jwt_audience_missing(self):
        """Verifies that missing JWT_AUDIENCE aborts startup with a critical configuration error."""
        original = os.environ.pop("JWT_AUDIENCE", None)
        try:
            with self.assertRaises(RuntimeError) as ctx:
                with TestClient(app):
                    self.fail("Startup should reject missing authentication configuration")
            self.assertIn("JWT_AUDIENCE", str(ctx.exception))
        finally:
            if original:
                os.environ["JWT_AUDIENCE"] = original


if __name__ == "__main__":
    unittest.main()
