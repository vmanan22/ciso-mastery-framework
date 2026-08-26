"""
Zero-Dependency Standard-Library JWT Validator (HMAC-SHA256)
Enforces strict RFC 7519 JWT verification with zero external dependencies:
- Mandatory Subject ('sub') non-empty string claim
- Mandatory Expiration ('exp') numeric future timestamp
- Issuer ('iss') claim validation
- Audience ('aud') claim validation
- Not-Before ('nbf') validation
- Constant-time HMAC-SHA256 signature verification
"""

import hmac
import hashlib
import base64
import json
import time
from typing import Dict, Any, Tuple, Optional, Union, List


def base64url_decode(input_str: str) -> bytes:
    """Decodes standard or URL-safe base64 string with padding."""
    rem = len(input_str) % 4
    if rem > 0:
        input_str += "=" * (4 - rem)
    return base64.urlsafe_b64decode(input_str.encode("utf-8"))


def base64url_encode(input_bytes: bytes) -> str:
    """Encodes bytes to URL-safe base64 string without trailing padding."""
    return base64.urlsafe_b64encode(input_bytes).decode("utf-8").rstrip("=")


def create_token(
    payload: Dict[str, Any],
    secret: str,
    issuer: Optional[str] = None,
    audience: Optional[str] = None,
    expires_in_seconds: Optional[int] = None
) -> str:
    """
    Helper to generate a valid signed HMAC-SHA256 JWT with standard claims.
    """
    if not secret:
        raise ValueError("JWT secret must be a non-empty string")

    token_payload = dict(payload)
    now = int(time.time())

    if "iat" not in token_payload:
        token_payload["iat"] = now

    if expires_in_seconds is not None and "exp" not in token_payload:
        token_payload["exp"] = now + expires_in_seconds

    if issuer and "iss" not in token_payload:
        token_payload["iss"] = issuer

    if audience and "aud" not in token_payload:
        token_payload["aud"] = audience

    header = {"alg": "HS256", "typ": "JWT"}
    header_b64 = base64url_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    payload_b64 = base64url_encode(json.dumps(token_payload, separators=(",", ":")).encode("utf-8"))
    
    signing_input = f"{header_b64}.{payload_b64}".encode("utf-8")
    signature = hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha256).digest()
    sig_b64 = base64url_encode(signature)
    
    return f"{header_b64}.{payload_b64}.{sig_b64}"


def verify_token(
    token: str,
    secret: str,
    expected_issuer: Optional[str] = None,
    expected_audience: Optional[str] = None,
    require_standard_claims: bool = True
) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
    """
    Validates signature, header, expiration, and standard RFC 7519 claims of an HMAC-SHA256 JWT.
    
    Args:
        token: Raw Bearer JWT string.
        secret: HMAC-SHA256 shared secret key.
        expected_issuer: Expected 'iss' claim value (optional).
        expected_audience: Expected 'aud' claim value (optional).
        require_standard_claims: When True, requires non-empty 'sub' and future 'exp'.
        
    Returns:
        (is_valid: bool, claims: Optional[dict], error_msg: Optional[str])
    """
    if not secret:
        return False, None, "JWT secret is not configured or empty"

    if not token or not isinstance(token, str):
        return False, None, "Missing or invalid token string"

    parts = token.split(".")
    if len(parts) != 3:
        return False, None, "Malformed JWT: Must contain exactly 3 segments"

    header_b64, payload_b64, sig_b64 = parts

    try:
        header_data = json.loads(base64url_decode(header_b64).decode("utf-8"))
        if not isinstance(header_data, dict):
            return False, None, "Invalid JWT header format"
        if header_data.get("alg") != "HS256":
            return False, None, f"Unsupported algorithm: {header_data.get('alg')}"

        payload_data = json.loads(base64url_decode(payload_b64).decode("utf-8"))
        if not isinstance(payload_data, dict):
            return False, None, "Invalid JWT payload format"
    except Exception as e:
        return False, None, f"Invalid token encoding: {str(e)}"

    # Signature verification (constant-time compare)
    signing_input = f"{header_b64}.{payload_b64}".encode("utf-8")
    expected_sig = hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha256).digest()
    
    try:
        actual_sig = base64url_decode(sig_b64)
    except Exception:
        return False, None, "Invalid signature encoding"

    if not hmac.compare_digest(expected_sig, actual_sig):
        return False, None, "Invalid token signature"

    now = time.time()

    # Required claims validation
    if require_standard_claims:
        # Subject ('sub') claim check
        sub = payload_data.get("sub")
        if not sub or not isinstance(sub, str) or not sub.strip():
            return False, None, "Missing or invalid 'sub' (subject) claim"

        # Expiration ('exp') claim check
        if "exp" not in payload_data:
            return False, None, "Missing mandatory 'exp' (expiration) claim"

    # Expiration ('exp') time validation
    if "exp" in payload_data:
        exp = payload_data["exp"]
        if not isinstance(exp, (int, float)):
            return False, None, "Invalid 'exp' claim type: Must be numeric timestamp"
        if exp < now:
            return False, None, "Authentication token has expired"

    # Not-Before ('nbf') time validation
    if "nbf" in payload_data:
        nbf = payload_data["nbf"]
        if not isinstance(nbf, (int, float)):
            return False, None, "Invalid 'nbf' claim type: Must be numeric timestamp"
        if nbf > now:
            return False, None, "Token is not yet valid ('nbf' timestamp is in future)"

    # Issuer ('iss') validation
    if expected_issuer is not None:
        iss = payload_data.get("iss")
        if not iss or iss != expected_issuer:
            return False, None, f"Invalid 'iss' (issuer) claim: expected '{expected_issuer}', got '{iss}'"

    # Audience ('aud') validation
    if expected_audience is not None:
        aud = payload_data.get("aud")
        if isinstance(aud, list):
            if expected_audience not in aud:
                return False, None, f"Invalid 'aud' (audience) claim: '{expected_audience}' not in audience list"
        elif isinstance(aud, str):
            if aud != expected_audience:
                return False, None, f"Invalid 'aud' (audience) claim: expected '{expected_audience}', got '{aud}'"
        else:
            return False, None, f"Missing or invalid 'aud' (audience) claim"

    return True, payload_data, None
