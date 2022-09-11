import os
import platform
import random
from functools import lru_cache

import discord
import discordhealthcheck
import sentry_sdk
from aiohttp import ClientSession, ClientTimeout
from config import Settings
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from sentry_sdk import capture_exception
from utils.clear_dir import clean_cache


@lru_cache()
def settings():
    return Settings()


conf = settings()

sentry_sdk.init(conf.sentry_dsn, traces_sample_rate=1.0)


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
        self.healthcheck_server = discordhealthcheck.start(self)
        self.user_agent = f"{conf.bot_name}/{conf.bot_version} ({platform.system()})"
        self.headers = {"User-Agent": self.user_agent}

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
        self.session = ClientSession(
            timeout=ClientTimeout(total=30), headers=self.headers
        )
        await super().start(conf.bot_token, *args, **kwargs)

    async def close(self):
        """
        The close function closes the session

        :param self: Used to access the class attributes.
        :return: the aiohttp.
        """
        self.healthcheck_server.close()
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
        except AttributeError as e:
            capture_exception(e)
            return False
        permitted_roles = conf.admin_roles
        return any(role in permitted_roles for role in user_roles)

    def user_is_superuser(self, user):
        """
        The user_is_superuser function specifically checks if the user is a superuser.

        :param self: Used to refer to the object itself.
        :param user: Used to check if the user is a superuser.
        :return: True if the user is a superuser and False otherwise.
        """
        superusers = conf.superusers
        return user.id in superusers


client = LhBot(
    command_prefix=conf.bot_prefix,
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
        capture_exception(e)
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
        f"{conf.bot_prefix}help",
        f"{conf.bot_prefix}info",
        f"{conf.bot_prefix}dog",
        f"{conf.bot_prefix}cat",
        f"{conf.bot_prefix}meme",
    ]
    await client.change_presence(activity=discord.Game(random.choice(statuses)))


@tasks.loop(minutes=60)
async def clean_dir():
    """
    The clean_dir function is used to clean the directory of all files that are not
    .py, .txt or .json files.

    :return: bool
    """
    clean_cache("./bot/files", ".pdf")


@client.event
async def on_ready():
    """
    The on_ready function specifically accomplishes the following:
        - Sets up a status task that changes the bot's status every 60 seconds.
        - Sets up a clean_dir task that cleans out old files in the cache directory every 5 minutes.

    :return: a string with the details of our main guild.
    """
    main_id = conf.main_guild
    client.main_guild = client.get_guild(main_id) or client.guilds[0]
    print(f"Discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")
    print("\nMain guild:", client.main_guild.name)
    print(f"\n{client.user.name} started successfully")
    status_task.start()
    clean_dir.start()
    return True


@client.event
async def on_command_error(ctx, error):
    error_message = {
        commands.BotMissingPermissions: "I don't have the permissions needed to run this command",
        commands.MissingRole: "You don't have the role(s) needed to use this command",
        commands.BadArgument: "Unexpected argument (check your capitalization and parameter order)",
        commands.MissingRequiredArgument: "Missing required argument.",
        commands.TooManyArguments: "Too many arguments",
        commands.CheckFailure: "You don't have the permissions needed to use this command",
        AttributeError: "It's probably due to a spelling error somewhere",
    }
    try:
        description = "Error: " + error_message[error]
        await ctx.channel.send(
            embed=discord.Embed(
                description=description, color=discord.Color.from_rgb(214, 11, 11)
            )
        )
    except KeyError as e:
        capture_exception(e)
        if isinstance(error, commands.CommandNotFound):
            return


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        if round(error.retry_after) <= 1:
            await ctx.send(
                f"This command is on cool down. Please try again in {round(error.retry_after)} second"
            )
        else:
            await ctx.send(
                f"This command is on cool down. Please try again in {round(error.retry_after)} seconds"
            )
        return


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


client.run(reconnect=True)
print("LhBot has exited")
