# ==============================================================================
# Input Variables — GCP Dev Environment
#
# LEARNING: Variables make Terraform config reusable and environment-agnostic.
# The same main.tf can deploy to dev, staging, or prod by changing these values.
# Never hardcode project IDs, regions, or account emails directly in main.tf.
# ==============================================================================

variable "project_id" {
  type        = string
  description = "GCP Project ID where resources will be deployed."
  # No default — this MUST be supplied. Terraform will error if missing.
  # Supply via: terraform apply -var="project_id=ssdlc-platform-dev"
  # Or via: TF_VAR_project_id environment variable (used in GitHub Actions)
}

variable "region" {
  type        = string
  default     = "us-central1"
  description = "GCP region for all resources."
  # WHY us-central1?
  # It is in the GCP Always Free Tier eligible regions.
  # Cloud Storage in us-central1 gets 5GB free per month.
  # Avoid multi-region or dual-region buckets for this lab — they cost more.
}

variable "environment" {
  type        = string
  default     = "dev"
  description = "Environment label (dev, staging, prod). Used in resource names and labels."
  # SECURITY PRINCIPLE: Never deploy this lab config to production.
  # Production needs separate Terraform workspaces, remote state, and
  # stricter lifecycle rules (force_destroy = false, prevent_destroy = true).
}

variable "pipeline_service_account" {
  type        = string
  description = "Email of the GCP service account used by GitHub Actions CI/CD pipeline."
  # Format: ssdlc-pipeline@<project_id>.iam.gserviceaccount.com
  # This is created during Workload Identity Federation setup (Step 0).
  # Passed in from GitHub Actions as TF_VAR_pipeline_service_account.
}
