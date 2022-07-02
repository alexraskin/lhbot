terraform {
  backend "s3" {
    bucket  = "terraform-state-lhbot"
    key     = "terraform.tfstate"
    encrypt = true
    region  = "us-east-1"
    profile = "lhcloudybot"
  }
}

provider "heroku" {
  email   = var.heroku_email
  api_key = var.heroku_api_key
}


resource "heroku_app" "lhbot" {
  name                  = var.app_name
  region                = var.app_region
  sensitive_config_vars = var.heroku_enviorment_vars
  stack                 = var.heroku_stack
}

resource "heroku_build" "lhbot" {
  app_id = heroku_app.lhbot.id

  source {
    url     = var.source_code_url
    version = var.app_version
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "heroku_formation" "lhbot" {
  app_id     = heroku_app.lhbot.id
  type       = var.dyno_type
  quantity   = var.app_quantity
  size       = var.dyno_size
  depends_on = [heroku_build.lhbot]
}

resource "heroku_app_release" "lhbot" {
  app_id  = heroku_app.lhbot.id
  slug_id = heroku_slug.lhbot.id
}

resource "heroku_slug" "lhbot" {
  app_id   = heroku_app.lhbot.id
  file_url = var.source_code_url

  process_types = {
    worker = "python bot/bot.py"
  }
}

resource "heroku_app_webhook" "lhbot" {
  app_id  = heroku_app.lhbot.id
  level   = "notify"
  url     = var.webhook_url
  include = ["api:release"]
}

resource "heroku_collaborator" "lhbot" {
  app_id = heroku_app.lhbot.id
  email  = var.collaborator_email
}
