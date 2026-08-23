# ADR-[Number]: [Architecture Decision Title]

> Standard Architectural Decision Record (ADR) template.

---

## 📋 Metadata

* **Status**: [PROPOSED / ACCEPTED / SUPERSEDED / REJECTED]
* **Deciders**: [e.g., Security Architecture Working Group]
* **Date**: [YYYY-MM-DD]
* **Related Controls**: [e.g., SC-01, SC-07]

---

## 1. Context & Problem Statement

[Describe the context, technical constraints, business requirements, and security risks driving this decision.]

---

## 2. Decision Drivers

* [Driver 1: e.g., Eliminate credential leak risk from static JSON service account keys]
* [Driver 2: e.g., Support multi-cloud and GitHub Actions automated deployment]
* [Driver 3: e.g., Minimize monthly infrastructure overhead to $0.00 base cost]

---

## 3. Considered Options

1. **Option 1**: [Option Title — e.g., Long-Lived Service Account Keys stored in GitHub Secrets]
2. **Option 2**: [Option Title — e.g., GCP Workload Identity Federation (WIF) with OIDC exchange]
3. **Option 3**: [Option Title — e.g., HashiCorp Vault Dynamic Secret Engine]

---

## 4. Decision Outcome

**Chosen Option**: **Option [X]** ([Option Title])

### Positive Consequences
* [Benefit 1: e.g., 100% elimination of static secret storage in CI/CD]
* [Benefit 2: e.g., Granular attribute condition mapping to repository and branch]

### Negative Consequences / Trade-offs
* [Trade-off 1: e.g., Initial setup complexity with STS and IAM provider configuration]
* [Trade-off 2: e.g., Requires explicit WIF provider updates upon repository rename]

---

## 5. Implementation & Verification Plan

* **Implementation Path**: [e.g., `07_PRIMARY_PROJECT/iac/environments/gcp-dev/main.tf`]
* **Validation Method**: [e.g., Automated OIDC token exchange test in `.github/workflows/devsecops.yml`]
