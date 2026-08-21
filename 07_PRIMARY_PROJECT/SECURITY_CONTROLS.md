# Security Controls Registry — AI-Powered Secure SDLC Platform

> Tracks all security controls, implementation status, and mapping to STRIDE threats and compliance frameworks.

---

## Controls Registry

| ID | Control | Category | Threat(s) Mitigated | Framework Mapping | Priority | Status |
|----|---------|----------|--------------------|--------------------|----------|--------|
| SC-01 | Short-lived OIDC tokens for CI/CD Cloud Access | Authentication | S2, I3 | NIST SSDF PO.3, ISO 27001 A.9.4.2 | 🔴 Critical | ✅ Implemented |
| SC-02 | Role-based access control (RBAC) in CI/CD & Cluster | Authorization | E1, I3 | SOC 2 CC6.3, ISO 27001 A.9.2.3 | 🔴 Critical | ✅ Implemented |
| SC-03 | KMS AES-256 Encryption at rest for state & data | Data Protection | I1, I2 | SOC 2 CC6.7, ISO 27001 A.10.1.1 | 🔴 Critical | ✅ Implemented |
| SC-04 | TLS 1.3 in transit with mTLS between internal pods | Data Protection | I1 | SOC 2 CC6.7, ISO 27001 A.13.1.1 | 🔴 Critical | 🔨 In progress |
| SC-05 | Immutable append-only audit trail & SHA256 integrity | Audit | R1, T1 | SOC 2 CC7.2, ISO 27001 A.12.4.1 | 🟡 High | ✅ Implemented |
| SC-06 | SAST & SCA scanning prior to code merge | Application | T1, E2 | OWASP ASVS V5, NIST SSDF PW.4 | 🔴 Critical | ✅ Implemented |
| SC-07 | IaC Policy-as-Code enforcement (OPA / Rego) | Infrastructure | I1, R2 | SOC 2 CC7.1, CIS Benchmark | 🔴 Critical | ✅ Implemented |
| SC-08 | Container security: Distroless base & non-root user | Workload | E2 | CIS Docker Benchmark 4.1 | 🔴 Critical | 🔨 In progress |
| SC-09 | Signed container images (Cosign / Sigstore) | Supply Chain | T2, E2 | SLSA Level 3, NIST SSDF PW.8 | 🟡 High | 🔨 In progress |
| SC-10 | DAST scans on active endpoints prior to production | Runtime | I2, D1 | OWASP ASVS V14 | 🟡 High | 🔨 In progress |

---

## Control Coverage Metrics

| Category | Count | Implemented | Coverage |
|----------|-------|-------------|----------|
| Authentication | 1 | 1 | 100% |
| Authorization | 1 | 1 | 100% |
| Data Protection | 2 | 1 | 50% |
| Audit | 1 | 1 | 100% |
| Application | 1 | 1 | 100% |
| Infrastructure | 1 | 1 | 100% |
| Workload | 1 | 0 | 0% |
| Supply Chain | 1 | 0 | 0% |
| Runtime | 1 | 0 | 0% |
| **Total** | **10** | **6** | **60%** |

---

## Status Legend

| Status | Meaning |
|--------|---------|
| ⬜ Not started | Control defined but not yet implemented |
| 🔨 In progress | Currently being built / tested |
| ✅ Implemented | Verified active control |
