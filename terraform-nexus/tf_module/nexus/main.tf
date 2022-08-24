resource "nexus_blobstore_file" "file" {
  name = var.file_name
  path = var.file_path

  soft_quota {
    limit = 1024000000
    type  = "spaceRemainingQuota"
  }
}

resource "nexus_repository_raw_hosted" "internal" {
  name   = var.repository_name
  online = true

  storage {
    blob_store_name                = nexus_blobstore_file.file.name
    strict_content_type_validation = false
    write_policy                   = "ALLOW"
  }

  depends_on = [
    nexus_blobstore_file.file
  ]
}
