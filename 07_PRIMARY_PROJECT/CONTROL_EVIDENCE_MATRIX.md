# Control & Evidence Matrix — CISO Learning Operating System (CLOS)

> Canonical, evidence-backed security control registry. Every control marked `verified` links to an automated test or reproducible audit artifact.

---

## 1. Maturity Status Definitions

| Status | Definition | Evidence Requirement |
| :--- | :--- | :--- |
| **planned** | Control requirement defined in architecture/threat model but not yet built. | Architecture specification or issue ticket. |
| **in progress** | Control implementation is actively in development. | Code branch or draft pull request. |
| **implemented** | Control code is written and integrated into the codebase. | Source file and configuration reference. |
| **verified** | Control is actively proven by automated tests and CI evidence. | Passing automated test suite + CI pipeline artifact. |
| **exception accepted** | Risk accepted or compensated with documented business rationale. | Documented ADR with expiration date and owner role. |

---

## 2. Control & Evidence Registry

| Control ID | Requirement | Implementation | Test | Evidence Path | Status | Last Verified |
| :---: | :--- | :--- | :--- | :--- | :---: | :---: |
| **SC-01** | Short-lived OIDC tokens for CI/CD Cloud Access (No Long-Lived Keys) | [`.github/workflows/devsecops.yml:300-308`](file://.github/workflows/devsecops.yml) | Google WIF OIDC Token Exchange | `.github/workflows/devsecops.yml` | **verified** | 2026-08-23 |
| **SC-02** | Bearer JWT Authentication on Protected Microservice Endpoints | [`containers/app/main.py:46-65`](file://07_PRIMARY_PROJECT/containers/app/main.py) | [`tests/test_jwt_validator.py:1-60`](file://07_PRIMARY_PROJECT/tests/test_jwt_validator.py) | `07_PRIMARY_PROJECT/tests/test_jwt_validator.py` | **verified** | 2026-08-23 |
| **SC-03** | Cloud KMS CMEK (AES-256) Encryption at Rest with 90-Day Rotation | [`iac/environments/gcp-dev/main.tf:37-47`](file://07_PRIMARY_PROJECT/iac/environments/gcp-dev/main.tf) | Checkov CKV_GCP_82 & OPA Rego Gate | `07_PRIMARY_PROJECT/policies/iac_policies/gcp_storage_security.rego` | **verified** | 2026-08-23 |
| **SC-04** | Hardened Security Headers (CSP, HSTS, X-Frame-Options, X-Content-Type) | [`containers/app/main.py:34-43`](file://07_PRIMARY_PROJECT/containers/app/main.py) | Unit test header assertions | `07_PRIMARY_PROJECT/tests/test_api_auth.py` | **verified** | 2026-08-23 |
| **SC-05** | Pre-Commit & CI Secret Scanning with Full History Audit | [`.gitleaks.toml`](file://07_PRIMARY_PROJECT/.gitleaks.toml) | Gitleaks Stage 1 CI Job | `.github/workflows/devsecops.yml` | **verified** | 2026-08-23 |
| **SC-06** | Static Application Security Testing (SAST) with Quality Gate | [`.semgrep.yml`](file://07_PRIMARY_PROJECT/.semgrep.yml) + Bandit | SAST Stage 2 Quality Gate Script | `bandit-results.json`, `semgrep.sarif` | **verified** | 2026-08-23 |
| **SC-07** | Infrastructure-as-Code Policy-as-Code Enforcement (OPA / Rego) | [`policies/iac_policies/`](file://07_PRIMARY_PROJECT/policies/iac_policies/) | Conftest evaluation against Terraform Plan | `07_PRIMARY_PROJECT/policies/iac_policies/` | **verified** | 2026-08-23 |
| **SC-08** | Container Hardening: Minimal Non-Root Runtime (UID 65532) | [`containers/Dockerfile.hardened`](file://07_PRIMARY_PROJECT/containers/Dockerfile.hardened) | Docker buildx + Trivy scan | `07_PRIMARY_PROJECT/containers/Dockerfile.hardened` | **verified** | 2026-08-23 |
| **SC-09** | Cryptographic Container Image Signing & Attestation (Cosign) | [`.github/workflows/devsecops.yml:278-284`](file://.github/workflows/devsecops.yml) | Sigstore Rekor transparency log | `.github/workflows/devsecops.yml` | **in progress** | 2026-08-23 |
| **SC-10** | Dynamic Application Security Testing (DAST) on Active Endpoints | Scheduled for v0.3 milestone | OWASP ZAP automated scan | Roadmap milestone v0.3 | **planned** | — |
| **SC-11** | Inbound Prompt Injection & Jailbreak Heuristic Guard | Scheduled for v0.2 milestone | Adversarial test suite | Roadmap milestone v0.2 | **planned** | — |
| **SC-12** | Outbound PII & Secret Redaction Engine | Scheduled for v0.2 milestone | Automated DLP test suite | Roadmap milestone v0.2 | **planned** | — |
| **SC-13** | Autonomous Agent MCP Tool Interception & Policy Gate | Scheduled for v0.2 milestone | MCP broker test suite | Roadmap milestone v0.2 | **planned** | — |

---

## 3. Coverage Summary

* **Total Controls**: 13
* **Verified (Automated Proof)**: 8 (62%)
* **Implemented**: 0 (0%)
* **In Progress**: 1 (8%)
* **Planned**: 4 (31%)
