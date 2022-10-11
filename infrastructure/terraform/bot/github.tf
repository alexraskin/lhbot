provider "github" {
  token = var.github_token
}

resource "github_actions_secret" "lhbot_github_actions_secret" {
  repository       = "lhbot"
  for_each = local.heroku_enviorment_vars
  secret_name      = each.key
  plaintext_value  = each.value
}
