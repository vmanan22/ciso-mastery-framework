# CLOS Learner & Contributor Templates

> Reusable engineering and leadership templates for learners, architects, and contributors.

---

## 📁 Available Templates

| Template | Purpose | Typical Use Case |
| :--- | :--- | :--- |
| [`LEARNER_PROFILE_TEMPLATE.md`](LEARNER_PROFILE_TEMPLATE.md) | Baseline skills and learning goals | Initial onboarding in private `.clos-local/` |
| [`LEARNER_PLAN_TEMPLATE.md`](LEARNER_PLAN_TEMPLATE.md) | Structured milestone execution plan | Planning multi-week capability track progression |
| [`LAB_RECORD_TEMPLATE.md`](LAB_RECORD_TEMPLATE.md) | Step-by-step lab execution notes | Documenting hands-on technical labs |
| [`ADR_TEMPLATE.md`](ADR_TEMPLATE.md) | Architectural Decision Record | Proposing architecture choices with trade-offs |
| [`VALIDATION_REPORT_TEMPLATE.md`](VALIDATION_REPORT_TEMPLATE.md) | Automated testing & security scan report | Submitting evidence for a pull request |
| [`RETROSPECTIVE_TEMPLATE.md`](RETROSPECTIVE_TEMPLATE.md) | Post-mortem & failure root-cause analysis | Analyzing incidents, bugs, and pipeline failures |
| [`EXECUTIVE_DECISION_MEMO_TEMPLATE.md`](EXECUTIVE_DECISION_MEMO_TEMPLATE.md) | Board / Executive Risk Memo | Translating technical evidence into business decisions |

---

## 🔒 Privacy & Local Conventions

Learners are encouraged to keep private notes, target timelines, and personal career goals in the local `.clos-local/` directory:

```bash
# Initialize local private learner workspace (automatically ignored by git)
mkdir -p .clos-local
cp templates/LEARNER_PROFILE_TEMPLATE.md .clos-local/my_profile.md
cp templates/LEARNER_PLAN_TEMPLATE.md .clos-local/my_plan.md
```

Public contributions demonstrate progress through **code, pull requests, automated tests, ADRs, and evidence artifacts**.
