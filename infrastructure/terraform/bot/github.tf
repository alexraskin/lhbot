provider "github" {
  token = var.github_token
}

resource "github_actions_secret" "lhbot_github_actions_secret" {
  repository      = "lhbot"
  for_each        = local.enviorment_vars
  secret_name     = each.key
  plaintext_value = each.value
}

resource "github_actions_secret" "aws_ac_key" {
  repository      = "lhbot"
  secret_name     = "AWS_ACCESS_KEY_ID"
  plaintext_value = var.enviorment_vars["AWS_ACCESS_KEY"]
}

resource "github_actions_secret" "aws_s_key" {
  repository      = "lhbot"
  secret_name     = "AWS_SECRET_ACCESS_KEY"
  plaintext_value = var.enviorment_vars["AWS_SECRET_ACCESS_KEY"]
}

resource "github_actions_secret" "aws_ecr_repo" {
  repository      = "lhbot"
  secret_name     = "AWS_ECR_REPOSITORY"
  plaintext_value = var.enviorment_vars["AWS_ECR_REPOSITORY"]
}