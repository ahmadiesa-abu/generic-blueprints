resource "bitbucketserver_repository" "repo" {
  project     = var.bitbucket_project_key
  name        = var.bitbucket_repository
  public      = var.is_public_repository
  fork_repository_project = var.bitbucket_project_key
  fork_repository_slug = var.bitbucket_repository_to_fork
}
