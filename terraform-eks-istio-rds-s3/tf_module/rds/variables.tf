variable "region" {
  type        = string
  description = "Name of the AWS region to deploy EKS into"
  default     = "us-east-1"
}

variable "subnet_ids" {
  type        = list(string)
  description = "Subnet IDs to deploy RDS nodes into"
}

variable "db_engine" {
  type        = string
  description = "DB Engine"
}

variable "db_engine_version" {
  type        = string
  description = "DB Engine Version"
}

variable "instance_type" {
  type        = string
  description = "Managed node group instance size to use"
  default     = "t3.medium"
}

variable "db_name" {
  type        = string
  description = "DB Name"
}

variable "db_identifier" {
  type        = string
  description = "DB Identifier"
}

variable "db_username" {
  type        = string
  description = "DB Username"
}

variable "db_password" {
  type        = string
  description = "DB Password"
}

variable "security_group_id" {
  type        = string
  description = "Security Group ID"
}

variable "database_subnet_group_name" {
  type        = string
  description = "Database subnet group name"
}
