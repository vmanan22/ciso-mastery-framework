# ==============================================================================
# OPA / Rego Policy: GCP Cloud Storage Security
# Engine: Open Policy Agent evaluated via Conftest in GitHub Actions
#
# HOW THIS WORKS:
# 1. GitHub Actions runs `terraform plan -out=tfplan`
# 2. Then: `terraform show -json tfplan > plan.json`
# 3. Then: `conftest test plan.json --policy policies/iac_policies/`
# 4. If any `deny` rule fires → conftest exits non-zero → pipeline FAILS
#
# LEARNING: Rego is a declarative language.
# You describe WHAT is forbidden — not HOW to check it.
# OPA figures out the "how" by evaluating rules against the JSON input.
# ==============================================================================

package main

import future.keywords.in

# ==============================================================================
# RULE 1: Block public access if public_access_prevention is not "enforced"
#
# WHY: "inherited" means the bucket inherits the org policy (if it exists).
# In a new GCP project without org policies, "inherited" = effectively public.
# Only "enforced" provides an absolute guarantee at the bucket level.
#
# THREAT MODEL MAPPING: Threat I3 — GCS bucket publicly exposing scan results
# ==============================================================================
deny[msg] {
  some resource in input.planned_values.root_module.resources
  resource.type == "google_storage_bucket"

  # Check that public_access_prevention is NOT "enforced"
  resource.values.public_access_prevention != "enforced"

  msg := sprintf(
    "POLICY VIOLATION [GCS-01] Bucket '%s': public_access_prevention must be 'enforced', got '%s'. Threat I3: Public bucket exposes SBOM and scan artifacts.",
    [resource.name, resource.values.public_access_prevention]
  )
}

# ==============================================================================
# RULE 2: Block bucket creation without CMEK encryption
#
# WHY: Default GCS encryption uses Google-managed keys.
# Compliance frameworks (SOC2, ISO 27001, PCI-DSS) often require customer-owned
# key management. Without CMEK, you cannot demonstrate key custodianship.
#
# THREAT MODEL MAPPING: Threat I3 / T5 — Unencrypted artifact exposure
# ==============================================================================
deny[msg] {
  some resource in input.planned_values.root_module.resources
  resource.type == "google_storage_bucket"

  # encryption block must exist
  not resource.values.encryption

  msg := sprintf(
    "POLICY VIOLATION [GCS-02] Bucket '%s': Missing CMEK encryption. All buckets must use a Customer Managed Encryption Key (KMS). Default Google-managed keys are prohibited.",
    [resource.name]
  )
}

deny[msg] {
  some resource in input.planned_values.root_module.resources
  resource.type == "google_storage_bucket"

  count(resource.values.encryption) == 0

  msg := sprintf(
    "POLICY VIOLATION [GCS-02] Bucket '%s': Missing CMEK encryption block. All buckets must use a Customer Managed Encryption Key (KMS).",
    [resource.name]
  )
}


# ==============================================================================
# RULE 3: Require uniform bucket-level access (disable legacy ACLs)
#
# WHY: ACLs can make individual objects public even if the bucket is private.
# This is the #1 cause of accidental GCS data exposure.
# Uniform access forces all access control through IAM only.
#
# THREAT MODEL MAPPING: Threat I3 — Misconfigured access control
# ==============================================================================
deny[msg] {
  some resource in input.planned_values.root_module.resources
  resource.type == "google_storage_bucket"

  # uniform_bucket_level_access must be true
  resource.values.uniform_bucket_level_access != true

  msg := sprintf(
    "POLICY VIOLATION [GCS-03] Bucket '%s': uniform_bucket_level_access must be true. Legacy ACLs are disabled in this organization — all access must be managed via IAM.",
    [resource.name]
  )
}

# ==============================================================================
# RULE 4: Require versioning on all buckets
#
# WHY: Without versioning, an attacker with write access can overwrite files
# and the original is permanently lost. Versioning creates an immutable audit trail.
#
# THREAT MODEL MAPPING: Threat T5 — Attacker overwrites GCS bucket content
# ==============================================================================
deny[msg] {
  some resource in input.planned_values.root_module.resources
  resource.type == "google_storage_bucket"

  # versioning block must exist and be enabled
  not resource.values.versioning[0].enabled

  msg := sprintf(
    "POLICY VIOLATION [GCS-04] Bucket '%s': Versioning must be enabled. Without versioning, file overwrites are irreversible and audit trails cannot be maintained.",
    [resource.name]
  )
}

# ==============================================================================
# RULE 5: Block KMS keys with rotation period > 90 days
#
# WHY: NIST SP 800-57 recommends annual key rotation at minimum.
# We enforce quarterly (90 days) rotation to limit the blast radius
# of a compromised key. If a key leaks, it's valid for at most 90 days.
#
# 7776000 seconds = 90 days
# THREAT MODEL MAPPING: Threat D2 — KMS key compromise
# ==============================================================================
deny[msg] {
  some resource in input.planned_values.root_module.resources
  resource.type == "google_kms_crypto_key"

  # rotation_period comes as a string like "7776000s" — extract the number
  rotation_str := resource.values.rotation_period
  rotation_seconds := to_number(trim_suffix(rotation_str, "s"))
  rotation_seconds > 7776000

  msg := sprintf(
    "POLICY VIOLATION [KMS-01] KMS Key '%s': rotation_period is %vs (%.0f days). Maximum allowed is 7776000s (90 days). Reduce rotation_period to comply.",
    [resource.name, rotation_seconds, rotation_seconds / 86400]
  )
}
