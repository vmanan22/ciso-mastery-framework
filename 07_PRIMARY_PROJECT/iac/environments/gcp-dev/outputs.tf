# ==============================================================================
# Outputs — Values printed after terraform apply
#
# LEARNING: Outputs serve two purposes:
# 1. Human-readable confirmation of what was deployed
# 2. Machine-readable values for downstream systems (other Terraform modules,
#    GitHub Actions steps, scripts that need the bucket name, etc.)
#
# In GitHub Actions, outputs can be captured with:
#   BUCKET=$(terraform output -raw bucket_name)
# ==============================================================================

output "bucket_name" {
  description = "Name of the deployed GCS artifact storage bucket"
  value       = google_storage_bucket.ssdlc_artifacts.name
}

output "bucket_url" {
  description = "gs:// URL of the deployed bucket (use with gsutil)"
  value       = google_storage_bucket.ssdlc_artifacts.url
}

output "bucket_self_link" {
  description = "Full REST API self-link for the bucket"
  value       = google_storage_bucket.ssdlc_artifacts.self_link
}

output "kms_key_id" {
  description = "Full resource ID of the CMEK key used to encrypt the bucket"
  value       = google_kms_crypto_key.ssdlc_storage_key.id
}

output "kms_key_ring" {
  description = "Full resource ID of the KMS key ring"
  value       = google_kms_key_ring.ssdlc_key_ring.id
}

output "deployment_summary" {
  description = "Human-readable summary of deployed resources"
  value       = <<-EOT
    ============================================================
    SSDLC Platform — GCP Dev Deployment Summary
    ============================================================
    Project:      ${var.project_id}
    Region:       ${var.region}
    Environment:  ${var.environment}
    ------------------------------------------------------------
    GCS Bucket:   ${google_storage_bucket.ssdlc_artifacts.name}
    Bucket URL:   ${google_storage_bucket.ssdlc_artifacts.url}
    KMS Key:      ${google_kms_crypto_key.ssdlc_storage_key.id}
    ------------------------------------------------------------
    Security Controls:
      ✅ CMEK encryption enforced (KMS AES-256)
      ✅ Public access prevention: ENFORCED
      ✅ Uniform bucket-level access: ENABLED
      ✅ Versioning: ENABLED
      ✅ 30-day lifecycle rule: ACTIVE
      ✅ IAM: Least-privilege pipeline writer only
    ============================================================
  EOT
}
