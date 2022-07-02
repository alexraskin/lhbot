import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    bot_prefix: str = os.getenv("BOT_PREFIX")
    bot_token: str = os.getenv("BOT_TOKEN")
    application_id: str = os.getenv("APPLICATION_ID")
    database_url: str = os.getenv("DATABASE_URL")
    owners: list = os.getenv("owners")
    admin_roles: list = os.getenv("admin_roles")
    superusers: list = os.getenv("superusers")
    main_guild: int = os.getenv("main_guild")
    sentry_dsn: str = os.getenv("SENTRY_DSN")
    giphy_api_key: str = os.getenv("GIPHY_API_KEY")
    bot_name: str = os.getenv("BOT_NAME")
    bot_version: str = "0.1.0"
    aws_access_key: str = os.getenv("AWS_ACCESS_KEY")
    aws_secret_access_key: str = os.getenv("AWS_SECRET_ACCESS_KEY")
    s3_bucket_name: str = os.getenv("S3_BUCKET_NAME")
