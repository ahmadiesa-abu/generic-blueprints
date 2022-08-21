variable "bitbucket_server" {
    type = string
}

variable "bitbucket_username" {
    type = string
}

variable "bitbucket_password" {
    type = string
}

variable "bitbucket_project_key" {
    type = string
}

variable "bitbucket_repository" {
    type = string
}

variable "is_public_repository" {
    type = bool
    default = false
}

variable "bitbucket_repository_to_fork" {
    type = string
}
