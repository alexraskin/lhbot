variable "aws_profile" {
  description = "AWS profile to use"
  type        = string
}

variable "aws_region" {
  description = "AWS region to use"
  type        = string
}

variable "app_name" {
  type        = string
  description = "The name of the Heroku app"
}
variable "enviorment_vars" {
  type        = map(string)
  description = "Environment variables for the app"
}

variable "mongodb_cluster_name" {
  type        = string
  description = "Mongodb Atlas cluster name"
}

variable "mongodb_region" {
  type        = string
  description = "Mongodb Atlas region"
}

variable "database_user" {
  type        = string
  description = "Mongodb Atlas database user"
}

variable "database_password" {
  type        = string
  description = "Mongodb Atlas database password"
}

variable "mongodb_project_id" {
  type        = string
  description = "Mongodb Atlas project ID"
}

variable "mongo_database_name" {
  type        = string
  description = "Mongodb Atlas database name"
}

variable "mongodbatlas_private_key" {
  type        = string
  description = "Mongodb Atlas private key"
}

variable "mongodbatlas_public_key" {
  type        = string
  description = "Mongodb Atlas public key"
}

variable "mongo_auth_database_name" {
  type        = string
  description = "Mongodb Atlas auth database name"
}

variable "sentry_token" {
  type        = string
  description = "Sentry token"
}

variable "sentry_team_name" {
  type        = string
  description = "Sentry team name"
}

variable "sentry_project_name" {
  type        = string
  description = "Sentry project name"
}

variable "sentry_slug" {
  type        = string
  description = "Sentry slug"
}

variable "sentry_organization" {
  type        = string
  description = "Sentry organization"
}

variable "lh_bot_s3_bot_config_bucket" {
  type        = string
  description = "S3 bucket for the bot config"
}

variable "lh_bot_s3_terraform_state_bucket" {
  type        = string
  description = "S3 bucket for the terraform state"
}

variable "lh_bot_reports_s3_bucket" {
  type        = string
  description = "S3 bucket for the reports"
}

variable "github_token" {
  type        = string
  description = "Github token"
}

variable "docker_image_tag" {
  type        = string
  description = "Which ECR Image tag to use"
  default     = "latest" # apprunner looks for the lastest tag to deploy off
}

variable "service_port" {
  type    = string
  default = 8000
}

variable "auto_scaling_min_size" {
  type        = number
  default     = 1
  description = "The minimum number of instances to run for the service. Defaults to 1. Minimum value of 1. Maximum value of 25"
}

variable "auto_scaling_max_size" {
  type        = number
  default     = 5
  description = "The maximum number of instances to run for the service. Defaults to 5. Minimum value of 1. Maximum value of 25"
}

variable "auto_deployments" {
  type        = bool
  default     = true
  description = "Whether or not to automatically deploy new code to the service. Defaults to true"
}

variable "service_cpu" {
  type        = number
  description = "The number of cpu's to allocate to the service"
  default     = 1024 # valid values: 1024|2048|(1|2) vCPU
}

variable "service_memory" {
  type        = number
  description = "The amount of memory to allocate to the service"
  default     = 2048 # valid values: 2048|3072|4096|(2|3|4) GB
}

variable "service_healthy_threshold" {
  type        = number
  default     = 5
  description = "The number of consecutive checks that must succeed before App Runner decides that the service is healthy. Defaults to 5. Minimum value of 1. Maximum value of 20."
}

variable "service_interval" {
  type        = number
  default     = 5
  description = "The time interval, in seconds, between health checks. Defaults to 5. Minimum value of 1. Maximum value of 20."
}

variable "service_health_check_path" {
  type        = string
  default     = "/"
  description = " The URL to send requests to for health checks. Defaults to /. Minimum length of 0. Maximum length of 51200."
}

variable "protocol" {
  type        = string
  default     = "TCP"
  description = "The IP protocol that App Runner uses to perform health checks for your service. Valid values: TCP, HTTP. Defaults to TCP. If you set protocol to HTTP, App Runner sends health check requests to the HTTP path specified by path."
}

variable "timeout" {
  type        = number
  default     = 2
  description = " The time, in seconds, to wait for a health check response before deciding it failed. Defaults to 2. Minimum value of 1. Maximum value of 20."
}

variable "unhealthy_threshold" {
  type        = number
  default     = 5
  description = "The number of consecutive checks that must fail before App Runner decides that the service is unhealthy. Defaults to 5. Minimum value of 1. Maximum value of 20."

}
