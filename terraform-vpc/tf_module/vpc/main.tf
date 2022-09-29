provider "aws" {
  region = local.region
}

locals {
  region = var.aws_region
}

################################################################################
# VPC Module
################################################################################

module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = var.vpc_name
  cidr = "10.0.0.0/16"
  create_database_subnet_group = false
  create_egress_only_igw = false
  create_elasticache_subnet_group = false
  create_igw = false
  create_redshift_subnet_group = false

  vpc_tags = {
    Name = var.vpc_name
  }
}
