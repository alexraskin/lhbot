import json
import os
import platform
import random
import sys

import discord
from discord.ext import tasks
from discord.ext.commands import Bot

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

intents = discord.Intents.default()

bot = Bot(command_prefix=config["bot_prefix"], intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print(f"Discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")
    status_task.start()


@tasks.loop(minutes=1.0)
async def status_task():
    statuses = [
      "Overwatch", "Overwatch 2",
      f"{config['bot_prefix']}help",
      f"{config['bot_prefix']}lhhint",
      f"{config['bot_prefix']}info"
      ]
    await bot.change_presence(activity=discord.Game(random.choice(statuses)))


if __name__ == "__main__":
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                bot.load_extension(f"cogs.{extension}")
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")

bot.run(config["token"])
