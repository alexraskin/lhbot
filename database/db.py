from functools import lru_cache

import motor.motor_asyncio

from config import Settings


@lru_cache()
def settings():
    return Settings()


conf = settings()

db_client = motor.motor_asyncio.AsyncIOMotorClient(conf.database_url)
