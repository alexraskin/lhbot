import json
import os
import platform
import random
import sys
from datetime import datetime

import discord
from aiohttp import ClientSession, ClientTimeout
from discord.ext import tasks, commands
from discord.ext.commands import Bot

from utils.clear_dir import _clear_dir

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json", encoding="utf-8") as file:
        config = json.load(file)

class LhBot(Bot):
    def __init__(self, *args, **options):
        super().__init__(*args, **options)
        self.session = None
        self.flood_mode = False
        self.last_errors = []

    async def start(self, *args, **kwargs):
        self.session = ClientSession(timeout=ClientTimeout(total=30))
        await super().start(config["token"], *args, **kwargs)

    async def close(self):
        await self.session.close()
        await super().close()

    def user_is_admin(self, user):
        try:
            user_roles = [role.id for role in user.roles]
        except AttributeError:
            return False
        permitted_roles = self.config['admin_roles']
        return any(role in permitted_roles for role in user_roles)

    def user_is_superuser(self, user):
        superusers = self.config['superusers']
        return user.id in superusers


client = LhBot(
    command_prefix=config["bot_prefix"],
    description='Hi I am LhBot!',
    max_messages=15000,
    intents=discord.Intents.all(),
    allowed_mentions=discord.AllowedMentions(everyone=False, users=True, roles=True)
)

STARTUP_EXTENSIONS = []

for file in os.listdir(os.path.join(os.path.dirname(__file__), 'cogs/')):
    filename, ext = os.path.splitext(file)
    if '.py' in ext:
        STARTUP_EXTENSIONS.append(f'cogs.{filename}')

for extension in reversed(STARTUP_EXTENSIONS):
    try:
        client.load_extension(f'{extension}')
    except Exception as e:
        client.last_errors.append((e, datetime.utcnow(), None, None))
        exc = f'{type(e).__name__}: {e}'
        print(f'Failed to load extension {extension}\n{exc}')

@tasks.loop(minutes=1.0)
async def status_task():
    statuses = [
        "Overwatch",
        "Overwatch 2",
        "Diffing LhCloudy",
        f"{config['bot_prefix']}help",
        f"{config['bot_prefix']}lhhint",
        f"{config['bot_prefix']}info",
    ]
    await client.change_presence(activity=discord.Game(random.choice(statuses)))

@tasks.loop(minutes=60)
async def clean_dir():
    _clear_dir("./files")

@client.event
async def on_ready():
    print(f"Discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")
    status_task.start()
    clean_dir.start()
    print(f'\n{client.user.name} started successfully')
    return True


@client.event
async def on_command_error(context, error):
    if isinstance(error, commands.CommandOnCooldown):
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        embed = discord.Embed(
            title="Hey, please slow down!",
            description=f"You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="Error!",
            description="You are missing the permission `" + ", ".join(
                error.missing_perms) + "` to execute this command!",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="Error!",
            description=str(error).capitalize(),
            color=0xE02B2B
        )
        await context.send(embed=embed)
    raise error

@client.event
async def on_message(message):
    if isinstance(message.channel, discord.DMChannel):
        return
    await client.process_commands(message)

@client.event
async def on_command_completion(ctx):
    full_command_name = ctx.command.qualified_name
    split = full_command_name.split(" ")
    executed_command = str(split[0])
    print(
        f"Executed {executed_command} command in {ctx.guild.name} (ID: {ctx.message.guild.id}) by {ctx.message.author} (ID: {ctx.message.author.id})"
    )


client.run()
print('LhBot has exited')