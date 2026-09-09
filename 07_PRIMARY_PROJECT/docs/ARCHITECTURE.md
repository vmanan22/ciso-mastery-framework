# DevSecOps & Cloud Security Platform — End-to-End System Architecture

> **Role**: Security Architect & Principal DevSecOps Engineer  
> **Document Purpose**: Technical architecture specification for automated shift-left security enforcement and hardened cloud deployment pipeline.

---

## 1. System Overview & Objectives

Modern engineering organizations deploy code tens or hundreds of times per day. Traditional "security gatekeeper" models (manual security reviews before release) create severe friction and bottleneck delivery velocity.

The objective of this platform is to build **Continuous Security Verification & Enforcement**:
- **Shift-Left**: Detect misconfigurations, vulnerabilities, and secrets in developer workflows (IDE, git pre-commit, pull requests).
- **Policy-as-Code**: Enforce deterministic security guardrails codified as code (Rego/OPA) rather than tribal knowledge or manual wikis.
- **Supply Chain Cryptographic Integrity**: Cryptographically verify build artifacts (containers, IaC, binaries) using SBOMs and digital signatures before cloud deployment.
- **Zero-Trust Cloud Runtime**: Deploy infrastructure defined via IaC adhering to least privilege, encryption at rest/transit, and isolated network perimeters.

---

## 2. High-Level End-to-End Architecture

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                       DEVELOPER ECOSYSTEM                                         │
│                                                                                                   │
│   ┌──────────────────┐            ┌──────────────────┐           ┌───────────────────────────┐    │
│   │ Developer Laptop │ ─────────> │ Git Pre-Commit   │ ────────> │ Pull Request (GitHub/Git) │    │
│   │ (IDE / Local)    │            │ (Secret / Lint)  │           │ (Code Review + Checks)    │    │
│   └──────────────────┘            └──────────────────┘           └─────────────┬─────────────┘    │
└────────────────────────────────────────────────────────────────────────────────┼──────────────────┘
                                                                                 │
                                                                                 ▼
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                     DEVSECOPS CI/CD PIPELINE                                      │
│                                                                                                   │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ Stage 1: Static Analysis & Secret Detection                                              │   │
│   │  ├── Gitleaks (Secret scanning)                                                           │   │
│   │  └── Semgrep / Bandit (SAST code analysis)                                                │   │
│   └─────────────────────────────┬─────────────────────────────────────────────────────────────┘   │
│                                 │                                                                 │
│                                 ▼                                                                 │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ Stage 2: Infrastructure-as-Code & Policy Verification                                     │   │
│   │  ├── Checkov / Trivy (Terraform static security scan)                                     │   │
│   │  └── OPA / Rego (Organizational security policy compliance check)                         │   │
│   └─────────────────────────────┬─────────────────────────────────────────────────────────────┘   │
│                                 │                                                                 │
│                                 ▼                                                                 │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ Stage 3: Container Hardening, SBOM & Cryptographic Attestation                            │   │
│   │  ├── Multi-stage Hardened Minimal Container Build                                         │   │
│   │  ├── Trivy / Grype (Container image CVE vulnerability scan)                               │   │
│   │  ├── Syft (Generate Software Bill of Materials - SBOM)                                    │   │
│   │  └── Cosign (Cryptographic signing of container digest via Keyless OIDC)                  │   │
│   └─────────────────────────────┬─────────────────────────────────────────────────────────────┘   │
│                                 │                                                                 │
│                                 ▼                                                                 │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ Stage 4: OIDC Workload Identity & Cloud Deployment Gate                                   │   │
│   │  ├── Short-lived GCP/AWS IAM token exchange via GitHub OIDC (No static cloud keys!)       │   │
│   │  └── Terraform / Helm Apply (Deployment to hardened Cloud Target)                         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Core Architectural Subsystems

### Subsystem A: Policy-as-Code Enforcement Engine
- **Engine**: Open Policy Agent (OPA) / Rego & Checkov.
- **Responsibility**: Evaluate IaC plans (Terraform JSON output) and Kubernetes manifests against security rules before execution.
- **Fail-Safe Mechanism**: Any `HIGH` or `CRITICAL` policy violation immediately fails the pipeline build step and posts an inline PR annotation.

### Subsystem B: Supply Chain Attestation & Container Provenance
- **Engine**: Cosign (Sigstore) + Syft.
- **Responsibility**: Ensure that only container images built by our authorized CI/CD pipeline (and signed with short-lived OIDC tokens) can be deployed to production.
- **Value**: Prevents "Poisoned Pipeline Execution" and unauthorized container pushing directly to the registry.

### Subsystem C: Identity Federation (Zero-Trust Secret Architecture)
- **Engine**: OpenID Connect (OIDC) Workload Identity Federation.
- **Responsibility**: Eliminate long-lived cloud access keys (`AWS_SECRET_ACCESS_KEY` or GCP service account JSON files) stored in CI secrets.
- **Mechanism**: The CI/CD runner requests an ephemeral ID token from GitHub's OIDC provider, which is exchanged for a 15-minute scoped cloud IAM token.

---

## 4. Alternatives & Trade-off Analysis

| Architecture Decision | Option Selected | Alternative Considered | Trade-off Rationale |
|-----------------------|-----------------|------------------------|---------------------|
| **Secret Scanning Placement** | Shift-Left (Pre-Commit + CI) | CI-Only Scanning | Pre-commit prevents secrets from ever touching git history. CI scanning acts as the non-bypassable safety net. |
| **Cloud Authentication** | OIDC Keyless Federation | Static Service Account Keys | Static keys leak frequently via logs or developer machines. OIDC eliminates static credentials entirely. |
| **Container Base Image** | Minimal Hardened (`python:3.11-slim`) | Standard Ubuntu/Debian Base | Hardened minimal base with stripped build packaging metadata, runtime-only isolation, and nonroot UID 65532, eliminating OS-level CVEs while ensuring predictable offline dependencies. |
| **Policy Engine** | OPA (Rego) Declarative Engine | Custom Shell Script Scanning | Custom scripts break easily, lack standardized AST parsing, and are unmaintainable at scale. OPA provides formal policy language & testing framework. |

---

## 5. Security Controls Mapping

- **NIST SP 800-53 / CSF**:
  - `SI-7 (Software Integrity)`: Covered via Cosign image signing and SBOM generation.
  - `IA-2 (Identification & Authentication)`: Covered via GitHub OIDC short-lived credential exchange.
  - `CM-6 (Configuration Settings)`: Covered via OPA policy scanning of IaC manifests.
  - `SA-11 (Developer Security Testing)`: Covered via SAST, Secret Scanning, and Container Scanning.
