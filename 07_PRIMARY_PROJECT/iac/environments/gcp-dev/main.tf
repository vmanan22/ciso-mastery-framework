# ------------------------------------------------------------------------------
# GCP Terraform Configuration — Hardened Cloud Infrastructure
# Provisioning: Cloud KMS CMEK Key + Hardened Cloud Storage Bucket
#
# LEARNING NOTE: This is the GCP equivalent of the AWS (S3 + KMS) config.
# The security principles are identical — only the provider syntax differs.
#
# Cost estimate: ~$0.06/month (1 KMS key version)
# All other resources are within GCP Always Free Tier
# ------------------------------------------------------------------------------

terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
      # WHY pin to ~> 5.0?
      # Pinning prevents a provider update from silently changing behavior.
      # The ~> operator allows patch updates (5.0.1, 5.0.2) but not major
      # breaking changes (6.0). This is "reproducible infrastructure".
    }
  }

  # LEARNING: Terraform state stores what resources are deployed.
  # For a real production system this would be a remote backend (GCS bucket).
  # We use local state here for the learning lab — do NOT commit .tfstate to git.
  # The .gitignore already excludes *.tfstate and *.tfstate.backup.
}

provider "google" {
  project = var.project_id
  region  = var.region
  # Authentication: In GitHub Actions, no credentials are set here.
  # The OIDC Workload Identity token is read automatically from the environment.
  # On your local machine: `gcloud auth application-default login` handles this.
}

# ==============================================================================
# RESOURCE 1: Cloud KMS Key Ring
#
# WHY a Key Ring?
# GCP requires all KMS keys to live inside a Key Ring.
# A Key Ring is a regional container — it groups keys and defines their location.
# Once created, a Key Ring CANNOT be deleted (GCP design choice for auditability).
# This means even after `terraform destroy`, the key ring name is permanently reserved.
# Use a name that's unique and meaningful: project-environment-purpose.
# ==============================================================================
resource "google_kms_key_ring" "ssdlc_key_ring" {
  name     = "ssdlc-${var.environment}-keyring"
  location = var.region

  # SECURITY NOTE: Key rings are regional. If you need keys in multiple regions
  # (for disaster recovery), create a key ring per region.
}

# ==============================================================================
# RESOURCE 2: Cloud KMS Crypto Key (CMEK)
#
# WHY CMEK over Google-managed encryption?
# All GCS data is encrypted by default — but with Google's keys.
# CMEK means YOU own the encryption key. If you delete this key,
# the data becomes permanently inaccessible — even to Google.
# This satisfies compliance requirements (SOC2, ISO 27001, GDPR, PCI-DSS)
# that require customer control over encryption keys.
#
# COST: $0.06/month per active key version
# ==============================================================================
resource "google_kms_crypto_key" "ssdlc_storage_key" {
  name            = "ssdlc-${var.environment}-storage-key"
  key_ring        = google_kms_key_ring.ssdlc_key_ring.id
  rotation_period = "7776000s" # 90 days = 7,776,000 seconds
  # WHY 90-day rotation?
  # Key rotation limits the blast radius of a compromised key.
  # If a key is leaked but rotated every 90 days, an attacker has at most
  # a 90-day window before their access expires. NIST recommends annual rotation
  # minimum — we exceed that with quarterly.
  # OPA policy BLOCKS deploy if rotation_period > 7776000s (90 days).

  purpose = "ENCRYPT_DECRYPT"

  lifecycle {
    # CRITICAL SAFETY CONTROL:
    # Prevent Terraform from destroying the key (which destroys ALL encrypted data).
    # If you genuinely want to delete: first remove this block, then terraform apply,
    # then terraform destroy. The extra step forces a conscious decision.
    prevent_destroy = false
    # NOTE: Set to true in production. False here for lab cleanup convenience.
  }

  labels = {
    environment = var.environment
    managed-by  = "terraform"
    purpose     = "storage-encryption"
  }
}

# ==============================================================================
# RESOURCE 3: IAM binding — Allow GCS to use the KMS key
#
# WHY do we need this explicit binding?
# Cloud Storage uses a service account (google_storage_project_service_account)
# to perform encryption operations. That service account needs permission to
# call the KMS key for encryption/decryption.
# Without this, bucket creation with CMEK fails with a 403 error.
#
# SECURITY PRINCIPLE: Least Privilege
# We grant ONLY `roles/cloudkms.cryptoKeyEncrypterDecrypter` — not admin, not owner.
# This means the GCS service account can encrypt/decrypt but cannot:
# - Create new keys
# - Delete keys
# - View key metadata
# ==============================================================================
data "google_storage_project_service_account" "gcs_account" {}

resource "google_kms_crypto_key_iam_member" "gcs_kms_binding" {
  crypto_key_id = google_kms_crypto_key.ssdlc_storage_key.id
  role          = "roles/cloudkms.cryptoKeyEncrypterDecrypter"
  member        = "serviceAccount:${data.google_storage_project_service_account.gcs_account.email_address}"
}

# ==============================================================================
# RESOURCE 4: Cloud Storage Bucket
#
# WHY each setting:
# - uniform_bucket_level_access: Disables legacy ACLs. With ACLs enabled,
#   an object can be made public even if the bucket is private — a confusing
#   and dangerous override. Uniform access means IAM is the ONLY control plane.
#
# - public_access_prevention = "enforced": Even if someone runs
#   `gcloud storage buckets add-iam-policy-binding ... --member=allUsers`,
#   GCP will reject it. Belt AND suspenders. This is also enforced by our OPA policy.
#
# - versioning: Every write creates a new version. If an attacker overwrites
#   a file, you can restore the previous version. Without this, overwrite = data loss.
#
# - lifecycle rule (30 days): Without a lifecycle rule, deleted object versions
#   accumulate forever and you pay for all of them. The rule auto-purges versions
#   older than 30 days, keeping costs at zero within the free tier.
# ==============================================================================
resource "google_storage_bucket" "ssdlc_artifacts" {
  name          = "ssdlc-artifacts-${var.project_id}-${var.environment}"
  location      = var.region
  force_destroy = true
  # WHY force_destroy = true in dev?
  # Allows `terraform destroy` to delete the bucket even if it contains files.
  # In production, set this to FALSE — you want Terraform to refuse to destroy
  # a non-empty bucket, forcing you to explicitly empty it first.

  # SECURITY CONTROL 1: Disable legacy ACLs
  uniform_bucket_level_access = true

  # SECURITY CONTROL 2: Block ALL public access at the GCP platform level
  public_access_prevention = "enforced"

  # SECURITY CONTROL 3: Soft-delete / versioning for tamper evidence
  versioning {
    enabled = true
  }

  # COST CONTROL: Auto-delete old versions after 30 days
  lifecycle_rule {
    condition {
      age        = 30
      with_state = "ARCHIVED" # Only applies to non-current (versioned) objects
    }
    action {
      type = "Delete"
    }
  }

  # SECURITY CONTROL 4: CMEK encryption using our KMS key
  encryption {
    default_kms_key_name = google_kms_crypto_key.ssdlc_storage_key.id
  }

  # Ensure KMS IAM binding exists before creating bucket
  depends_on = [google_kms_crypto_key_iam_member.gcs_kms_binding]

  labels = {
    environment = var.environment
    managed-by  = "terraform"
    purpose     = "ssdlc-artifacts"
    security    = "cmek-encrypted"
  }
}

# ==============================================================================
# RESOURCE 5: IAM Binding — Who can write to the bucket?
#
# SECURITY PRINCIPLE: Least Privilege
# The CI/CD pipeline's service account gets ONLY Storage Object Creator.
# This means it can UPLOAD artifacts (SBOM, scan results) but CANNOT:
# - Delete objects
# - List bucket contents
# - Change bucket configuration
# - Read other objects (only the ones it just wrote)
#
# If the pipeline is compromised, blast radius = upload of malicious artifacts
# but NOT deletion, exfiltration of other data, or bucket reconfiguration.
# ==============================================================================
resource "google_storage_bucket_iam_member" "pipeline_writer" {
  bucket = google_storage_bucket.ssdlc_artifacts.name
  role   = "roles/storage.objectCreator"
  member = "serviceAccount:${var.pipeline_service_account}"
  # The pipeline SA email comes from the Workload Identity Federation setup.
  # It is passed in as a variable — not hardcoded — to keep this config reusable.
}
