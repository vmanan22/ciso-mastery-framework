# ✅ FIXED TEST FILE FOR HANDS-ON SECURITY SCANNING LAB

# Fix 1: Secrets are NOT hardcoded. Injected securely at runtime via AWS Secrets Manager / KMS
locals {
  # Secrets managed out-of-band via Secret Store
}

# Fix 2: S3 Bucket is Private (No public-read ACL)
resource "aws_s3_bucket" "secure_private_bucket" {
  bucket = "my-company-confidential-customer-data"
}

# Enforce Public Access Block
resource "aws_s3_bucket_public_access_block" "private_block" {
  bucket = aws_s3_bucket.secure_private_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
