terraform {
  required_version = ">= 0.13"

  required_providers {
    bitbucketserver = {
      source  = "gavinbunney/bitbucketserver"
    }
  }
}