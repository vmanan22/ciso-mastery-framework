"""
Zero-Dependency Standard-Library JWT Validator (HMAC-SHA256)
Enforces RFC 7519 JWT verification with zero external dependencies.
"""

import hmac
import hashlib
import base64
import json
import time
from typing import Dict, Any, Tuple, Optional


def base64url_decode(input_str: str) -> bytes:
    """Decodes standard or URL-safe base64 string with padding."""
    rem = len(input_str) % 4
    if rem > 0:
        input_str += "=" * (4 - rem)
    return base64.urlsafe_b64decode(input_str.encode("utf-8"))


def base64url_encode(input_bytes: bytes) -> str:
    """Encodes bytes to URL-safe base64 string without trailing padding."""
    return base64.urlsafe_b64encode(input_bytes).decode("utf-8").rstrip("=")


def create_token(payload: Dict[str, Any], secret: str) -> str:
    """Helper to generate a valid signed HMAC-SHA256 JWT."""
    header = {"alg": "HS256", "typ": "JWT"}
    header_b64 = base64url_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    payload_b64 = base64url_encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    
    signing_input = f"{header_b64}.{payload_b64}".encode("utf-8")
    signature = hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha256).digest()
    sig_b64 = base64url_encode(signature)
    
    return f"{header_b64}.{payload_b64}.{sig_b64}"


def verify_token(token: str, secret: str) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
    """
    Validates signature, header, and expiration of an HMAC-SHA256 JWT.
    
    Returns:
        (is_valid: bool, claims: Optional[dict], error_msg: Optional[str])
    """
    parts = token.split(".")
    if len(parts) != 3:
        return False, None, "Malformed JWT: Must contain exactly 3 segments"

    header_b64, payload_b64, sig_b64 = parts

    try:
        header_data = json.loads(base64url_decode(header_b64).decode("utf-8"))
        if header_data.get("alg") != "HS256":
            return False, None, f"Unsupported algorithm: {header_data.get('alg')}"

        payload_data = json.loads(base64url_decode(payload_b64).decode("utf-8"))
    except Exception as e:
        return False, None, f"Invalid token encoding: {str(e)}"

    # Signature verification
    signing_input = f"{header_b64}.{payload_b64}".encode("utf-8")
    expected_sig = hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha256).digest()
    
    try:
        actual_sig = base64url_decode(sig_b64)
    except Exception:
        return False, None, "Invalid signature encoding"

    if not hmac.compare_digest(expected_sig, actual_sig):
        return False, None, "Invalid token signature"

    # Expiration check
    exp = payload_data.get("exp")
    if exp is not None:
        if isinstance(exp, (int, float)) and exp < time.time():
            return False, None, "Authentication token has expired"

    return True, payload_data, None
