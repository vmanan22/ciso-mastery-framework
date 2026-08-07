variable "aws_region" {
  type        = string
  default     = "us-east-1"
  description = "Target AWS Region for deployment"
}

variable "environment" {
  type        = string
  default     = "dev"
  description = "Target Deployment Environment (dev, staging, prod)"
}

variable "account_id_suffix" {
  type        = string
  default     = "987654"
  description = "Account ID suffix for bucket uniqueness"
}
