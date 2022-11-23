import logging
import platform
import random
from functools import lru_cache
from os import listdir, path

import motor.motor_asyncio
import sentry_sdk
from aiohttp import ClientSession, ClientTimeout
from config import Settings
from discord import AllowedMentions, Color, Embed, Game, Intents, Status
from discord.ext import commands, tasks
from discord.ext.commands import AutoShardedBot
from sentry_sdk import capture_exception
from utils.clear_dir import clean_cache

logging.basicConfig(level=logging.INFO)


@lru_cache()
def settings():
    """
    Load the settings from the config file.
    """
    return Settings()


config = settings()

sentry_sdk.init(config.sentry_dsn, traces_sample_rate=1.0)


class LhBot(AutoShardedBot):
    """
    The Bot class is a subclass of the AutoShardedBot class.
    """

    def __init__(self, *args, **options) -> None:
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
        self.db_client = None
        self.config = config
        self.status = Status.online
        self.user_agent = (
            f"{self.config.bot_name}/{self.config.bot_version}:{platform.system()}"
        )
        self.headers = {"User-Agent": self.user_agent}

    async def start(self, *args, **kwargs) -> None:
        self.session = ClientSession(
            timeout=ClientTimeout(total=30), headers=self.headers
        )
        self.db_client = motor.motor_asyncio.AsyncIOMotorClient(
            self.config.database_url
        )
        await super().start(*args, **kwargs)

    async def close(self) -> None:
        await self.session.close()
        await super().close()

    async def setup_hook(self) -> None:
        logging.info("Loading Extensions:")
        startup_extensions = []
        for file in listdir(path.join(path.dirname(__file__), "cogs/")):
            filename, ext = path.splitext(file)
            if ".py" in ext:
                startup_extensions.append(f"cogs.{filename}")

        for extension in reversed(startup_extensions):
            try:
                logging.info(f"Loading: {extension}")
                await self.load_extension(f"{extension}")
            except Exception as error:
                capture_exception(error)
                exc = f"{type(error).__name__}: {error}"
                logging.error(f"Failed to load extension {extension}\n{exc}")

    def user_is_admin(self, user) -> bool:
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
        except AttributeError as error:
            capture_exception(error)
            return False
        permitted_roles = self.config.admin_roles
        return any(role in permitted_roles for role in user_roles)

    def user_is_superuser(self, user) -> bool:
        """
        The user_is_superuser function specifically checks if the user is a superuser.

        :param self: Used to refer to the object itself.
        :param user: Used to check if the user is a superuser.
        :return: True if the user is a superuser and False otherwise.
        """
        superusers = self.config.superusers
        return user.id in superusers


client = LhBot(
    command_prefix=config.bot_prefix,
    description="Hi I am LhBot!",
    max_messages=15000,
    intents=Intents.all(),
    allowed_mentions=AllowedMentions(everyone=False, users=True, roles=True),
)


@tasks.loop(minutes=1.0)
async def status_task() -> None:
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
        f"{config.bot_prefix}help",
        f"{config.bot_prefix}info",
        f"{config.bot_prefix}dog",
        f"{config.bot_prefix}cat",
        f"{config.bot_prefix}meme",
    ]
    await client.change_presence(activity=Game(random.choice(statuses)))


@tasks.loop(minutes=60)
async def clean_dir() -> None:
    """
    The clean_dir function is used to clean the directory of all files that are not
    .py, .txt or .json files.

    :return: bool
    """
    clean_cache("./bot/files", ".pdf")


@client.event
async def on_ready() -> bool:
    """
    The on_ready function specifically accomplishes the following:
        - Sets up a status task that changes the bot's status every 60 seconds.
        - Sets up a clean_dir task that cleans out old files in the cache directory every 5 minutes.

    :return: a string with the details of our main guild.
    """
    main_id = config.main_guild
    client.main_guild = client.get_guild(main_id) or client.guilds[0]
    logging.info(f"{client.user.name} started successfully")
    status_task.start()
    clean_dir.start()
    return True


@client.event
async def on_command_error(ctx, error) -> None:
    """
    The on_command_error function is used to handle errors that occur when a command is run.
    """
    if ctx.command.qualified_name:
        full_command_name = ctx.command.qualified_name
    split = full_command_name.split(" ")
    executed_command = str(split[0])
    error_message = {
        commands.BotMissingPermissions: "I don't have the permissions needed to run this command",
        commands.MissingRole: "You don't have the role(s) needed to use this command",
        commands.BadArgument: "Unexpected argument (check your capitalization and parameter order)",
        commands.MissingRequiredArgument: "Missing required argument.",
        commands.TooManyArguments: "Too many arguments",
        commands.CheckFailure: "You don't have the permissions needed to use this command",
        AttributeError: "It's probably due to a spelling error somewhere",
    }

    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(
            "This command is on cool down."
            + f" Please try again in {round(error.retry_after)} "
            + f'{"second" if round(error.retry_after) <= 1 else "seconds"}.'
        )
        logging.info(
            f"Executed {executed_command} command in {ctx.guild.name}"
            + f"(ID: {ctx.message.guild.id}) by {ctx.message.author} (ID: {ctx.message.author.id})"
        )
        return

    if isinstance(error, commands.CommandNotFound):
        await ctx.send(
            f"Command not found, try `{config.bot_prefix}help` for a list of available commands."
        )
        return

    try:
        description = "Error: " + error_message[error]
        await ctx.channel.send(
            embed=Embed(description=description, color=Color.from_rgb(214, 11, 11))
        )
    except KeyError as error:
        logging.error(error)
        capture_exception(error)
        if isinstance(error, commands.CommandNotFound):
            return


@client.event
async def on_command_completion(ctx) -> None:
    """
    The on_command_completion function tracks the commands that are executed in each server.

    :param ctx: Used to access the context of the command.
    :return: a string of the executed command.
    """
    full_command_name = ctx.command.qualified_name
    split = full_command_name.split(" ")
    executed_command = str(split[0])
    logging.info(
        f"Executed {executed_command} command in {ctx.guild.name}"
        + f"(ID: {ctx.message.guild.id}) by {ctx.message.author} (ID: {ctx.message.author.id})"
    )


client.run(token=config.bot_token, reconnect=True, log_handler=None)
logging.info("LhBot has exited")
