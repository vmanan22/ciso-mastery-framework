# Project Charter — CISO Learning Operating System (CLOS)

> Canonical project definition, product thesis, architectural principles, and governance baseline.

---

## 1. Mission & Product Thesis

**CLOS (CISO Learning Operating System)** is an open-source, hands-on framework for developing **Technical CISOs, Security Architects, and DevSecOps Leaders**. 

Most cybersecurity educational resources either stay high-level (theoretical risk frameworks and slide decks) or hyper-specialized (isolated CTF challenges and code snippets). CLOS bridges this gap by providing an end-to-end operational operating system spanning **secure code, cloud platform architecture, supply chain assurance, machine-readable evidence (OSCAL), enterprise risk quantification, and board decision-making**.

### The Core Differentiator: The Evidence Chain
CLOS is built upon a non-negotiable **Evidence Chain**:

```
Threat ➔ Requirement ➔ Architecture Decision ➔ Control ➔ Implementation ➔ Test ➔ Evidence ➔ Risk Metric ➔ Executive Decision
```

Every security claim in CLOS must be backed by an automated test, cryptographic signature, policy gate, or machine-readable attestation.

---

## 2. Target Audiences

1. **Aspiring & Practicing Technical CISOs**: Security leaders who need deep technical fluency across cloud infrastructure, AI models, and software supply chains to lead engineering teams and advise corporate boards.
2. **Security Architects & Principal Engineers**: Builders designing zero-trust cloud platforms, Policy-as-Code guardrails, and automated DevSecOps factories.
3. **DevSecOps & Platform Engineers**: Practitioners implementing shift-left CI/CD pipelines, container hardening, SBOM generation, and keyless cloud authentication.
4. **Security Auditors & Compliance Officers**: Risk professionals translating regulatory mandates (NIST SSDF, ISO 27001, SOC 2, EU AI Act) into machine-readable control evidence (OSCAL).

---

## 3. Scope: What CLOS Includes & Non-Goals

### What CLOS Includes
* **8 Core Capability Tracks**: Covering foundations to executive board operations.
* **Hands-on Flagship Labs**: Turnkey reference architectures with live CI/CD pipelines, IaC, and Policy-as-Code.
* **Evidence-Backed Control Registry**: Mapping technical controls to STRIDE threats, NIST SP 800-53, and OSCAL schemas.
* **Executive Translation Templates**: Decision memos, risk matrices, and board presentations derived directly from technical validation data.

### Explicit Non-Goals
* **Not a Commercial SaaS Product**: CLOS is an open educational operating system and reference architecture, not a commercial enterprise vendor product.
* **Not a Theoretical Textbook**: CLOS does not contain static slide decks or unsupported advice; every concept must be reproducible.
* **No Proprietary Vendor Lock-in**: All reference labs utilize open standards (OpenAPI, OPA Rego, SPDX, Cosign, Distroless, Terraform/OpenTofu).
* **No Unverified Claims**: A control is never marked "implemented" or "verified" without automated proof.

---

## 4. Architectural & Operational Principles

1. **Evidence over Assertion**: A control does not exist unless automated tests prove it.
2. **Fail-Closed by Default**: Security gates halt execution upon scanner failure or policy violation. No masking with `|| true` or soft-fails.
3. **Least Privilege & Keyless Identity**: Eliminate static credentials in favor of short-lived OIDC federation (WIF) and non-root containers.
4. **Changes Must Teach**: Every technical change articulates *Why* (risk context), *What* (architectural design), and *How* (concrete implementation).
5. **Separation of Concerns**: Clean isolation between untrusted ingress, application compute, data storage, and policy control planes.

---

## 5. Project Maturity Model

| Stage | Name | Description | Criteria |
| :---: | :--- | :--- | :--- |
| **M1** | **Foundation (v0.1)** | Core DevSecOps pipeline fail-closed, verified API contract, authentic evidence chain. | 100% fail-closed CI, passing unit tests, zero failure-masking. |
| **M2** | **AI & Workload (v0.2)** | Zero-Trust AI Security Gateway, MCP tool authorization broker, MITRE ATLAS telemetry. | Turnkey AI Gateway container, adversarial test suite passing. |
| **M3** | **Control Plane (v0.3)** | Executive CISO control plane, risk register, DAST integration, automated OSCAL generation. | Full STRIDE-to-OSCAL pipeline, risk metric dashboard. |
| **M4** | **Ecosystem (v1.0)** | Multi-track curriculum, community governance, reproducible releases. | Comprehensive 8-track capability model, active open-source contribution workflow. |

---

## 6. Measurable Success Criteria

* **100% Reproducibility**: Any developer can clone the repository and run the documented test suites locally with zero proprietary dependencies.
* **Zero False-Greens**: CI/CD pipelines deterministically fail on policy violations, CVE thresholds, or secret leaks.
* **Full Auditability**: 100% of claimed security controls map to verifiable evidence paths in [CONTROL_EVIDENCE_MATRIX.md](file:///Users/mananvora/CLOS_Kickoff_Mission/07_PRIMARY_PROJECT/CONTROL_EVIDENCE_MATRIX.md).
