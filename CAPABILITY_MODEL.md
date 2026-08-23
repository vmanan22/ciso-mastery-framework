# Capability Model — CISO Learning Operating System (CLOS)

> Canonical taxonomy of 8 core technical and leadership tracks. Every track follows the uniform progression: **Understand ➔ Design ➔ Build ➔ Validate ➔ Lead**.

---

## 🧭 The 5-Stage Progression Framework

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  UNDERSTAND  │ ──► │    DESIGN    │ ──► │    BUILD     │ ──► │   VALIDATE   │ ──► │     LEAD     │
│  Threats &   │     │ Architecture │     │ Hands-on     │     │ Automated    │     │ Executive    │
│  Standards   │     │  & Controls  │     │ Code & IaC   │     │ Tests & Gate │     │ Translation  │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
```

---

## 📚 The 8 Capability Tracks

### Track 1: Security Engineering Foundations
* **Understand**: Cryptography fundamentals (symmetric/asymmetric, HMAC, TLS 1.3, PKI), memory safety, identity protocols (OAuth2, OIDC, SAML).
* **Design**: Zero-trust identity architecture, cryptographic key lifecycle, token exchange flows.
* **Build**: Zero-dependency HMAC-SHA256 JWT validators, mutual TLS (mTLS) certificate authorities.
* **Validate**: Cryptographic unit test suites, token tampering tests, signature verification benchmarks.
* **Lead**: Authoring cryptographic standards and enterprise identity modernization roadmaps.
* **Maturity**: `implemented`

---

### Track 2: Security Architecture
* **Understand**: Threat modeling frameworks (STRIDE, PASTA), C4 architecture modeling, trust boundaries.
* **Design**: System context diagrams, container boundaries, defense-in-depth isolation layers, Architectural Decision Records (ADRs).
* **Build**: Spec-driven API contracts (OpenAPI 3.1), architectural boundary enforcement.
* **Validate**: Threat-to-control traceability verification, architectural linter checks.
* **Lead**: Defending architecture designs before executive review boards and enterprise architecture committees.
* **Maturity**: `implemented`

---

### Track 3: Secure Software & DevSecOps
* **Understand**: OWASP Top 10, CWE/SANS Top 25, NIST SP 800-218 (SSDF), software supply chain security (SLSA).
* **Design**: 6-stage fail-closed CI/CD pipeline, pre-commit quality gates, dependency vulnerability triage policies.
* **Build**: GitHub Actions workflows, Semgrep AST rules, Bandit linters, Gitleaks secret hooks.
* **Validate**: Automated pipeline integrity tests, SARIF report validation, negative vulnerability injection tests.
* **Lead**: Measuring mean time to remediate (MTTR), developer security enablement, and SSDLC KPI reporting.
* **Maturity**: `verified` (Flagship Lab v0.1)

---

### Track 4: Cloud, Platform, Kubernetes, IaC & Policy as Code
* **Understand**: Cloud shared responsibility, CIS Benchmarks, Keyless Identity (WIF), Policy-as-Code (OPA Rego).
* **Design**: Immutable infrastructure topologies, CMEK encryption at rest, uniform cloud storage access policies.
* **Build**: Terraform / OpenTofu modules, Google Cloud Storage & Cloud KMS CMEK, OPA Rego policy suites.
* **Validate**: Checkov IaC security scans, Conftest OPA evaluations against Terraform plan JSON.
* **Lead**: Cloud security budget optimization, multi-cloud governance, and infrastructure exception management.
* **Maturity**: `verified` (Flagship Lab v0.1)

---

### Track 5: AI Security & AI Engineering
* **Understand**: OWASP Top 10 for LLMs & Agentic Applications (2026), MITRE ATLAS, NIST AI RMF 1.0, Gartner AI TRiSM.
* **Design**: Zero-Trust AI Security Gateway, MCP tool authorization broker, input/output inspection gates.
* **Build**: Inbound prompt injection guards, outbound Presidio PII maskers, hardened Docker execution sandboxes.
* **Validate**: Automated adversarial prompt injection & jailbreak test suites.
* **Lead**: Enterprise AI Acceptable Use Policies (AUP), ISO/IEC 42001 compliance, and Shadow AI governance.
* **Maturity**: `in progress` (Milestone v0.2)

---

### Track 6: Assurance, Validation, Red Teaming & Pentesting
* **Understand**: Hypothesis-led penetration testing, MITRE ATT&CK adversary emulation, DAST methodologies.
* **Design**: Automated security test harnesses, red team attack playbooks, continuous validation schedules.
* **Build**: Dynamic API fuzzers, OWASP ZAP automated scan jobs, automated exploit verification scripts.
* **Validate**: Control failure detection rates, security telemetry ingestion verification.
* **Lead**: Translating red team findings into executive risk remediation budgets and defense investments.
* **Maturity**: `planned` (Milestone v0.3)

---

### Track 7: Security Operations & Resilience
* **Understand**: SOC operations, SIEM telemetry correlation, incident response playbooks (NIST SP 800-61), disaster recovery.
* **Design**: Structured MITRE ATT&CK/ATLAS telemetry schemas, alerting thresholds, containment workflows.
* **Build**: Cryptographic audit log sinks, SHA-256 tamper-evident event buffers, automated containment scripts.
* **Validate**: Chaos engineering & incident simulation exercises, MTTR benchmarking.
* **Lead**: Incident post-mortems, board breach communication, and business continuity strategy.
* **Maturity**: `in progress`

---

### Track 8: CISO Operations, Enterprise Risk, Budgeting & Board Communication
* **Understand**: Enterprise risk quantification (FAIR), regulatory frameworks (SOC 2, ISO 27001, SEC Cyber Disclosure, EU NIS2).
* **Design**: Machine-readable control schemas (NIST OSCAL), risk registries, security budget models.
* **Build**: OSCAL component definitions, risk quantification calculators, executive reporting pipelines.
* **Validate**: Automated audit evidence compilation, control gap analysis scripts.
* **Lead**: Authoring Board of Directors cybersecurity updates, CAPEX/OPEX security investment trade-offs.
* **Maturity**: `in progress`
