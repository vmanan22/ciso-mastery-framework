# Technical Retrospective & Failure Case Study Template

> Objective post-mortem and root-cause analysis template for incidents, bugs, and pipeline failures.

---

## 📋 Case Metadata

* **Incident / Failure Title**: [e.g., False-Green Pipeline Masking Due to Trailing OR-True]
* **Impact Level**: [P0 - Critical / P1 - High / P2 - Medium / P3 - Low]
* **Discovery Date**: [YYYY-MM-DD]
* **Resolution Date**: [YYYY-MM-DD]

---

## 1. What Happened? (The Symptoms)

[Concise technical description of the failure as observed by users, CI/CD, or automated alerting.]

---

## 2. Technical Root Cause (The Mechanism)

[Deep-dive into the underlying technical flaw, misconfiguration, or architectural gap that enabled the failure.]

```
[System Input] ──► [Flawed Component / Masking Pattern] ──► [Incorrect Output / False Green]
```

---

## 3. Evidence & Reproduction

* **Reproduction Command**:
  ```bash
  # Exact command to reproduce the issue
  ```
* **Failure Output**:
  ```text
  [Paste error log or reproduction output]
  ```

---

## 4. Corrective Actions Taken

1. **Immediate Remediation**: [e.g., Removed `|| true` from workflow steps and enforced strict exit codes.]
2. **Automated Regression Guard**: [e.g., Added `scripts/verify_fail_closed.py` into the CI pre-flight gate.]
3. **Documentation & Process Update**: [e.g., Updated CONTRIBUTING.md with anti-masking standards.]

---

## 5. CISO Leadership Lesson

[How should a Technical CISO communicate this failure to executive leadership and what systemic guardrail prevents recurrence?]
