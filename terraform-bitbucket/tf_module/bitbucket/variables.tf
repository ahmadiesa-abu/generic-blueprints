variable "bitbucket_username" {
    type = string
}

variable "bitbucket_password" {
    type = string
}

variable "bitbucket_workspace" {
    type = string
}

variable "bitbucket_project" {
    type = string
}

variable "bitbucket_project_key" {
    type = string
}

variable "is_private_project" {
    type = bool
    default = true
}

variable "bitbucket_repository" {
    type = string
}

variable "is_private_repository" {
    type = bool
    default = true
}
