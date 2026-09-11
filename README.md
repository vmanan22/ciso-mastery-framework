# CLOS — CISO Learning Operating System

<div align="center">

[![DevSecOps Pipeline](https://github.com/vmanan22/ciso-mastery-framework/actions/workflows/devsecops.yml/badge.svg)](https://github.com/vmanan22/ciso-mastery-framework/actions/workflows/devsecops.yml)
[![Security Standard](https://img.shields.io/badge/Security-NIST%20SSDF%20%7C%20OWASP%20SAMM-blue.svg)](https://csrc.nist.gov/publications/detail/sp/800-218/final)
[![Spec-Driven](https://img.shields.io/badge/API%20Spec-OpenAPI%203.1-6BA539.svg)](07_PRIMARY_PROJECT/docs/openapi.yaml)
[![Policy as Code](https://img.shields.io/badge/Policy%20as%20Code-OPA%20%2F%20Rego-magenta.svg)](07_PRIMARY_PROJECT/policies/iac_policies/)
[![Zero-Trust Cloud](https://img.shields.io/badge/Cloud%20Auth-GCP%20OIDC%20WIF-orange.svg)](07_PRIMARY_PROJECT/iac/environments/gcp-dev/)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

**An open, hands-on operating system for developing Technical CISOs, Security Architects, and DevSecOps Leaders.**

[Charter](PROJECT_CHARTER.md) • [Roadmap](ROADMAP.md) • [Capability Model](CAPABILITY_MODEL.md) • [Architecture](07_PRIMARY_PROJECT/ARCHITECTURE.md) • [Control Evidence](07_PRIMARY_PROJECT/CONTROL_EVIDENCE_MATRIX.md)

</div>

---

## 1. What is CLOS?

**CLOS (CISO Learning Operating System)** is an open-source reference architecture and learning framework designed to develop **Technical CISOs**. It bridges the gap between high-level executive security strategy and deep technical engineering by operationalizing security across the entire lifecycle: **from secure code and zero-trust cloud platforms to machine-readable audit evidence (OSCAL) and board-level risk decisions**.

---

## 2. Who is it for?

* **Aspiring & Practicing Technical CISOs**: Security leaders seeking deep, verifiable technical fluency across cloud infrastructure, AI models, and software supply chains.
* **Security Architects & Principal Engineers**: Designers building zero-trust systems, Policy-as-Code guardrails, and automated DevSecOps factories.
* **DevSecOps Practitioners**: Engineers building shift-left pipelines, container hardening, SBOM generation, and keyless cloud authentication.
* **Compliance & Risk Officers**: Professionals translating regulations (NIST SSDF, ISO 27001, SOC 2, EU AI Act) into machine-readable control evidence.

---

## 3. What makes it different?

The core differentiator of CLOS is the **Unbroken Evidence Chain**:

```
Threat ➔ Requirement ➔ Architecture Decision ➔ Control ➔ Implementation ➔ Test ➔ Evidence ➔ Risk Metric ➔ Executive Decision
```

In CLOS:
* **No Unsupported Claims**: A control is never marked "implemented" or "verified" without automated tests and reproducible evidence.
* **Fail-Closed Default**: No `|| true`, no soft-fails, and no fake test substitutes. If a scanner or policy fails, the gate fails closed.
* **Changes Must Teach**: Every technical implementation articulates *Why* (business/risk context), *What* (technical architecture), and *How* (concrete code).

---

## 4. What works today? (Maturity: v0.1-RC)

The local and CI foundations below are implemented and backed by automated evidence. Live GCP deployment remains optional and is not currently included in the verified evidence set.

* **Fail-Closed DevSecOps CI/CD**: Gitleaks secret scanning, Semgrep AST + Bandit SAST, Checkov IaC scanning, OPA Rego policy enforcement, hardened minimal container builds, Trivy CVE scanning, Syft SPDX SBOM generation, and keyless container signing. GCP OIDC deployment stages run only when the repository has the required cloud credentials.
* **Hardened Microservice with Bearer JWT**: RFC 7519 HMAC-SHA256 token verification, OWASP security headers (CSP, HSTS, X-Frame-Options), and unauthenticated health probes.
* **Cloud KMS CMEK & Hardened Storage**: Terraform IaC enforcing AES-256 customer-managed encryption keys with automated 90-day rotation and uniform bucket-level access; live deployment is pending controlled GCP validation.
* **Policy-as-Code Gate**: Open Policy Agent (OPA) Rego rules blocking unencrypted storage, public access, and dangerous IAM roles before deployment.
* **Automated Evidence Matrix**: [CONTROL_EVIDENCE_MATRIX.md](07_PRIMARY_PROJECT/CONTROL_EVIDENCE_MATRIX.md) tracking 13 controls with direct links to automated tests.

---

## 5. What is planned?

* **v0.2 — AI Security Engineering & MCP Broker Lab**: Zero-Trust AI Security Gateway, prompt injection classifiers, outbound PII redaction, and autonomous agent tool sandboxing.
* **v0.3 — Technical CISO Control Plane**: Dynamic risk registers derived from CI/CD telemetry, automated DAST scanning, and executive board decision memo templates.
* **v1.0 — Multi-Track Community Ecosystem**: Expansion across all 8 capability tracks with multi-maintainer open-source governance.

*See [ROADMAP.md](ROADMAP.md) for detailed milestone milestones and release criteria.*

---

## 6. How does a learner start?

### Local Prerequisites
* Python 3.11+
* Git
* A Python virtual environment with Semgrep, Bandit, pytest, httpx, and the application dependencies installed
* Terraform / OpenTofu (optional for cloud labs)

### Run Verified Test Suites Locally
```bash
# 1. Clone the repository
git clone https://github.com/vmanan22/ciso-mastery-framework.git
cd ciso-mastery-framework

# 2. Install the local validation and application dependencies
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install semgrep bandit pytest httpx
python -m pip install -r 07_PRIMARY_PROJECT/containers/app/requirements.txt

# 3. Run automated pipeline integrity verification
python3 scripts/verify_fail_closed.py

# 4. Run all unit and cryptographic test suites
PYTHONPATH=. python3 -m unittest discover -s tests -p "test_*.py"
PYTHONPATH=07_PRIMARY_PROJECT python3 -m unittest discover -s 07_PRIMARY_PROJECT/tests -p "test_*.py"
```

---

## 7. How can someone contribute?

We welcome technical contributions that adhere to the **Evidence Chain**.
1. Review the [Project Charter](PROJECT_CHARTER.md) and [Capability Model](CAPABILITY_MODEL.md).
2. Choose an open issue or propose an enhancement on a separate branch.
3. Ensure all changes include automated tests, zero failure-masking, and updated control evidence mappings.

---

## 📄 License

This project is licensed under the [Apache-2.0 License](LICENSE).
