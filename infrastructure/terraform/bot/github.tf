provider "github" {
  token = var.github_token
}

resource "github_actions_secret" "lhbot_github_actions_secret" {
  repository      = "lhbot"
  for_each        = local.heroku_enviorment_vars
  secret_name     = each.key
  plaintext_value = each.value
}

resource "github_actions_secret" "mongodbatlas_public_key" {
  repository      = "lhbot"
  secret_name     = "mongodbatlas_public_key"
  plaintext_value = var.mongodbatlas_public_key
}

resource "github_actions_secret" "mongodbatlas_private_key" {
  repository      = "lhbot"
  secret_name     = "mongodbatlas_private_key"
  plaintext_value = var.mongodbatlas_private_key
}

resource "github_actions_secret" "heroku_email" {
  repository      = "lhbot"
  secret_name     = "heroku_email"
  plaintext_value = var.heroku_email
}

resource "github_actions_secret" "heroku_api_key" {
  repository      = "lhbot"
  secret_name     = "heroku_api_key"
  plaintext_value = var.heroku_api_key
}

resource "github_actions_secret" "heroku_app_name" {
  repository      = "lhbot"
  secret_name     = "app_name"
  plaintext_value = var.app_name
}

resource "github_actions_secret" "heroku_app_region" {
  repository      = "lhbot"
  secret_name     = "app_region"
  plaintext_value = var.app_region
}

resource "github_actions_secret" "heroku_stack" {
  repository      = "lhbot"
  secret_name     = "heroku_stack"
  plaintext_value = var.heroku_stack
}

resource "github_actions_secret" "heroku_dyno_type" {
  repository      = "lhbot"
  secret_name     = "dyno_type"
  plaintext_value = var.dyno_type
}

resource "github_actions_secret" "heroku_dyno_size" {
  repository      = "lhbot"
  secret_name     = "dyno_size"
  plaintext_value = var.dyno_size
}

resource "github_actions_secret" "git_version_tag" {
  repository      = "lhbot"
  secret_name     = "git_version_tag"
  plaintext_value = local.latest_tag
}
