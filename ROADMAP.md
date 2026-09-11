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
│         • Status: Release Candidate — Local/CI Evidence Complete; Cloud      │
│           Validation Pending                                                  │
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
│  [Post-v0.3 Capstone] Evidence-Backed vCISO Engagement Simulator             │
│         • Cross-Track Capstone synthesizing Tracks 2, 6, 7, and 8           │
│         • Evidence feeds from DevSecOps (T3), Cloud (T4), and AI (T5)       │
│         • Status: Planned (Target: Q2 2027)                                 │
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

### 🎯 Version 0.1 — Trustworthy Foundations & Flagship Secure Software Factory (v0.1-RC)
* **Goal**: Deliver an uncompromised, evidence-backed DevSecOps reference architecture.
* **Status**: *Release Candidate — Local/CI Evidence Complete; Cloud Validation Pending* (Target: Q3 2026).
* **Key Deliverables**:
  - [x] Fail-Closed 6-Stage CI/CD Pipeline (Gitleaks, Bandit, Semgrep, Checkov, OPA, Hardened Container, Trivy, Syft, Cosign).
  - [x] Zero-Dependency HMAC-SHA256 Bearer JWT Auth with RFC 7519 Standard Claims in FastAPI Microservice.
  - [x] Single Canonical Architecture Specification with C4 Container Diagram & ADRs.
  - [x] Single Canonical Control & Evidence Matrix mapping all controls to automated test evidence.
  - [x] Standard Apache-2.0 open-source licensing.
  - [x] Generic learner template system and private learner directory structure (`.clos-local/`).
  - [x] Open-source contributor infrastructure (`CONTRIBUTING.md`, `GOVERNANCE.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`).
  - [x] Local/CI evidence reconciliation, including immutable container digest signing and verification.
  - [ ] Optional controlled GCP validation of Workload Identity Federation, CMEK storage, and deployment stages.

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

### 🎓 Post-v0.3 Capstone — Evidence-Backed vCISO Engagement Simulator
* **Goal**: Provide a cross-track capstone experience synthesizing technical control assurance into end-to-end executive advisory deliverables.
* **Primary Synthesis Tracks**: Track 2 (Security Architecture), Track 6 (Assurance, Validation, Red Teaming & Pentesting), Track 7 (Security Operations & Resilience), and Track 8 (CISO Operations, Enterprise Risk, Budgeting & Board Communication).
* **Technical Evidence Feeds**: Consumes machine-readable evidence produced by Track 3 (DevSecOps), Track 4 (Cloud Security), and Track 5 (AI Security).
* **Key Deliverables**:
  - [ ] Engagement Scope & Charter Template for synthetic organization (e.g., *Acme FinTech*).
  - [ ] Evidence-Confidence Assessment evaluating machine-readable scanner outputs.
  - [ ] Dynamic Risk Register mapping CI/CD findings to quantifiable business impact (FAIR / CVSS).
  - [ ] Control Remediation Roadmap with prioritized technical milestones.
  - [ ] Budget & ROSI Scenario Modeling (trade-offs between remediation cost vs. breach loss expectancy).
  - [ ] Executive Board Decision Memo & QBR Presentation Deck.
  - [ ] Client Handover Package with audit-ready OSCAL compliance records.
* **Non-Goals & Constraints**:
  - Does *not* introduce a 9th track (remains a capstone synthesizing the 8 core CLOS tracks).
  - Uses 100% synthetic organizational profiles (no proprietary or individual-specific data).
  - Implementation commences only after v0.1, v0.2, and v0.3 provide live evidence feeds.

---

### 🌐 Version 1.0 — Community Operating System & Multi-Track Ecosystem
* **Goal**: Expand into a comprehensive, multi-maintainer open-source learning ecosystem.
* **Key Deliverables**:
  - [ ] Completion of all 8 core capability tracks across Understand ➔ Design ➔ Build ➔ Validate ➔ Lead.
  - [ ] Multi-maintainer review and contribution governance model.
  - [ ] Automated release packaging and signed provenance for all reference labs.
