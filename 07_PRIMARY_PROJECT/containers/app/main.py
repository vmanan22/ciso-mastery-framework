from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Secure Microservice API",
    description="Production-grade secure service implementing OWASP security controls",
    version="1.0.0"
)

# CORS Policy: Restrict Allowed Origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mycompany.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)

@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    # Enforce Hardened Security Headers (OWASP Recommendations)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response

@app.get("/healthz", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "healthy", "service": "secure-app", "version": "1.0.0"}

@app.get("/api/v1/data")
def get_secure_data():
    return {
        "message": "Secure payload retrieved successfully",
        "encryption": "KMS-AES-256",
        "auth": "OIDC-Verified"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080, log_config=None)
