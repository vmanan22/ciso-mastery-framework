# Project Governance — CISO Learning Operating System (CLOS)

> Transparent governance model defining maintainer roles, contributor progression, decision-making, and review boundaries.

---

## 🏛️ Governance Structure

CLOS operates as an open-source, meritocratic project guided by technical maintainers and peer reviewers.

```
┌─────────────────────────────────────────────────────────────┐
│                    LEAD MAINTAINER (CISO)                   │
│      • Final architectural authority and release signer     │
│      • Ensures strategic adherence to the Evidence Chain    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│               TRACK MAINTAINERS & REVIEWERS                 │
│      • Domain owners for specific capability tracks         │
│      • Review pull requests, triage issues, maintain labs   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  CONTRIBUTORS & LEARNERS                    │
│      • Propose code, labs, ADRs, test cases, and fixes      │
└─────────────────────────────────────────────────────────────┘
```

---

## 👥 Roles & Responsibilities

### 1. Lead Maintainer
* **Responsibilities**: Overall architectural consistency, release authorization, dispute resolution, and security escalation handling.
* **Appointment**: Founding role.

### 2. Track Maintainers
* **Responsibilities**: Review and approve pull requests within their specific track (e.g., Track 3: DevSecOps, Track 5: AI Security), ensure tests pass, and keep documentation accurate.
* **Progression Pathway**: Any contributor who demonstrates sustained, high-quality contributions (3+ merged non-trivial PRs, comprehensive test coverage, active peer reviews) may be nominated as a Track Maintainer.

### 3. Reviewers
* **Responsibilities**: Conduct code and architectural reviews on incoming pull requests, verify the Evidence Chain, and assist new contributors.

---

## 🗳️ Decision-Making Process (RFCs)

1. **Standard Changes**: Bug fixes, test additions, and documentation improvements are proposed via pull requests and merged upon approval by at least one Maintainer.
2. **Major Architectural Changes**: New capability tracks, breaking API changes, or major framework adoptions require an **Architectural Decision Record (ADR)** submitted as a draft PR for community discussion.
3. **Consensus & Dispute Resolution**: Decisions are made through technical consensus. If consensus cannot be reached, the Lead Maintainer has the final tie-breaking responsibility.

---

## 🔄 Inactivity & Offboarding

Maintainers who are inactive for more than 6 months will be transitioned to an Emeritus status to ensure the review process remains responsive and active.
