# Security Validation Report — [Component Name]

> Standard template for automated testing, scanner outputs, and compliance validation.

---

## 📋 Executive Summary

* **Target System**: [e.g., CLOS Core Microservice & Cloud IaC]
* **Validation Date**: [YYYY-MM-DD]
* **Validation Type**: [Automated CI / Local Pre-Flight / Regression Suite]
* **Overall Outcome**: 🟢 **PASSED** / 🔴 **FAILED** / 🟡 **PASSED WITH NOTED EXCEPTIONS**

---

## 🛡️ Security Gate Results

| Gate # | Security Tool / Test | Scope | Severity Threshold | Result | Findings Count |
| :---: | :--- | :--- | :---: | :---: | :---: |
| **1** | **Gitleaks** | Full Git Commit History | ANY Secret | ✅ PASS | 0 |
| **2** | **Semgrep + Bandit** | Python Source AST | HIGH / CRITICAL | ✅ PASS | 0 |
| **3** | **Checkov** | Terraform IaC | HIGH / CRITICAL | ✅ PASS | 0 |
| **4** | **OPA / Conftest** | Terraform Plan JSON | ANY Deny Rule | ✅ PASS | 0 |
| **5** | **Trivy** | Hardened Container Image | HIGH / CRITICAL | ✅ PASS | 0 |
| **6** | **Syft + Cosign** | Supply Chain SBOM / Attestation | SLSA Level 3 | ✅ PASS | Validated |
| **7** | **FastAPI Auth Tests**| RFC 7519 JWT Enforcement | 100% Pass Rate | ✅ PASS | 0 Failures |

---

## 🔬 Evidence Artifacts

1. **SAST Scan Evidence**: `artifacts/sast/semgrep.sarif`
2. **IaC Policy Evidence**: `artifacts/iac/opa_evaluation.json`
3. **Software Bill of Materials (SBOM)**: `artifacts/supply_chain/sbom.spdx.json`
4. **Cosign Cryptographic Digest**: `sha256:[digest_here]`

---

## ⚠️ Residual Risks & Known Limitations

* [Document any accepted exceptions, skipped non-critical checks, or future improvements.]
