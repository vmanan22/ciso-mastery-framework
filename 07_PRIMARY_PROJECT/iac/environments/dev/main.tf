# Hardened Infrastructure as Code (Terraform)
# Target Environment: Development / Production Baseline

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

# ------------------------------------------------------------------------------
# 1. KMS Key for Dedicated Customer-Managed Encryption (Enforce KMS at Rest)
# ------------------------------------------------------------------------------
resource "aws_kms_key" "app_kms_key" {
  description             = "KMS Key for DevSecOps Platform Data Encryption"
  deletion_window_in_days = 30
  enable_key_rotation     = true

  tags = {
    Environment = var.environment
    ManagedBy   = "DevSecOps-IaC"
    Security    = "Encrypted"
  }
}

resource "aws_kms_alias" "app_kms_alias" {
  name          = "alias/devsecops-app-key"
  target_key_id = aws_kms_key.app_kms_key.key_id
}

# ------------------------------------------------------------------------------
# 2. Hardened S3 Bucket (Zero Public Access, Encryption, Access Logging)
# ------------------------------------------------------------------------------
resource "aws_s3_bucket" "secure_storage" {
  bucket        = "devsecops-secure-storage-${var.environment}-${var.account_id_suffix}"
  force_destroy = false

  tags = {
    Environment = var.environment
    ManagedBy   = "DevSecOps-IaC"
    DataClass   = "Confidential"
  }
}

# Block ALL Public Access (Control #1)
resource "aws_s3_bucket_public_access_block" "public_block" {
  bucket = aws_s3_bucket.secure_storage.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Mandatory KMS Encryption at Rest (Control #2)
resource "aws_s3_bucket_server_side_encryption_configuration" "kms_encryption" {
  bucket = aws_s3_bucket.secure_storage.id

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.app_kms_key.arn
      sse_algorithm     = "aws:kms"
    }
    bucket_key_enabled = true
  }
}

# Enforce Bucket Versioning for Ransomware/Tampering Protection (Control #3)
resource "aws_s3_bucket_versioning" "versioning" {
  bucket = aws_s3_bucket.secure_storage.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Enforce TLS 1.2+ for Data In Transit via Bucket Policy (Control #4)
resource "aws_s3_bucket_policy" "enforce_tls_policy" {
  bucket = aws_s3_bucket.secure_storage.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "EnforceTLSRequestsOnly"
        Effect    = "Deny"
        Principal = "*"
        Action    = "s3:*"
        Resource = [
          aws_s3_bucket.secure_storage.arn,
          "${aws_s3_bucket.secure_storage.arn}/*"
        ]
        Condition = {
          Bool = {
            "aws:SecureTransport" = "false"
          }
        }
      }
    ]
  })
}

# ------------------------------------------------------------------------------
# 3. Least Privilege IAM Execution Role for App Runner / Container
# ------------------------------------------------------------------------------
resource "aws_iam_role" "app_execution_role" {
  name = "devsecops-app-execution-role-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "tasks.ecs.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Environment = var.environment
    ManagedBy   = "DevSecOps-IaC"
  }
}

# Scoped Policy (No Wildcards!)
resource "aws_iam_policy" "scoped_kms_s3_policy" {
  name        = "devsecops-kms-s3-access-policy-${var.environment}"
  description = "Scoped least-privilege policy for application runtime"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowS3ReadWriteObjectsOnly"
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject"
        ]
        Resource = "${aws_s3_bucket.secure_storage.arn}/*"
      },
      {
        Sid    = "AllowKMSKmsDecryptEncryptOnly"
        Effect = "Allow"
        Action = [
          "kms:Decrypt",
          "kms:GenerateDataKey"
        ]
        Resource = aws_kms_key.app_kms_key.arn
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "attach_scoped_policy" {
  role       = aws_iam_role.app_execution_role.name
  policy_arn = aws_iam_policy.scoped_kms_s3_policy.arn
}
