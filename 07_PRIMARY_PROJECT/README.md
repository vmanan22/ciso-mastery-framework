# Flagship Lab 01 — Secure Software Factory (v0.1)

> An end-to-end reference implementation of a hardened, spec-driven DevSecOps software factory.

---

## 🎯 Lab Overview & Learner Outcomes

This flagship lab demonstrates how to design, build, validate, and govern a production-grade software factory enforcing the **Evidence Chain**:

```
Threat ➔ Requirement ➔ Architecture Decision ➔ Control ➔ Implementation ➔ Test ➔ Evidence ➔ Risk Metric ➔ Executive Decision
```

### What You Will Master
1. **Understand**: STRIDE threat modeling and NIST SP 800-218 (SSDF) requirements.
2. **Design**: Spec-first API contracts (OpenAPI 3.1) and zero-trust cloud architecture.
3. **Build**: Hardened FastAPI microservice, minimal non-root containers, and 6-stage fail-closed CI/CD pipelines.
4. **Validate**: Policy-as-Code (OPA Rego), AST security scanning (Semgrep/Bandit), and automated cryptographic test suites.
5. **Lead**: Translating validation evidence into board-level risk metrics and executive decision memos.

---

## 📁 Lab Components

```
07_PRIMARY_PROJECT/
├── README.md                      # Lab Overview & Quickstart
├── LAB_GUIDE.md                   # Step-by-Step 5-Stage Execution Walkthrough
├── ARCHITECTURE.md                # C4 Architecture Model & ADR Decision Matrix
├── THREAT_MODEL.md                # STRIDE Threat Model & Control Mappings
├── CONTROL_EVIDENCE_MATRIX.md     # Traceable Control Status & Verification Links
├── EXECUTIVE_DECISION_MEMO.md     # Board-Level Risk & Budget Allocation Memo
├── containers/
│   ├── Dockerfile.hardened        # Multi-stage Minimal Non-Root Container
│   └── app/
│       ├── main.py                # Hardened FastAPI App with Bearer JWT
│       └── jwt_validator.py       # Zero-Dependency RFC 7519 JWT Engine
├── iac/environments/gcp-dev/      # Hardened Terraform IaC (CMEK + Uniform GCS)
├── policies/iac_policies/         # OPA / Rego Policy-as-Code Guardrails
├── docs/
│   ├── openapi.yaml               # OpenAPI 3.1 Spec-Driven API Contract
│   └── oscal/                     # Machine-Readable NIST SP 800-53 OSCAL Model
└── tests/                         # Automated Unit & Cryptographic Test Suite
```

---

## 🚀 Quickstart & Verification

Run the entire verification suite locally in one command:

```bash
# Run fail-closed pipeline verifier and cryptographic unit tests
python3 scripts/verify_fail_closed.py && \
PYTHONPATH=. python3 -m unittest discover -s tests -p "test_*.py" && \
PYTHONPATH=07_PRIMARY_PROJECT python3 -m unittest discover -s 07_PRIMARY_PROJECT/tests -p "test_*.py"
```

*For complete step-by-step instructions, see [LAB_GUIDE.md](LAB_GUIDE.md).*
