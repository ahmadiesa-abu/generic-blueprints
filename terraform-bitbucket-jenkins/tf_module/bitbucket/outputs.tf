output "repo_url" {
    description = "Bitbucket Repository URL"
    value       = bitbucketserver_repository.repo.clone_https
}
