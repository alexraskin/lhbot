import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """
    The Settings class is a class that contains all the settings for the bot.
    """

    docker_enabled = os.getenv("DOCKER_ENABLED", False)
    port = int(os.getenv("PORT", 8000))
    bot_prefix: str = os.getenv("BOT_PREFIX")
    bot_token: str = os.getenv("BOT_TOKEN")
    application_id: str = os.getenv("APPLICATION_ID")
    database_url: str = os.getenv("DATABASE_URL")
    owners: list = os.getenv("OWNERS")
    admin_roles: list = os.getenv("ADMIN_ROLES")
    superusers: list = os.getenv("SUPERUSERS")
    main_guild: int = os.getenv("MAIN_GUILD")
    sentry_dsn: str = os.getenv("SENTRY_DSN")
    giphy_api_key: str = os.getenv("GIPHY_API_KEY")
    bot_name: str = os.getenv("BOT_NAME")
    bot_version: str = os.getenv("BOT_VERSION")
    aws_access_key: str = os.getenv("AWS_ACCESS_KEY")
    aws_secret_access_key: str = os.getenv("AWS_SECRET_ACCESS_KEY")
    s3_bucket_name: str = os.getenv("S3_BUCKET_NAME")
