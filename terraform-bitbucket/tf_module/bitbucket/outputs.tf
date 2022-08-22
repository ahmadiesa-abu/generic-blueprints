output "repo_url" {
    description = "Bitbucket Repository ID"
    value       = join("", ["https://", var.bitbucket_username, "@bitbucket.org/", var.bitbucket_workspace, "/", var.bitbucket_repository, ".git"])
}
