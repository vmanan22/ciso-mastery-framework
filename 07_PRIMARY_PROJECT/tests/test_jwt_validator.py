"""
Unit Tests — RFC 7519 HMAC-SHA256 JWT Validator
Zero-dependency test suite validating cryptographic signing, claim validation, and expiration.
"""

import time
import unittest
from containers.app.jwt_validator import create_token, verify_token


class TestJwtValidator(unittest.TestCase):
    def setUp(self):
        self.secret = "test-secret-key-12345"

    def test_valid_token_verification(self):
        """Verifies that a validly signed token decodes accurately."""
        payload = {"sub": "user-001", "role": "admin", "exp": time.time() + 600}
        token = create_token(payload, self.secret)
        
        is_valid, claims, err = verify_token(token, self.secret)
        self.assertTrue(is_valid)
        self.assertIsNone(err)
        self.assertEqual(claims["sub"], "user-001")
        self.assertEqual(claims["role"], "admin")

    def test_tampered_signature_rejected(self):
        """Verifies that altering the payload or signature causes rejection."""
        payload = {"sub": "user-001", "role": "admin", "exp": time.time() + 600}
        token = create_token(payload, self.secret)
        
        # Tamper with signature
        tampered_token = token[:-4] + "AAAA"
        is_valid, claims, err = verify_token(tampered_token, self.secret)
        self.assertFalse(is_valid)
        self.assertIn("signature", err.lower())

    def test_wrong_secret_rejected(self):
        """Verifies that token signed with secret A fails verification with secret B."""
        payload = {"sub": "user-001", "exp": time.time() + 600}
        token = create_token(payload, "secret-A")
        
        is_valid, claims, err = verify_token(token, "secret-B")
        self.assertFalse(is_valid)
        self.assertIn("signature", err.lower())

    def test_expired_token_rejected(self):
        """Verifies that expired token fails with expiration message."""
        payload = {"sub": "user-001", "exp": time.time() - 3600}
        token = create_token(payload, self.secret)
        
        is_valid, claims, err = verify_token(token, self.secret)
        self.assertFalse(is_valid)
        self.assertIn("expired", err.lower())

    def test_malformed_token_rejected(self):
        """Verifies that malformed string without 3 segments is rejected."""
        is_valid, claims, err = verify_token("not.a.valid.jwt.token", self.secret)
        self.assertFalse(is_valid)
        self.assertIn("malformed", err.lower())


if __name__ == "__main__":
    unittest.main()
