output "kms_key_arn" {
  value       = aws_kms_key.app_kms_key.arn
  description = "ARN of the dedicated KMS Key"
}

output "secure_storage_bucket_id" {
  value       = aws_s3_bucket.secure_storage.id
  description = "Name of the secure S3 storage bucket"
}

output "execution_role_arn" {
  value       = aws_iam_role.app_execution_role.arn
  description = "ARN of the application least-privilege IAM execution role"
}
