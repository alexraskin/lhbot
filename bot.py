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
    with open("config.json", encoding='utf-8') as file:
        config = json.load(file)

intents = discord.Intents.default()

bot = Bot(command_prefix=config["bot_prefix"], intents=intents)


@bot.event
async def on_ready():
    """
    code in this event is executed on ready
    """
    print(f"Logged in as {bot.user.name}")
    print(f"Discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")
    status_task.start()


@tasks.loop(minutes=1.0)
async def status_task():
    """
    run a task to change the game presence
    """
    statuses = [
        "Overwatch", "Overwatch 2", "Diffing LhCloudy",
        f"{config['bot_prefix']}help", f"{config['bot_prefix']}lhhint",
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


@bot.event
async def on_message(message):
    """
    do not want the bot to reply to itself
    """
    if message.author == bot.user or message.author.bot:
        return
    await bot.process_commands(message)


@bot.event
async def on_command_completion(ctx):
    """
    code in this event is executed every time a command has been *successfully* executed
    """
    full_command_name = ctx.command.qualified_name
    split = full_command_name.split(" ")
    executed_command = str(split[0])
    print(
        f"Executed {executed_command}\
            command in {ctx.guild.name}\
                (ID: {ctx.message.guild.id})\
                    by {ctx.message.author} (ID: {ctx.message.author.id})"
    )


bot.run(config["token"])
