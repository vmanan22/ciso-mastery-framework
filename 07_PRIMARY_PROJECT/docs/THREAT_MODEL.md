# Threat Model & Vulnerability Analysis — DevSecOps Pipeline & Cloud Target

> **Framework**: STRIDE & OWASP Top 10 CI/CD Security Risks  
> **Author**: Staff Security Engineer / Technical CISO  
> **Scope**: Source Code Repository, CI/CD Pipeline Runners, Artifact Registry, Cloud Target Environment.

---

## 1. OWASP Top 10 CI/CD Security Risks Mapping

| Rank | OWASP CI/CD Risk | Description | Specific Threat in Our Platform | Mitigation Strategy |
|------|------------------|-------------|---------------------------------|---------------------|
| **CICD-SEC-1** | Insufficient Flow Control Mechanisms | Malicious PR merged without security review | Unauthorized code deployed to production | Branch protection rules, required approval workflows, automated status checks |
| **CICD-SEC-2** | Inadequate Identity & Access Management | Pipeline runners over-privileged in cloud | Stolen runner token used to wipe cloud resources | Ephemeral OIDC authentication with tight IAM role scoping |
| **CICD-SEC-3** | Dependency Chain Abuse | Typosquatting or malicious upstream dependency | Supply chain compromise via `npm`/`pip`/`go` packages | Lockfiles, SCA dependency vulnerability scanning, SBOM tracking |
| **CICD-SEC-4** | Poisoned Pipeline Execution (PPE) | Attacker modifies `.github/workflows/` in unreviewed PR | Execution of arbitrary code/miner on runner | Restrict workflow modification permissions, isolate PR workflow contexts (`pull_request` vs `pull_request_target`) |
| **CICD-SEC-5** | Insufficient Pipeline Security Controls | Missing scanning tools or ignored build failures | Critical CVE or misconfiguration shipped to prod | Non-bypassable mandatory CI quality gates (`exit 1` on policy failure) |
| **CICD-SEC-6** | Insufficient Credential Hygiene | Hardcoded cloud keys in repository or logs | Exposure of AWS secret keys or database credentials | Automated Gitleaks scanning + OIDC identity federation |
| **CICD-SEC-7** | Insecure System Configuration | Misconfigured container registry or runner host | Container image tampering in registry | Private registry with immutable tags and mandatory Cosign signature verification |
| **CICD-SEC-8** | Ungoverned Third-Party Services | Unverified GitHub Actions plugins used in pipeline | Malicious third-party Action exfiltrating secrets | Pin Actions to full 40-character commit hashes (SHA-1), pin action provenance |
| **CICD-SEC-9** | Improper Artifact Integrity Validation | Unsigned container images deployed to K8s/Cloud | Rogue container deployed into infrastructure | Keyless Cosign signing + Admission Controller / Deployment gate check |
| **CICD-SEC-10** | Insufficient Logging & Visibility | Lack of audit logs for build & deployment events | Inability to perform post-incident forensics | Centralized immutable workflow logs and CloudTrail/Cloud Audit logs |

---

## 2. STRIDE Threat Model Analysis

### A. Spoofing (Identity Faking)
- **Threat**: Attacker spoofs CI runner identity or container registry credentials.
- **Attack Vector**: Compromising static service account keys stored in GitHub Secrets.
- **Mitigation**: Ephemeral OpenID Connect (OIDC) identity exchange. Tokens expire in 15 minutes and are bound strictly to the specific GitHub Repository and Branch ref.

### B. Tampering (Unauthorized Data Alteration)
- **Threat**: Attacker tampers with container binary after security scan passes but before deployment (Time-of-Check to Time-of-Use / TOCTOU attack).
- **Attack Vector**: Pushing a malicious container image with an identical tag (e.g. `app:latest`) to the container registry.
- **Mitigation**: 
  1. Use immutable image digests (`@sha256:abcd...`) instead of mutable tags.
  2. Cryptographically sign the exact container digest using Cosign immediately post-build.

### C. Repudiation (Denying Actions)
- **Threat**: Developer or pipeline operator denies approving or deploying a compromised release.
- **Attack Vector**: Shared deployment credentials with no user/session binding.
- **Mitigation**: Immutable git commit logs, signed commits (GPG/Sigstore), and signed build attestations (SLSA provenance).

### D. Information Disclosure (Secret Leaks)
- **Threat**: API keys, database passwords, or private keys printed to public CI/CD build logs.
- **Attack Vector**: Verbose debugging in build scripts or unhandled error stack traces.
- **Mitigation**: Masking secrets in GitHub Action runners + automated Gitleaks secret detection step running before any code execution.

### E. Denial of Service (Resource Exhaustion)
- **Threat**: Malicious PR triggers hundreds of concurrent heavy pipeline jobs, consuming CI runner quota and blocking urgent security hotfixes.
- **Attack Vector**: Submitting automated PR loops.
- **Mitigation**: Concurrency limits on workflow runs, job timeout restrictions, and workflow execution approval requirements for first-time contributors.

### F. Elevation of Privilege (Gaining Unauthorized Access)
- **Threat**: Container escape or arbitrary command execution on the runner host escaping into cloud infrastructure.
- **Attack Vector**: Running root containers with excessive Linux capabilities (`CAP_SYS_ADMIN`).
- **Mitigation**: Non-root container execution (`USER 65532:65532`), read-only root filesystems, dropping all Linux capabilities (`cap_drop: ["ALL"]`).

---

## 3. High-Risk Vector Deep Dive: Poisoned Pipeline Execution (PPE)

```
[Attacker] ──(Forks Repo)──> [Modifies .github/workflows/deploy.yml] ──(Opens PR)──> [Triggers Runner]
                                                                                            │
                                                                                            ▼
                                                                                   [Exfiltrates SECRETS 
                                                                                    to Remote C2 Server]
```

### Defense in Depth against PPE:
1. **Never use `pull_request_target`** for untrusted code execution.
2. **Require Approval** for all workflow runs originating from fork PRs.
3. **Isolate Secrets**: Workflow jobs running on PR contexts (`pull_request`) must not have access to production deployment tokens or cloud credentials. Secrets are only injected on trusted `main` branch merges.
