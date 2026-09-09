"""
Unit Tests — RFC 7519 HMAC-SHA256 JWT Validator
Zero-dependency test suite validating cryptographic signing, claim validation (sub, exp, iss, aud, nbf), and failure modes.
"""

import time
import unittest
from containers.app.jwt_validator import create_token, verify_token


class TestJwtValidator(unittest.TestCase):
    def setUp(self):
        self.secret = "test-secret-key-12345"
        self.issuer = "clos-auth-service"
        self.audience = "clos-api"

    def test_valid_token_verification(self):
        """Verifies that a validly signed token with standard claims decodes accurately."""
        payload = {
            "sub": "user-001",
            "role": "admin",
            "exp": time.time() + 600,
            "iss": self.issuer,
            "aud": self.audience,
        }
        token = create_token(payload, self.secret)
        
        is_valid, claims, err = verify_token(
            token, self.secret, expected_issuer=self.issuer, expected_audience=self.audience
        )
        self.assertTrue(is_valid)
        self.assertIsNone(err)
        self.assertEqual(claims["sub"], "user-001")
        self.assertEqual(claims["role"], "admin")
        self.assertEqual(claims["iss"], self.issuer)
        self.assertEqual(claims["aud"], self.audience)

    def test_missing_sub_claim_rejected(self):
        """Verifies that token without 'sub' claim is rejected."""
        payload = {"role": "admin", "exp": time.time() + 600}
        token = create_token(payload, self.secret)
        
        is_valid, claims, err = verify_token(token, self.secret, require_standard_claims=True)
        self.assertFalse(is_valid)
        self.assertIn("sub", err.lower())

    def test_empty_sub_claim_rejected(self):
        """Verifies that token with empty whitespace 'sub' is rejected."""
        payload = {"sub": "   ", "exp": time.time() + 600}
        token = create_token(payload, self.secret)
        
        is_valid, claims, err = verify_token(token, self.secret, require_standard_claims=True)
        self.assertFalse(is_valid)
        self.assertIn("sub", err.lower())

    def test_missing_exp_claim_rejected(self):
        """Verifies that token without 'exp' claim is rejected when standard claims required."""
        payload = {"sub": "user-001"}
        token = create_token(payload, self.secret)
        
        is_valid, claims, err = verify_token(token, self.secret, require_standard_claims=True)
        self.assertFalse(is_valid)
        self.assertIn("exp", err.lower())

    def test_expired_token_rejected(self):
        """Verifies that expired token fails with expiration message."""
        payload = {"sub": "user-001", "exp": time.time() - 3600}
        token = create_token(payload, self.secret)
        
        is_valid, claims, err = verify_token(token, self.secret)
        self.assertFalse(is_valid)
        self.assertIn("expired", err.lower())

    def test_future_nbf_token_rejected(self):
        """Verifies that token with future 'nbf' (not before) claim is rejected."""
        payload = {
            "sub": "user-001",
            "exp": time.time() + 3600,
            "nbf": time.time() + 1800,  # 30 minutes in future
        }
        token = create_token(payload, self.secret)
        
        is_valid, claims, err = verify_token(token, self.secret)
        self.assertFalse(is_valid)
        self.assertIn("nbf", err.lower())

    def test_invalid_issuer_rejected(self):
        """Verifies that token with mismatched issuer claim is rejected."""
        payload = {
            "sub": "user-001",
            "exp": time.time() + 600,
            "iss": "rogue-auth-service",
        }
        token = create_token(payload, self.secret)
        
        is_valid, claims, err = verify_token(token, self.secret, expected_issuer=self.issuer)
        self.assertFalse(is_valid)
        self.assertIn("iss", err.lower())

    def test_invalid_audience_rejected(self):
        """Verifies that token with mismatched audience claim is rejected."""
        payload = {
            "sub": "user-001",
            "exp": time.time() + 600,
            "aud": "wrong-api-service",
        }
        token = create_token(payload, self.secret)
        
        is_valid, claims, err = verify_token(token, self.secret, expected_audience=self.audience)
        self.assertFalse(is_valid)
        self.assertIn("aud", err.lower())

    def test_tampered_signature_rejected(self):
        """Verifies that altering the payload or signature causes rejection."""
        payload = {"sub": "user-001", "role": "admin", "exp": time.time() + 600}
        token = create_token(payload, self.secret)
        
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

    def test_empty_secret_rejected(self):
        """Verifies that passing an empty secret returns configuration error."""
        payload = {"sub": "user-001", "exp": time.time() + 600}
        token = create_token(payload, self.secret)
        
        is_valid, claims, err = verify_token(token, "")
        self.assertFalse(is_valid)
        self.assertIn("secret", err.lower())

    def test_malformed_token_rejected(self):
        """Verifies that malformed string without 3 segments is rejected."""
        is_valid, claims, err = verify_token("not.a.valid.jwt.token", self.secret)
        self.assertFalse(is_valid)
        self.assertIn("malformed", err.lower())


if __name__ == "__main__":
    unittest.main()
