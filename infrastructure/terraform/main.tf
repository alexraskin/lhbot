terraform {
  backend "s3" {
    bucket  = "terraform-state-lhbot"
    key     = "terraform.tfstate"
    encrypt = true
    region  = "us-east-1"
    profile = "default"
  }
}

provider "heroku" {}

locals {
  app_region = "us"
  heroku_enviorment_vars = {
    BOT_PREFIX        = var.heroku_enviorment_vars["BOT_PREFIX"]
    BOT_TOKEN         = var.heroku_enviorment_vars["BOT_TOKEN"]
    APPLICATION_ID    = var.heroku_enviorment_vars["APPLICATION_ID"]
    DATABASE_URL      = var.heroku_enviorment_vars["DATABASE_URL"]
    SENTRY_DSN        = var.heroku_enviorment_vars["SENTRY_DSN"]
    main_guild        = var.heroku_enviorment_vars["main_guild"]
    owners            = var.heroku_enviorment_vars["owners"]
    superusers        = var.heroku_enviorment_vars["superusers"]
    admin_roles       = var.heroku_enviorment_vars["admin_roles"]
    GIPHY_API_KEY     = var.heroku_enviorment_vars["GIPHY_API_KEY"]
    BOT_NAME          = var.heroku_enviorment_vars["BOT_NAME"]
    AWS_ACCESS_KEY_ID = var.heroku_enviorment_vars["AWS_ACCESS_KEY"]
    AWS_SECRET_KEY_ID = var.heroku_enviorment_vars["AWS_SECRET_ACCESS_KEY"]
    AWS_REGION        = var.heroku_enviorment_vars["AWS_REGION"]
    S3_BUCKET_NAME    = var.heroku_enviorment_vars["S3_BUCKET_NAME"]
  }
}

resource "heroku_app" "lhbot" {
  name                  = var.app_name
  region                = local.app_region
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
