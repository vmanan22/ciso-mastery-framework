# ==============================================================================
# OPA / Rego Policy: GCP IAM Security
# Engine: Open Policy Agent evaluated via Conftest in GitHub Actions
#
# LEARNING: IAM misconfigurations are the #1 cause of GCP security incidents.
# These rules prevent privilege escalation and over-permissioned bindings
# from ever reaching production.
# ==============================================================================

package main

import future.keywords.in

# ==============================================================================
# RULE 1: Block IAM bindings to allUsers or allAuthenticatedUsers
#
# WHY: `allUsers` = literally anyone on the internet.
# `allAuthenticatedUsers` = anyone with a Google account (billions of people).
# These are almost never intentional for internal SSDLC platform resources.
# This is the #1 GCP misconfiguration in bug bounty reports.
#
# THREAT MODEL MAPPING: Threat I3 — Unauthorized access to scan results
# ==============================================================================
deny[msg] {
  some resource in input.planned_values.root_module.resources
  resource.type == "google_storage_bucket_iam_member"

  member := resource.values.member
  member in {"allUsers", "allAuthenticatedUsers"}

  msg := sprintf(
    "POLICY VIOLATION [IAM-01] IAM binding '%s': member '%s' grants PUBLIC access. allUsers and allAuthenticatedUsers are prohibited on this platform.",
    [resource.name, member]
  )
}

# Also check google_project_iam_member (project-level bindings)
deny[msg] {
  some resource in input.planned_values.root_module.resources
  resource.type == "google_project_iam_member"

  member := resource.values.member
  member in {"allUsers", "allAuthenticatedUsers"}

  msg := sprintf(
    "POLICY VIOLATION [IAM-02] Project IAM binding '%s': member '%s' grants PUBLIC project access. This is a critical misconfiguration.",
    [resource.name, member]
  )
}

# ==============================================================================
# RULE 2: Block primitive roles (Owner, Editor, Viewer) at project level
#
# WHY: Primitive roles predate IAM and grant extremely broad permissions.
# - roles/owner: Can do ANYTHING in the project including deleting it
# - roles/editor: Can read and modify almost all resources
# - roles/viewer: Can read ALL resources (violates least privilege)
#
# Best practice: Use predefined roles (roles/storage.objectCreator) or
# custom roles — never primitive roles.
#
# THREAT MODEL MAPPING: Threat E3 — Privilege escalation via Terraform IAM
# ==============================================================================
deny[msg] {
  some resource in input.planned_values.root_module.resources
  resource.type == "google_project_iam_member"

  primitive_roles := {"roles/owner", "roles/editor", "roles/viewer"}
  resource.values.role in primitive_roles

  msg := sprintf(
    "POLICY VIOLATION [IAM-03] Project IAM binding '%s': role '%s' is a primitive role. Use predefined or custom roles instead. Primitive roles violate least-privilege and grant excessive permissions.",
    [resource.name, resource.values.role]
  )
}

# ==============================================================================
# RULE 3: Block service account key creation
#
# WHY: Service account key files are static credentials.
# They do not expire, can be downloaded and stored anywhere, and if leaked
# provide permanent access until manually revoked.
# We use Workload Identity Federation (OIDC) instead — short-lived tokens only.
#
# THREAT MODEL MAPPING: Threat I4 — Static SA key leaked in CI logs
# ==============================================================================
deny[msg] {
  some resource in input.planned_values.root_module.resources
  resource.type == "google_service_account_key"

  msg := sprintf(
    "POLICY VIOLATION [IAM-04] Service Account Key '%s': Creating service account keys is prohibited. Use Workload Identity Federation with OIDC for keyless authentication. Static keys violate our Zero-Trust secret architecture.",
    [resource.name]
  )
}
