# ------------------------------------------------------------------------------
# Production Terraform Configuration — Hardened Cloud Infrastructure
# Provisioning: Secure S3 Bucket, KMS Encryption Key & Public Access Controls
# ------------------------------------------------------------------------------

terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  type        = string
  default     = "us-east-1"
  description = "Target AWS Region for ephemeral sandbox deployment"
}

variable "environment" {
  type        = string
  default     = "dev"
  description = "Environment identifier"
}

# 1. KMS Customer Managed Key for Encryption-at-Rest
resource "aws_kms_key" "app_storage_key" {
  description             = "KMS Key for SSDLC Application Encrypted Storage"
  deletion_window_in_days = 7
  enable_key_rotation     = true

  tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
    Security    = "KMS-AES-256"
  }
}

# 2. Hardened Encrypted S3 Storage Bucket
resource "aws_s3_bucket" "app_data_storage" {
  bucket        = "ssdlc-secure-app-data-${var.environment}"
  force_destroy = true

  tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
    Security    = "Encrypted-Private"
  }
}

# 3. Server-Side Encryption Configuration (KMS)
resource "aws_s3_bucket_server_side_encryption_configuration" "s3_encryption" {
  bucket = aws_s3_bucket.app_data_storage.id

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.app_storage_key.arn
      sse_algorithm     = "aws:kms"
    }
  }
}

# 4. Mandatory S3 Public Access Block (Enforcing Private Access)
resource "aws_s3_bucket_public_access_block" "public_block" {
  bucket = aws_s3_bucket.app_data_storage.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# 5. S3 Versioning Configuration for Anti-Tampering & Recovery
resource "aws_s3_bucket_versioning" "versioning" {
  bucket = aws_s3_bucket.app_data_storage.id
  versioning_configuration {
    status = "Enabled"
  }
}
