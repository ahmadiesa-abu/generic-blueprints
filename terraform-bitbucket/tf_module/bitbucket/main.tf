resource "bitbucket_project" "project" {
  workspace  = var.bitbucket_workspace
  name       = var.bitbucket_project
  key        = var.bitbucket_project_key
  is_private = var.is_private_project
}


resource "bitbucket_repository" "repo" {
  workspace   = var.bitbucket_workspace
  name        = var.bitbucket_repository
  project_key = bitbucket_project.project.key
  is_private  = var.is_private_repository
  fork_policy = "allow_forks"
  enable_pipelines = true

  depends_on = [
    bitbucket_project.project
  ]
}
