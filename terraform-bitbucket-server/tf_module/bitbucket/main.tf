resource "bitbucketserver_project" "project" {
  name       = var.bitbucket_project
  key        = var.bitbucket_project_key
  public     = var.is_public_project
}


resource "bitbucketserver_repository" "repo" {
  project     = bitbucketserver_project.project.key
  name        = var.bitbucket_repository
  public      = var.is_public_repository

  depends_on = [
    bitbucketserver_project.project
  ]
}
