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
| **SC-01** | Short-lived OIDC tokens for CI/CD Cloud Access (No Long-Lived Keys) | [`.github/workflows/devsecops.yml`](../.github/workflows/devsecops.yml) | Google WIF Keyless Workflow Gate | Gated in CI (Pending live cloud credentials) | **implemented** | — |
| **SC-02** | Bearer JWT Authentication with RFC 7519 Standard Claims (sub, exp, iss, aud) | [`containers/app/main.py`](containers/app/main.py) | [`tests/test_jwt_validator.py`](tests/test_jwt_validator.py), [`tests/test_api_auth.py`](tests/test_api_auth.py) | [PR #15 CI Run #32972289149](https://github.com/vmanan22/ciso-mastery-framework/actions/runs/32972289149) (24/24 Tests Passed) | **verified** | 2026-08-26 |
| **SC-03** | Cloud KMS CMEK (AES-256) Encryption at Rest with 90-Day Rotation | [`iac/environments/gcp-dev/main.tf`](iac/environments/gcp-dev/main.tf) | Checkov CKV_GCP_82 & OPA Rego Gate | IaC Policy Verified; Operational CMEK pending live cloud deploy | **implemented** | — |
| **SC-04** | Hardened Security Headers (CSP, HSTS, X-Frame-Options, X-Content-Type) | [`containers/app/main.py`](containers/app/main.py) | [`tests/test_api_auth.py`](tests/test_api_auth.py) | [PR #15 CI Run #32972289149](https://github.com/vmanan22/ciso-mastery-framework/actions/runs/32972289149) (Stage 2 Integration Tests) | **verified** | 2026-08-26 |
| **SC-05** | Pre-Commit & CI Secret Scanning with Full History Audit | [`.gitleaks.toml`](.gitleaks.toml) | Gitleaks Stage 1 CI Job | [PR #15 CI Run #32972289149](https://github.com/vmanan22/ciso-mastery-framework/actions/runs/32972289149) (0 Leaks Detected) | **verified** | 2026-08-26 |
| **SC-06** | Static Application Security Testing (SAST) with Quality Gate | [`.semgrep.yml`](.semgrep.yml) + Bandit | SAST Stage 2 native scanner exit status + gate regression tests | Correction pending CI proof; [prior head Semgrep failure](https://github.com/vmanan22/ciso-mastery-framework/runs/98195127253) contradicts Stage 2 success | **in progress** | — |
| **SC-07** | Infrastructure-as-Code Policy-as-Code Enforcement (OPA / Rego) | [`policies/iac_policies/`](policies/iac_policies/) | Conftest evaluation against Terraform Plan | [PR #15 CI Run #32972289149](https://github.com/vmanan22/ciso-mastery-framework/actions/runs/32972289149) (Stage 3 Conftest Gate) | **verified** | 2026-08-26 |
| **SC-08** | Container Hardening: Minimal Non-Root Runtime (UID 65532) | [`containers/Dockerfile.hardened`](containers/Dockerfile.hardened) | Docker buildx + Trivy scan | [PR #15 CI Run #32972289149](https://github.com/vmanan22/ciso-mastery-framework/actions/runs/32972289149) (0 High/Crit CVEs) | **verified** | 2026-08-26 |
| **SC-09** | Cryptographic Container Image Signing & Attestation (Cosign) | [`.github/workflows/devsecops.yml`](../.github/workflows/devsecops.yml) | Sigstore Rekor transparency log | Configured in CI workflow (Runs on main push) | **in progress** | — |
| **SC-10** | Dynamic Application Security Testing (DAST) on Active Endpoints | Scheduled for v0.3 milestone | OWASP ZAP automated scan | Roadmap milestone v0.3 | **planned** | — |
| **SC-11** | Inbound Prompt Injection & Jailbreak Heuristic Guard | Scheduled for v0.2 milestone | Adversarial test suite | Roadmap milestone v0.2 | **planned** | — |
| **SC-12** | Outbound PII & Secret Redaction Engine | Scheduled for v0.2 milestone | Automated DLP test suite | Roadmap milestone v0.2 | **planned** | — |
| **SC-13** | Autonomous Agent MCP Tool Interception & Policy Gate | Scheduled for v0.2 milestone | MCP broker test suite | Roadmap milestone v0.2 | **planned** | — |

---

## 3. Coverage Summary

* **Total Controls**: 13
* **Verified (Automated CI Proof)**: 5 (38%)
* **Implemented / Locally Tested**: 2 (15%)
* **In Progress**: 2 (15%)
* **Planned**: 4 (31%)
* **Reference CI Run**: [PR #15 Run #32972289149](https://github.com/vmanan22/ciso-mastery-framework/actions/runs/32972289149) (Historical reference only; separate Semgrep check failed on head `23a3e47`. SAST reconciliation pending; cloud stages skipped.)
