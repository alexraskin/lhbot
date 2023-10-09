variable "railway_token" {
  type        = string
  description = "Railway token"
}

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

variable "heroku_email" {
  type        = string
  description = "Heroku account email"
}

variable "heroku_api_key" {
  type        = string
  description = "Heroku API Key"
}

variable "heroku_stack" {
  type        = string
  description = "Stack for your Heroku app"
}

variable "dyno_type" {
  type        = string
  description = "Type of dyno"
}

variable "dyno_size" {
  type        = string
  description = "Size of dyno"
}

variable "app_region" {
  type        = string
  description = "The region to deploy the app to"
}

variable "app_quantity" {
  default     = 1
  description = "Number of dynos in your Heroku formation"
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
