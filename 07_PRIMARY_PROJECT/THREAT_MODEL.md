# Threat Model — AI-Powered Secure SDLC Platform

> STRIDE-based threat model. Updated as the architecture evolves.

---

## Scope

**System**: AI-Powered Secure SDLC Platform
**Version**: 0.1 (Initial)
**Last Updated**: _TBD_

---

## Assets

| ID | Asset | Sensitivity | Description |
|----|-------|------------|-------------|
| A1 | Source code (customer) | 🔴 Critical | Customer source code analyzed by the platform |
| A2 | Vulnerability findings | 🔴 Critical | Security vulnerabilities found in customer code |
| A3 | User credentials | 🔴 Critical | Authentication tokens, API keys |
| A4 | AI model / prompts | 🟡 High | Proprietary AI models and prompt templates |
| A5 | Audit logs | 🟡 High | Who did what, when |
| A6 | Configuration data | 🟡 High | Platform and integration settings |

---

## STRIDE Analysis

### S — Spoofing (Identity)

| # | Threat | Target | Likelihood | Impact | Mitigation | Status |
|---|--------|--------|------------|--------|------------|--------|
| S1 | Attacker impersonates a developer to access findings | AuthN | | | | ⬜ |
| S2 | Compromised CI/CD token used to submit malicious code for analysis | API | | | | ⬜ |

### T — Tampering (Data Integrity)

| # | Threat | Target | Likelihood | Impact | Mitigation | Status |
|---|--------|--------|------------|--------|------------|--------|
| T1 | Attacker modifies vulnerability findings to hide issues | Database | | | | ⬜ |
| T2 | Tampering with AI model/prompts to produce incorrect results | AI Service | | | | ⬜ |

### R — Repudiation (Accountability)

| # | Threat | Target | Likelihood | Impact | Mitigation | Status |
|---|--------|--------|------------|--------|------------|--------|
| R1 | User denies suppressing a critical vulnerability | Audit | | | | ⬜ |
| R2 | No audit trail for AI-generated recommendations | AI Service | | | | ⬜ |

### I — Information Disclosure (Confidentiality)

| # | Threat | Target | Likelihood | Impact | Mitigation | Status |
|---|--------|--------|------------|--------|------------|--------|
| I1 | Customer source code leaked to unauthorized parties | Storage | | | | ⬜ |
| I2 | Source code sent to external LLM API without controls | AI Service | | | | ⬜ |
| I3 | Vulnerability findings exposed to unauthorized users | API | | | | ⬜ |

### D — Denial of Service (Availability)

| # | Threat | Target | Likelihood | Impact | Mitigation | Status |
|---|--------|--------|------------|--------|------------|--------|
| D1 | Attacker submits massive codebase to exhaust resources | Analysis | | | | ⬜ |
| D2 | AI service rate-limited or unavailable | AI Service | | | | ⬜ |

### E — Elevation of Privilege

| # | Threat | Target | Likelihood | Impact | Mitigation | Status |
|---|--------|--------|------------|--------|------------|--------|
| E1 | Developer escalates to admin role | AuthZ | | | | ⬜ |
| E2 | Prompt injection to make AI perform unintended actions | AI Service | | | | ⬜ |

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────┐
│              [TO BE COMPLETED]                    │
│                                                   │
│  Draw DFD once architecture is finalized.        │
│  Include trust boundaries, data stores,          │
│  processes, and external entities.               │
│                                                   │
└─────────────────────────────────────────────────┘
```

---

## Risk Matrix

| Likelihood ↓ / Impact → | Low | Medium | High | Critical |
|--------------------------|-----|--------|------|----------|
| **Almost Certain** | 🟡 | 🟠 | 🔴 | 🔴 |
| **Likely** | 🟢 | 🟡 | 🟠 | 🔴 |
| **Possible** | 🟢 | 🟡 | 🟡 | 🟠 |
| **Unlikely** | 🟢 | 🟢 | 🟡 | 🟡 |
| **Rare** | 🟢 | 🟢 | 🟢 | 🟡 |

---

*Update this threat model whenever the architecture changes or new features are added.*
