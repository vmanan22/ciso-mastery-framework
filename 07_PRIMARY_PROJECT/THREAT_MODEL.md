# Threat Model — AI-Powered Secure SDLC Platform

> STRIDE-based threat model. Aligned with NIST SP 800-218 and OWASP SAMM.

---

## Scope & Architecture

**System**: AI-Powered Secure SDLC Platform  
**Version**: 2.0.0  
**Last Updated**: 2026-08-21  

---

## Assets & Classification

| ID | Asset | Sensitivity | Description |
|----|-------|------------|-------------|
| A1 | Source code | 🔴 Critical | Application source code analyzed by the platform |
| A2 | Vulnerability findings | 🔴 Critical | Security vulnerabilities, SAST/SCA/DAST reports |
| A3 | User credentials & secrets | 🔴 Critical | Authentication tokens, API keys, OIDC tokens |
| A4 | Policy-as-Code & rules | 🟡 High | OPA / Rego security policies & compliance definitions |
| A5 | Audit logs | 🟡 High | Complete immutable security log trail |
| A6 | Infrastructure state | 🟡 High | Terraform state files, secret pointers |
| A7 | SBOM artifacts | 🟡 High | Software Bill of Materials for all built containers |
| A8 | GCS bucket (scan results) | 🔴 Critical | Cloud Storage bucket containing SAST/SCA/SBOM artifacts |
| A9 | GCP KMS key | 🔴 Critical | Customer-managed encryption key — loss = permanent data loss |
| A10 | CI/CD pipeline definition | 🔴 Critical | GitHub Actions workflow YAML — tampering enables full supply chain attack |

---

## STRIDE Threat Matrix

### S — Spoofing (Identity)

| # | Threat | Target | Likelihood | Impact | Mitigation | Status |
|---|--------|--------|------------|--------|------------|--------|
| S1 | Attacker impersonates a developer to access findings | AuthN | Medium | High | Require MFA & WebAuthn for portal; OIDC for CI/CD | 🔨 In progress |
| S2 | Compromised CI/CD token used to submit malicious code | Pipeline API | High | Critical | Ephemeral short-lived OIDC tokens; short token TTLs | ✅ Implemented |
| S3 🆕 | Attacker spoofs GitHub OIDC claims to gain GCP access | Workload Identity | Low | Critical | Attribute conditions on WIF pool (repo + branch restrictions) | 🔨 In progress |

### T — Tampering (Data Integrity)

| # | Threat | Target | Likelihood | Impact | Mitigation | Status |
|---|--------|--------|------------|--------|------------|--------|
| T1 | Attacker modifies vulnerability findings to hide issues | DB / Logs | Low | Critical | Immutable append-only audit trail & SHA256 checksums | ✅ Implemented |
| T2 | Tampering with Policy-as-Code rules to bypass security checks | PaC Engine | Medium | High | Signed OPA policies with Cosign; strict PR approvals | 🔨 In progress |
| T3 🆕 | **Supply Chain — Dependency Confusion**: Malicious PyPI package replaces internal package during `pip install` | CI Build | Medium | Critical | Pin all deps with hashes in requirements.txt; Dependabot alerts | 🔨 In progress |
| T4 🆕 | **Poisoned Pipeline Execution**: Attacker injects malicious step into devsecops.yml via PR | GitHub Actions | Medium | Critical | Branch protection on `main`; PR approval required before CI runs on fork PRs | 🔨 In progress |
| T5 🆕 | Attacker modifies GCS bucket content directly (bypassing CI) | GCS Bucket (A8) | Low | High | Versioning enabled; Cloud Audit Logs alert on manual writes outside pipeline | 🔨 In progress |

### R — Repudiation (Accountability)

| # | Threat | Target | Likelihood | Impact | Mitigation | Status |
|---|--------|--------|------------|--------|------------|--------|
| R1 | User denies suppressing or overriding a critical security alert | Audit Service | Medium | High | Mandatory sign-off with cryptographically signed override logs | ✅ Implemented |
| R2 | Unaudited manual infrastructure changes outside CI/CD | Cloud IaC | High | High | Disable manual cloud edits; Cloud Audit Logs alert on drift | 🔨 In progress |
| R3 🆕 | Developer denies pushing code that introduced a vulnerability | CI Pipeline | Medium | Medium | Cosign-signed images tie every build to a specific GitHub Actions run ID | 🔨 In progress |

### I — Information Disclosure (Confidentiality)

| # | Threat | Target | Likelihood | Impact | Mitigation | Status |
|---|--------|--------|------------|--------|------------|--------|
| I1 | Source code or secrets leaked via S3 bucket exposure | S3 Storage | High | Critical | Public Access Block via OPA; KMS AES-256 encryption | ✅ Implemented |
| I2 | Vulnerability report exposed via unauthenticated endpoint | API Gateway | Medium | High | OAuth2 / JWT authorization on all report endpoints | 🔨 In progress |
| I3 🆕 | GCS bucket publicly accessible — SBOM + scan results exposed | GCS Bucket (A8) | Medium | Critical | `public_access_prevention = enforced` + OPA Rego gate blocks deploy if missing | 🔨 In progress |
| I4 🆕 | Static GCP service account key leaked in GitHub repo or CI logs | IAM / Secrets | High | Critical | Workload Identity Federation — zero static keys; OIDC tokens only | 🔨 In progress |
| I5 🆕 | Secrets hardcoded in container image layers (e.g., API keys in Dockerfile) | Container (A7) | Medium | Critical | Gitleaks scans all commits; Semgrep scans source; Trivy scans image layers | 🔨 In progress |

### D — Denial of Service (Availability)

| # | Threat | Target | Likelihood | Impact | Mitigation | Status |
|---|--------|--------|------------|--------|------------|--------|
| D1 | Resource exhaustion via massive repo submissions | Scan Engine | Medium | Medium | Rate limiting, worker pool quotas, file size limits | 🔨 In progress |
| D2 🆕 | KMS key accidental deletion — permanent loss of all encrypted data | GCP KMS (A9) | Low | Critical | 7-day scheduled deletion window enforced; alert on deletion attempt | 🔨 In progress |
| D3 🆕 | CI/CD pipeline paralysis via runaway job consuming all GitHub Actions minutes | GitHub Actions | Low | Medium | Job-level timeout (15 min); cancel-in-progress concurrency setting | 🔨 In progress |

### E — Elevation of Privilege

| # | Threat | Target | Likelihood | Impact | Mitigation | Status |
|---|--------|--------|------------|--------|------------|--------|
| E1 | Developer escalates to administrator role in pipeline | RBAC | Low | Critical | Strict RBAC roles; separation of duties between Sec & Dev | ✅ Implemented |
| E2 | Container breakout to host node in Kubernetes | K8s Cluster | Medium | Critical | Non-root containers, drop ALL capabilities, Kyverno policies | 🔨 In progress |
 [Developer] ──── (HTTPS/Git) ────> [Pre-Commit Hook] 
                                          │ (Push)
                                          ▼
                                   [GitHub Actions CI/CD]
                                      │        │
                     ┌────────────────┘        └────────────────┐
                     ▼                                          ▼
           [SAST / SCA Engine]                         [IaC Scan (OPA / Checkov)]
                     │                                          │
                     ▼                                          ▼
         [Container Build (Trivy)]                     [Terraform Plan / Apply]
                     │                                          │
                     └────────────────┬─────────────────────────┘
                                      ▼
                           [Kubernetes Sandbox Cluster]
                                      │
                                      ▼
                           [DAST Engine (ZAP/Nuclei)]
```

### Trust Boundaries
1. **Boundary 1 (Workstation ➔ VCS)**: TLS 1.3 encryption, SSH key authentication.
2. **Boundary 2 (CI/CD Pipeline ➔ Cloud Provider)**: OIDC token exchange without static access keys.
3. **Boundary 3 (Kubernetes Ingress ➔ Cluster Service)**: Mutual TLS (mTLS) and Kyverno network policies.
