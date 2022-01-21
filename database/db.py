import json
import os
import sys

import motor.motor_asyncio

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("./config.json", encoding="utf-8") as file:
        config = json.load(file)

db_client = motor.motor_asyncio.AsyncIOMotorClient(config["DATABASE_URL"])
