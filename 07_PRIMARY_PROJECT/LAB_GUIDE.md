# Lab Guide — Flagship Secure Software Factory (v0.1)

> Comprehensive learner guide following the 5-stage progression: **Understand ➔ Design ➔ Build ➔ Validate ➔ Lead**.

---

## 🧭 The 5-Stage Progression

```
[Stage 1: UNDERSTAND] ──► [Stage 2: DESIGN] ──► [Stage 3: BUILD] ──► [Stage 4: VALIDATE] ──► [Stage 5: LEAD]
```

---

## 📖 Stage 1: UNDERSTAND (Threats & Requirements)

### The Threat Scenario
An enterprise deploys a customer-facing microservice backed by cloud storage. Without automated security controls, the system faces four critical failure modes:
1. **Unauthenticated API Access (STRIDE: Spoofing)**: Attackers query endpoints directly, bypassing authentication.
2. **Credential Leaks (STRIDE: Information Disclosure)**: Engineers accidentally commit static cloud API keys.
3. **Infrastructure Misconfiguration (STRIDE: Tampering)**: Cloud storage buckets deployed without encryption or with public access.
4. **Supply Chain Compromise (STRIDE: Elevation of Privilege)**: Vulnerable third-party base images allowing remote code execution.

*Reference: [THREAT_MODEL.md](THREAT_MODEL.md)*

---

## 📐 Stage 2: DESIGN (Architecture & Contracts)

### Spec-First API Contract (OpenAPI 3.1)
Rather than writing code first, we author the formal contract in [`docs/openapi.yaml`](docs/openapi.yaml), defining:
* `BearerAuth` (RFC 7519 JWT) enforced on all data routes.
* Public access strictly restricted to `/healthz`.

### Architectural Decisions (ADRs)
* **ADR-01**: Keyless Workload Identity Federation (WIF) over static JSON keys.
* **ADR-02**: Multi-stage Google Distroless containers (non-root UID 65532).
* **ADR-03**: Policy-as-Code (OPA Rego) evaluating Terraform plan JSON.

*Reference: [ARCHITECTURE.md](ARCHITECTURE.md)*

---

## 🔨 Stage 3: BUILD (Implementation)

### 1. Hardened Microservice Application
* Code location: [`containers/app/main.py`](containers/app/main.py)
* Zero-dependency JWT validator: [`containers/app/jwt_validator.py`](containers/app/jwt_validator.py)
* Enforces OWASP security headers: CSP, HSTS, X-Frame-Options, X-Content-Type-Options.

### 2. Infrastructure as Code (Terraform)
* Location: [`iac/environments/gcp-dev/`](iac/environments/gcp-dev/)
* Provisions Cloud KMS CMEK key ring with automated 90-day rotation and uniform GCS bucket.

### 3. Policy-as-Code (OPA Rego)
* Location: [`policies/iac_policies/`](policies/iac_policies/)
* Enforces non-bypassable guardrails: `gcp_storage_security.rego` and `gcp_iam_security.rego`.

---

## 🧪 Stage 4: VALIDATE (Automated Testing & Gates)

### 1. Fail-Closed Pipeline Verification
```bash
python3 scripts/verify_fail_closed.py
```
*Expected Output*: `✅ All workflow files passed fail-closed verification (0 failure-masking patterns detected).`

### 2. Cryptographic Unit Tests
```bash
PYTHONPATH=07_PRIMARY_PROJECT python3 -m unittest 07_PRIMARY_PROJECT/tests/test_jwt_validator.py
```
*Validates*: Token signing, signature verification, expiration checks, and tampering rejection.

### 3. API Authentication Integration Tests
```bash
PYTHONPATH=07_PRIMARY_PROJECT python3 -m unittest 07_PRIMARY_PROJECT/tests/test_api_auth.py
```
*Validates*: Missing token returns `401 Unauthorized`, valid token returns `200 OK`.

---

## 👔 Stage 5: LEAD (Executive Risk Translation)

As a Technical CISO, technical test outputs must be translated into business risk decisions for the Board of Directors.

Review the [Executive Decision Memo](EXECUTIVE_DECISION_MEMO.md) to see how technical evidence is converted into:
* **Residual Risk Scores** (Low / Acceptable)
* **Return on Security Investment (ROSI)** ($0.06/month cloud runtime vs. $4.45M average breach cost)
* **Audit & Regulatory Readiness** (NIST SSDF & SOC 2 compliance).
