import os
import json
import sys

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("./config.json", encoding="utf-8") as file:
        config = json.load(file)

import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient(config["DATABASE_URL"])
