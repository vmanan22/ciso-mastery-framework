# Learning Log 📖

> A running journal of everything learned in CLOS. Update after every meaningful session.

---

## Log Entries

---

### Entry #1 — 2026-08-21

**Topic:** End-to-End SSDLC Architecture, Spec-Driven Development, GCP Workload Identity Federation, and 6-Stage CI/CD Security Gates

**Key Learnings:**
1. **Spec-Driven Development (SDD):** Defining API contracts (OpenAPI 3.1) and security schemas BEFORE code creates a verifiable single source of truth across engineering and security.
2. **Workload Identity Federation (WIF):** Eliminates static service account JSON keys by exchanging ephemeral GitHub Actions OIDC JWT tokens for short-lived (15 min) GCP IAM tokens.
3. **Defense-in-Depth Cloud IaC:** Provisions KMS Customer-Managed Encryption Keys (CMEK) with 90-day rotation, uniform bucket-level access, public access prevention, and object versioning for ~$0.06/month.
4. **Policy-as-Code (OPA/Rego):** Shift-left policy evaluation against Terraform plan JSON output creates non-bypassable automated compliance gates in CI/CD.

**New Terminology:**

| Term | Definition | Context |
|------|-----------|---------|
| **WIF (Workload Identity Federation)** | Keyless identity exchange between identity providers (OIDC) and cloud IAM. | Zero-secret CI/CD pipelines |
| **CMEK (Customer-Managed Key)** | Encryption keys generated and managed by the customer in Cloud KMS rather than the cloud provider. | Data-at-rest compliance |
| **Spec-Driven Development (SDD)** | Engineering approach where formal specifications (OpenAPI/Protobuf/Schemas) precede and govern implementation. | Secure SDLC foundations |
| **SARIF** | Static Analysis Results Interchange Format (JSON-based standard for security tools). | GitHub Code Scanning alerts |
| **SBOM (Software Bill of Materials)** | Formal machine-readable inventory of software components and dependencies (SPDX/CycloneDX). | Supply chain security |

**Mistakes Made / Lessons Learned:** _(also in Hall of Pain)_
- GitHub Actions only executes workflow files located in root `.github/workflows/`, not subdirectories.
- Pushing to `.github/workflows/` requires explicit `workflow` OAuth scope on git tokens.
- Hardcoded API keys in local client scripts must be scrubbed before git commits.

**Follow-Up Topics for Tomorrow:**
- [ ] Add JWT Authentication dependency to FastAPI routes (`main.py`) to satisfy OpenAPI spec.
- [ ] Run live end-to-end SAST / Container build / Cloud deploy verification.
- [ ] Implement DAST testing sandbox for API endpoints.

**Confidence Level (1-5):** 4.5/5

---


<!-- Copy the entry template above for each new entry -->

---

## Monthly Summary

### Month 1 — [Date Range]

**Skills Practiced:**
-

**Biggest Breakthroughs:**
-

**Persistent Gaps:**
-

**Focus for Next Month:**
-
