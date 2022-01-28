import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    bot_token: str = os.getenv("BOT_TOKEN")
    application_id: str = os.getenv("APPLICATION_ID")
    database_url: str = os.getenv("DATABASE_URL")
    filestack_api_key: str = os.getenv("FILE_STACK_API_KEY")
    owners: list = os.getenv("owners")
    admin_roles: list = os.getenv("admin_roles")
    superusers: list = os.getenv("superusers")
    main_guild: int = os.get("main_guild")

    