# Technical Retrospectives & Failure Case Studies

> Objective analysis of real-world failures, root causes, and prevention strategies.

---

## 📋 Case Study Registry

| # | Date | Category | Incident / Failure | Root Cause | Systemic Prevention Strategy |
|:---:|:---:|:---:|:---|:---|:---|
| **1** | 2026-08-21 | Process / CI | Workflows placed in subdirectories were not triggered by GitHub Actions | GitHub Actions runner strictly parses `.github/workflows/*.yml` at root | Enforce pipeline linter in CI to verify workflow placement |
| **2** | 2026-08-21 | Security / Git | Pushing workflow modifications was rejected by GitHub remote | Git CLI personal token lacked explicit `workflow` OAuth scope | Restrict `workflow` scope to authorized CI maintainers; use keyless OIDC |
| **3** | 2026-08-21 | Security / Code | Hardcoded API key detected in local prototyping script | Placeholder secret committed during rapid iteration | Shift-left pre-commit hooks (`gitleaks`, `semgrep`) blocking commits before push |
| **4** | 2026-08-23 | CI / Governance | CI pipeline reported green despite scanner failures | Trailing `\|\| true` and `--soft-fail` masked scanner exit codes | Implemented `scripts/verify_fail_closed.py` and fail-closed gates |

---

## 🔬 Failure Categories

* **Security**: Missed vulnerability, weak control, unauthorized access, insecure default.
* **Architecture**: Anti-pattern, unmitigated threat, excessive coupling, lack of trust boundary.
* **Code Quality**: Missing unit/regression tests, edge-case failure, unhandled exception.
* **Supply Chain**: Unpinned action, mutable dependency tag, unverified signature.
* **Pipeline Integrity**: False-green masking, skipped prerequisite, unverified deployment.

---

## 📝 Submitting a New Retrospective

To add a new retrospective or failure case study, use [`templates/RETROSPECTIVE_TEMPLATE.md`](../templates/RETROSPECTIVE_TEMPLATE.md).
