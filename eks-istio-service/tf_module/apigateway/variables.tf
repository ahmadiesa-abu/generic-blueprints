# Input variable definitions

variable "aws_region" {
  description = "AWS region for all resources."
  type    = string
  default = "us-east-1"
}

variable "api_gw_name" {
  description = "name of api_gateway"
  type = string
  default = "test_apigw"
}


variable "url_endpoint" {
  description = "url endpoint to redirect to"
  type = string
}
