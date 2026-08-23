# Roadmap — CISO Learning Operating System (CLOS)

> Sequenced release plan and technical milestones for CLOS.

---

## 🗺️ Milestone Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                             CLOS RELEASE ROADMAP                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [v0.1] Trustworthy Foundations & Flagship Secure Software Factory          │
│         • Fail-closed DevSecOps CI/CD, Bearer JWT Auth, OPA Policy Gate    │
│         • Status: In Progress (Target: Q3 2026)                             │
│                                                                             │
│  [v0.2] AI Security Engineering & MCP Broker Lab                            │
│         • Zero-Trust AI Security Gateway, Inbound/Outbound Guards           │
│         • Agentic Tool Interception, MITRE ATLAS Structured Telemetry       │
│         • Status: Planned (Target: Q4 2026)                                 │
│                                                                             │
│  [v0.3] Technical CISO Control Plane & Automated Assurance                  │
│         • Dynamic Risk Register, Automated DAST Scanning (OWASP ZAP)        │
│         • Machine-Readable OSCAL Generation & Executive Board Memos         │
│         • Status: Planned (Target: Q1 2027)                                 │
│                                                                             │
│  [v1.0] Community Operating System & Multi-Track Ecosystem                  │
│         • 8 Full Capability Tracks, Multi-Maintainer Governance             │
│         • Turnkey Cloud Deployments & Reproducible Release Automation       │
│         • Status: Planned (Target: Q2 2027)                                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📦 Detailed Milestone Breakdown

### 🎯 Version 0.1 — Trustworthy Foundations & Flagship Secure Software Factory
* **Goal**: Deliver an uncompromised, evidence-backed DevSecOps reference architecture.
* **Key Deliverables**:
  - [x] Fail-Closed 6-Stage CI/CD Pipeline (Gitleaks, Bandit, Semgrep, Checkov, OPA, Distroless, Trivy, Syft, Cosign).
  - [x] Zero-Dependency HMAC-SHA256 Bearer JWT Auth in FastAPI Microservice.
  - [x] Single Canonical Architecture Specification with C4 Container Diagram & ADRs.
  - [x] Single Canonical Control & Evidence Matrix mapping all controls to automated test evidence.
  - [x] Standard Apache-2.0 open-source licensing.
  - [ ] Generic learner template system and private learner directory structure (`.clos-local/`).
  - [ ] Open-source contributor infrastructure (`CONTRIBUTING.md`, `GOVERNANCE.md`, `SECURITY.md`).

---

### 🧠 Version 0.2 — AI Security Engineering & MCP Tool Broker Lab
* **Goal**: Build the flagship Zero-Trust AI Security Gateway and MCP Runtime Broker.
* **Key Deliverables**:
  - [ ] Inbound Prompt Injection & Multi-Turn Jailbreak Classifier (MITRE ATLAS AML.T0054).
  - [ ] Outbound Presidio PII & Secret Redaction Engine (AML.T0055).
  - [ ] Autonomous Agent MCP Tool Interceptor & OPA Rego Capability Gate (AML.T0048 / AML.T0057).
  - [ ] Ephemeral Docker Sandbox Execution Environment with dropped Linux capabilities (`CAP_DROP_ALL`).
  - [ ] Automated Adversarial Test Suite for LLMs & Agents.

---

### 📊 Version 0.3 — Technical CISO Control Plane & Automated Assurance
* **Goal**: Translate technical validation telemetry into executive risk metrics and board-level decisions.
* **Key Deliverables**:
  - [ ] Dynamic Risk Register deriving risk scores from active CI/CD scan outputs.
  - [ ] Automated DAST integration in pre-production staging (OWASP ZAP / Nuclei).
  - [ ] Machine-readable OSCAL Assessment Results (`oscal-ar`) generation from CI artifacts.
  - [ ] Executive Board Decision Memos and Budget Allocation trade-off templates.

---

### 🌐 Version 1.0 — Community Operating System & Multi-Track Ecosystem
* **Goal**: Expand into a comprehensive, multi-maintainer open-source learning ecosystem.
* **Key Deliverables**:
  - [ ] Completion of all 8 core capability tracks across Understand ➔ Design ➔ Build ➔ Validate ➔ Lead.
  - [ ] Multi-maintainer review and contribution governance model.
  - [ ] Automated release packaging and signed provenance for all reference labs.
