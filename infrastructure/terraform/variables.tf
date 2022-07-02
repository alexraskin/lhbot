variable "app_name" {
  type = string
}

variable "app_quantity" {
  default     = 1
  description = "Number of dynos in your Heroku formation"
}

variable "heroku_enviorment_vars" {
  type        = map(string)
  description = "Environment variables for Heroku app"
}

variable "source_code_url" {
  type        = string
  description = "URL to the source code"
}

variable "app_version" {
  type        = string
  description = "Version of the app"
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

variable "webhook_url" {
  type        = string
  description = "URL to the webhook"
}

variable "collaborator_email" {
  type = string
}