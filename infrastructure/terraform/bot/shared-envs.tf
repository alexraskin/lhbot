locals {
  enviorment_vars = {
    DATABASE_URL         = var.enviorment_vars["DATABASE_URL"]
    BOT_PREFIX           = var.enviorment_vars["BOT_PREFIX"]
    BOT_TOKEN            = var.enviorment_vars["BOT_TOKEN"]
    BOT_VERSION          = var.enviorment_vars["BOT_VERSION"]
    APPLICATION_ID       = var.enviorment_vars["APPLICATION_ID"]
    SENTRY_DSN           = var.enviorment_vars["SENTRY_DSN"]
    MAIN_GUILD           = var.enviorment_vars["MAIN_GUILD"]
    OWNERS               = var.enviorment_vars["OWNERS"]
    SUPERUSERS           = var.enviorment_vars["SUPERUSERS"]
    ADMIN_ROLES          = var.enviorment_vars["ADMIN_ROLES"]
    GIPHY_API_KEY        = var.enviorment_vars["GIPHY_API_KEY"]
    BOT_NAME             = var.enviorment_vars["BOT_NAME"]
    AWS_ACCESS_KEY_ID    = var.enviorment_vars["AWS_ACCESS_KEY"]
    AWS_SECRET_KEY_ID    = var.enviorment_vars["AWS_SECRET_ACCESS_KEY"]
    AWS_REGION           = var.enviorment_vars["AWS_REGION"]
    S3_BUCKET_NAME       = var.enviorment_vars["S3_BUCKET_NAME"]
    TWITCH_CLIENT_ID     = var.enviorment_vars["TWITCH_CLIENT_ID"]
    TWITCH_CLIENT_SECRET = var.enviorment_vars["TWITCH_CLIENT_SECRET"]
    OPENAI_API_KEY       = var.enviorment_vars["OPENAI_API_KEY"]
  }
}
