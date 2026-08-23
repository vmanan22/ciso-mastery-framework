# Contributing to CLOS

> Welcome! We are excited to collaborate with engineers, architects, and security leaders to build the definitive Technical CISO operating system.

---

## 🏛️ Guiding Principles for Contributions

All contributions to CLOS must adhere to the **Evidence Chain**:

```
Threat ➔ Requirement ➔ Architecture Decision ➔ Control ➔ Implementation ➔ Test ➔ Evidence ➔ Risk Metric ➔ Executive Decision
```

1. **Evidence over Assertion**: Code, architecture changes, and policies must include automated tests or reproducible evidence.
2. **Fail-Closed Default**: Never use `|| true`, `--soft-fail`, or synthetic fallback artifacts.
3. **Changes Must Teach**: Explain *Why* (risk context), *What* (architecture), and *How* (implementation).
4. **No Unverified Claims**: Never mark a control "implemented" without automated test coverage.

---

## 🛠️ Local Development & Setup

### Prerequisites
* Python 3.11+
* Git
* Terraform / OpenTofu (for cloud IaC tracks)

### Running Automated Test Suites
```bash
# 1. Verify fail-closed pipeline integrity (0 anti-patterns allowed)
python3 scripts/verify_fail_closed.py

# 2. Run unit and cryptographic tests
PYTHONPATH=. python3 -m unittest discover -s tests -p "test_*.py"
PYTHONPATH=07_PRIMARY_PROJECT python3 -m unittest discover -s 07_PRIMARY_PROJECT/tests -p "test_*.py"
```

---

## 🌿 Branch & Commit Conventions

### Branch Naming
* `feat/[feature-name]` — New capability track, lab, or control implementation.
* `fix/[bug-name]` — Bug fixes, CI/CD corrections, or policy adjustments.
* `docs/[doc-name]` — Documentation, ADRs, or curriculum updates.
* `refactor/[refactor-name]` — Template improvements or architectural refactoring.

### Commit Messages (Conventional Commits)
```text
feat(iac): add OPA Rego rule enforcing 90-day KMS key rotation
fix(ci): remove failure masking from Semgrep SAST step
docs(charter): define maturity criteria for milestone v0.2
test(jwt): add expired token rejection unit tests
```

---

## 📋 Pull Request Submission & Review Process

1. **Fork and Branch**: Create a focused branch for your change.
2. **Run Tests**: Ensure all automated tests pass locally before opening a PR.
3. **Use the PR Template**: Complete all sections of `.github/PULL_REQUEST_TEMPLATE.md`.
4. **Update Control Matrix**: If implementing a new control, update `07_PRIMARY_PROJECT/CONTROL_EVIDENCE_MATRIX.md`.
5. **Review**: Maintainers will review and provide technical feedback.

---

## 🏁 Definition of Done (DoD)

A pull request is considered ready for merge when:
- [ ] Automated tests prove the functionality (both positive and negative paths).
- [ ] No failure-masking patterns exist (`scripts/verify_fail_closed.py` passes).
- [ ] Documentation and architectural decision records (ADRs) are updated.
- [ ] Control status is accurately reflected in the evidence matrix.
- [ ] CI/CD pipeline runs and passes completely without soft-fails.
