from functools import lru_cache

import motor.motor_asyncio

from config import Settings


@lru_cache()
def settings():
    return Settings()


creds = settings()

db_client = motor.motor_asyncio.AsyncIOMotorClient(creds.database_url)
