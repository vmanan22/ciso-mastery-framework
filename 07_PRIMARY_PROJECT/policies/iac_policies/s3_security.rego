package main

# ------------------------------------------------------------------------------
# Policy-as-Code: S3 Infrastructure Security Rules
# Engine: Open Policy Agent (OPA) / Conftest
# ------------------------------------------------------------------------------

default allow = false

# Rule 1: Deny S3 Buckets without Public Access Block configuration
deny[msg] {
    resource := input.resource.aws_s3_bucket_public_access_block[name]
    not resource.block_public_acls == true
    msg := sprintf("SECURITY VIOLATION [Policy-S3-01]: S3 Public Access Block '%v' must set block_public_acls = true", [name])
}

deny[msg] {
    resource := input.resource.aws_s3_bucket_public_access_block[name]
    not resource.block_public_policy == true
    msg := sprintf("SECURITY VIOLATION [Policy-S3-02]: S3 Public Access Block '%v' must set block_public_policy = true", [name])
}

# Rule 2: Require Encryption Configuration for S3 Buckets
deny[msg] {
    bucket_name := input.resource.aws_s3_bucket[name]
    encryption_rules := [e | e := input.resource.aws_s3_bucket_server_side_encryption_configuration[_]; e.bucket == sprintf("${aws_s3_bucket.%v.id}", [name])]
    count(encryption_rules) == 0
    msg := sprintf("SECURITY VIOLATION [Policy-S3-03]: S3 Bucket '%v' lacks explicit Server-Side Encryption Configuration", [name])
}
