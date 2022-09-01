variable "region" {
  type        = string
  description = "Name of the AWS region to deploy EKS into"
  default     = "us-east-1"
}

variable "bucket_name" {
  type        = string
  description = "Bucket Name"
}
