import os
import platform
import random
from datetime import datetime
from functools import lru_cache

import discord
from aiohttp import ClientSession, ClientTimeout
from discord.ext import commands, tasks
from discord.ext.commands import Bot

from config import Settings
from utils.clear_dir import _clear_dir

PREFIX = "!"


@lru_cache()
def settings():
    return Settings()


creds = settings()


class LhBot(Bot):
    def __init__(self, *args, **options):
        """
        The __init__ function is the constructor for a class.
        It is called when an instance of a class is created.
        It can take arguments (in this case, *args and **options)

        :param self: Used to refer to the object itself.
        :param *args: Used to pass a non-keyworded, variable-length argument list to the function.
        :param **options: Used to pass a dictionary of keyword arguments to the function.
        :return: a new instance of the Session class.
        """
        super().__init__(*args, **options)
        self.session = None
        self.last_errors = []

    async def start(self, *args, **kwargs):
        """
        The start function is used to start the bot.
        It creates a ClientSession object
         which allows us to make requests and download data from the internet.
        It also sets up our command prefixes and loads cogs.

        :param self: Used to access the class attributes.
        :param *args: Used to pass a non-keyworded, variable-length argument list.
        :param **kwargs: Used to pass a keyworded, variable-length argument list.
        :return: ClientSession object.
        """
        self.session = ClientSession(timeout=ClientTimeout(total=30))
        await super().start(creds.bot_token, *args, **kwargs)

    async def close(self):
        """
        The close function closes the session

        :param self: Used to access the class attributes.
        :return: the aiohttp.
        """
        await self.session.close()
        await super().close()

    def user_is_admin(self, user):
        """
        The user_is_admin function specifically checks
        if the user has a role that is in the permitted_roles list.
        The permitted_roles list contains
        all of the roles that are allowed to access admin functions.

        :param self: Used to access attributes of the class.
        :param user: Used to check if the user has a certain role.
        :return: false if the user attribute is not an instance of discord.
        """
        try:
            user_roles = [role.id for role in user.roles]
        except AttributeError:
            return False
        permitted_roles = creds.admin_roles
        return any(role in permitted_roles for role in user_roles)

    def user_is_superuser(self, user):
        """
        The user_is_superuser function specifically checks if the user is a superuser.

        :param self: Used to refer to the object itself.
        :param user: Used to check if the user is a superuser.
        :return: True if the user is a superuser and False otherwise.
        """
        superusers = creds.superusers
        return user.id in superusers


client = LhBot(
    command_prefix=creds.bot_prefix,
    description="Hi I am LhBot!",
    max_messages=15000,
    intents=discord.Intents.all(),
    allowed_mentions=discord.AllowedMentions(everyone=False, users=True, roles=True),
)

STARTUP_EXTENSIONS = []

for file in os.listdir(os.path.join(os.path.dirname(__file__), "cogs/")):
    filename, ext = os.path.splitext(file)
    if ".py" in ext:
        STARTUP_EXTENSIONS.append(f"cogs.{filename}")

for extension in reversed(STARTUP_EXTENSIONS):
    try:
        client.load_extension(f"{extension}")
        print(f"Loaded extension '{extension}'")
    except Exception as e:
        client.last_errors.append((e, datetime.utcnow(), None, None))
        exc = f"{type(e).__name__}: {e}"
        print(f"Failed to load extension {extension}\n{exc}")


@tasks.loop(minutes=1.0)
async def status_task():
    """
    The status_task function is a loop that will run every 60 seconds.
    It will randomly select one of the statuses from the list
    and set it as the bot's status.

    :return: a list of strings that will be used to change the status of the bot.
    """
    statuses = [
        "Overwatch",
        "Overwatch 2",
        "Diffing LhCloudy",
        f"{creds.bot_prefix}help",
        f"{creds.bot_prefix}info",
        f"{creds.bot_prefix}dog",
        f"{creds.bot_prefix}cat",
        f"{creds.bot_prefix}meme",
    ]
    await client.change_presence(activity=discord.Game(random.choice(statuses)))


@tasks.loop(minutes=60)
async def clean_dir():
    """
    The clean_dir function is used to clean the directory of all files that are not
    .py, .txt or .json files.

    :return: bool
    """
    _clear_dir("./files", ".pdf")


@client.event
async def on_ready():
    """
    The on_ready function specifically accomplishes the following:
        - Sets up a status task that changes the bot's status every 60 seconds.
        - Sets up a clean_dir task that cleans out old files in the cache directory every 5 minutes.

    :return: a string with the details of our main guild.
    """
    main_id = creds.main_guild
    client.main_guild = client.get_guild(main_id) or client.guilds[0]
    print(f"Discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")
    status_task.start()
    clean_dir.start()
    print("\nMain guild:", client.main_guild.name)
    print(f"\n{client.user.name} started successfully")
    return True


@client.event
async def on_command_error(context, error):
    """
    The on_command_error function is used to handle errors that occur while executing a command.
    It's called when an error is raised while invoking a command,
    and it passes itself and the context of the invocation as arguments.

    :param context: Used to send messages to the user.
    :param error: Used to handle errors.
    :return: None.
    """
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="Error!",
            description="You are missing the permission `"
            + ", ".join(error.missing_perms)
            + "` to execute this command!",
            color=0xE02B2B,
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="Error!", description=str(error).capitalize(), color=0xE02B2B
        )
        await context.send(embed=embed)
    raise error


@client.event
async def on_message(message):
    """
    The on_message function specifically is what allows the bot to recognize messages and respond accordingly.
    It also checks if the message was sent in a DM channel, which it ignores.

    :param message: Used to get the message content and other information.
    :return: a "None" object.
    """
    if isinstance(message.channel, discord.DMChannel):
        return
    await client.process_commands(message)


@client.event
async def on_command_completion(ctx):
    """
    The on_command_completion function specifically tracks the commands that are executed in each server.
    It also prints out the command name and server name to a text file called "command_logs.txt".

    :param ctx: Used to access the context of the command.
    :return: a string of the executed command.
    """
    full_command_name = ctx.command.qualified_name
    split = full_command_name.split(" ")
    executed_command = str(split[0])
    print(
        f"Executed {executed_command} command in {ctx.guild.name}"
        + f"(ID: {ctx.message.guild.id}) by {ctx.message.author} (ID: {ctx.message.author.id})"
    )


client.run()
print("LhBot has exited")
