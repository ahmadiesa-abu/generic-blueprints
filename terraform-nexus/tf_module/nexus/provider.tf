provider "nexus" {
  insecure = true
  password = var.nexus_password
  url      = var.nexus_server
  username = var.nexus_username
}
