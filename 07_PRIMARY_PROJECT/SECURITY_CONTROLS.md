# Security Controls Registry — AI-Powered Secure SDLC Platform

> Tracks all security controls, their implementation status, and mapping to threats and compliance frameworks.

---

## Controls

| ID | Control | Category | Threat(s) Mitigated | Framework Mapping | Priority | Status |
|----|---------|----------|--------------------|--------------------|----------|--------|
| SC-01 | Multi-factor authentication for all users | Authentication | S1 | SOC 2 CC6.1, ISO 27001 A.9.4.2 | 🔴 Critical | ⬜ Not started |
| SC-02 | Role-based access control (RBAC) | Authorization | E1, I3 | SOC 2 CC6.3, ISO 27001 A.9.2.3 | 🔴 Critical | ⬜ Not started |
| SC-03 | Encryption at rest for all data stores | Data Protection | I1, I2 | SOC 2 CC6.7, ISO 27001 A.10.1.1 | 🔴 Critical | ⬜ Not started |
| SC-04 | TLS 1.3 for all data in transit | Data Protection | I1 | SOC 2 CC6.7, ISO 27001 A.13.1.1 | 🔴 Critical | ⬜ Not started |
| SC-05 | Comprehensive audit logging | Audit | R1, R2 | SOC 2 CC7.2, ISO 27001 A.12.4.1 | 🟡 High | ⬜ Not started |
| SC-06 | Input validation and sanitization | Application | T1, E2 | OWASP ASVS V5 | 🟡 High | ⬜ Not started |
| SC-07 | Rate limiting and resource quotas | Availability | D1, D2 | SOC 2 CC7.1 | 🟡 High | ⬜ Not started |
| SC-08 | Prompt injection prevention | AI Security | E2, T2 | OWASP LLM01 | 🟡 High | ⬜ Not started |
| SC-09 | Source code isolation (no external LLM) | Data Protection | I2 | Custom | 🔴 Critical | ⬜ Not started |
| SC-10 | API authentication (OAuth2 / API keys) | Authentication | S2 | SOC 2 CC6.1 | 🔴 Critical | ⬜ Not started |

---

## Control Categories

| Category | Count | Implemented | Coverage |
|----------|-------|-------------|----------|
| Authentication | 2 | 0 | 0% |
| Authorization | 1 | 0 | 0% |
| Data Protection | 3 | 0 | 0% |
| Audit | 1 | 0 | 0% |
| Application | 1 | 0 | 0% |
| Availability | 1 | 0 | 0% |
| AI Security | 1 | 0 | 0% |

---

## Status Legend

| Status | Meaning |
|--------|---------|
| ⬜ Not started | Control not yet implemented |
| 🔨 In progress | Currently being implemented |
| ✅ Implemented | Implemented and verified |
| 🧪 Testing | Implemented, undergoing testing |
| ❌ Failed | Implementation attempted, issues found |

---

*Update this registry as controls are designed and implemented.*
