provider "heroku" {
  email   = var.heroku_email
  api_key = var.heroku_api_key
}

locals {
  latest_tag      = jsondecode(data.http.github_tag.response_body)[0].name
  source_code_url = "https://github.com/alexraskin/lhbot/archive/refs/tags/${local.latest_tag}.tar.gz"
}

resource "heroku_app" "lhbot" {
  name                  = var.app_name
  region                = var.app_region
  sensitive_config_vars = var.enviorment_vars
  stack                 = var.heroku_stack
}

resource "heroku_build" "lhbot" {
  app_id = heroku_app.lhbot.id
  source {
    url     = local.source_code_url
    version = local.latest_tag
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "heroku_formation" "lhbot" {
  app_id   = heroku_app.lhbot.id
  type     = var.dyno_type
  quantity = var.app_quantity
  size     = var.dyno_size
  depends_on = [
    heroku_build.lhbot,
    heroku_app_release.lhbot
  ]
}

resource "heroku_app_release" "lhbot" {
  app_id  = heroku_app.lhbot.id
  slug_id = heroku_slug.lhbot.id
}

resource "heroku_slug" "lhbot" {
  app_id   = heroku_app.lhbot.id
  file_url = local.source_code_url

  process_types = {
    web = "python bot/bot.py"
  }
}

resource "heroku_domain" "lhbot" {
  app_id   = heroku_app.lhbot.id
  hostname = "lhbot.twizy.dev"
}
