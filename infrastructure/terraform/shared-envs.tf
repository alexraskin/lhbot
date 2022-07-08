locals {
  heroku_enviorment_vars = {
    BOT_PREFIX        = var.heroku_enviorment_vars["BOT_PREFIX"]
    BOT_TOKEN         = var.heroku_enviorment_vars["BOT_TOKEN"]
    BOT_VERSION       = var.heroku_enviorment_vars["BOT_VERSION"]
    APPLICATION_ID    = var.heroku_enviorment_vars["APPLICATION_ID"]
    DATABASE_URL      = var.heroku_enviorment_vars["DATABASE_URL"]
    SENTRY_DSN        = var.heroku_enviorment_vars["SENTRY_DSN"]
    MAIN_GUILD        = var.heroku_enviorment_vars["MAIN_GUILD"]
    OWNERS            = var.heroku_enviorment_vars["OWNERS"]
    SUPERUSERS        = var.heroku_enviorment_vars["SUPERUSERS"]
    ADMIN_ROLES       = var.heroku_enviorment_vars["ADMIN_ROLES"]
    GIPHY_API_KEY     = var.heroku_enviorment_vars["GIPHY_API_KEY"]
    BOT_NAME          = var.heroku_enviorment_vars["BOT_NAME"]
    AWS_ACCESS_KEY_ID = var.heroku_enviorment_vars["AWS_ACCESS_KEY"]
    AWS_SECRET_KEY_ID = var.heroku_enviorment_vars["AWS_SECRET_ACCESS_KEY"]
    AWS_REGION        = var.heroku_enviorment_vars["AWS_REGION"]
    S3_BUCKET_NAME    = var.heroku_enviorment_vars["S3_BUCKET_NAME"]
  }
}
