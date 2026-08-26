"""
Secure Microservice API — Hardened FastAPI Implementation
Enforces:
- Bearer JWT Authentication (OpenAPI 3.1 Contract Compliance)
- OWASP Recommended Security Headers
- Strict CORS Policy
- Unauthenticated Healthz Probe
"""

import os
from contextlib import asynccontextmanager
from typing import Optional, Dict
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

try:
    from .jwt_validator import verify_token
except ImportError:
    from jwt_validator import verify_token


def validate_auth_config() -> Dict[str, str]:
    """
    Validates that all mandatory authentication environment variables are configured.
    Raises RuntimeError on startup if any required parameter is missing or empty.
    """
    secret = os.environ.get("JWT_SECRET")
    issuer = os.environ.get("JWT_ISSUER")
    audience = os.environ.get("JWT_AUDIENCE")

    missing = []
    if not secret or not secret.strip():
        missing.append("JWT_SECRET")
    if not issuer or not issuer.strip():
        missing.append("JWT_ISSUER")
    if not audience or not audience.strip():
        missing.append("JWT_AUDIENCE")

    if missing:
        raise RuntimeError(
            f"CRITICAL: Application startup aborted. Missing mandatory authentication environment variables: {', '.join(missing)}. "
            "Set JWT_SECRET, JWT_ISSUER, and JWT_AUDIENCE in the deployment environment."
        )

    return {"secret": secret, "issuer": issuer, "audience": audience}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan handler executing fail-closed startup validation checks."""
    validate_auth_config()
    yield


app = FastAPI(
    title="Secure Microservice API",
    description="Production-grade secure service implementing OWASP security controls & Bearer JWT authentication",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Policy: Restrict Allowed Origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mycompany.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)

security = HTTPBearer(auto_error=False)


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    # Enforce Hardened Security Headers (OWASP Recommendations)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response


def verify_jwt_token(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> dict:
    """
    Validates the Bearer JWT token against signature, expiration, issuer, and audience.
    Returns decoded token claims on success; raises 401 Unauthorized or fails closed on configuration error.
    """
    try:
        auth_config = validate_auth_config()
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Bearer authentication token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    token = credentials.credentials
    is_valid, claims, error_msg = verify_token(
        token=token,
        secret=auth_config["secret"],
        expected_issuer=auth_config["issuer"],
        expected_audience=auth_config["audience"],
        require_standard_claims=True
    )
    
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_msg or "Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return claims


@app.get("/healthz", status_code=status.HTTP_200_OK)
def health_check():
    """Unauthenticated health & liveness probe."""
    return {"status": "healthy", "service": "secure-app", "version": "1.0.0"}


@app.get("/api/v1/data", status_code=status.HTTP_200_OK)
def get_secure_data(token_claims: dict = Depends(verify_jwt_token)):
    """
    Protected data endpoint requiring authenticated Bearer JWT.
    """
    return {
        "message": "Secure payload retrieved successfully",
        "encryption": "KMS-AES-256",
        "auth": "Bearer-JWT-Verified",
        "subject": token_claims.get("sub", "authenticated-user")
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080, log_config=None)
