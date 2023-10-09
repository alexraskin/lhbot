import datetime
import logging
import os
import platform
import time
from functools import lru_cache
import psutil

import motor.motor_asyncio
import sentry_sdk
from cogs import EXTENSIONS
from aiohttp import ClientSession, ClientTimeout
from config import Settings
from discord import AllowedMentions, Intents, Status, User
from discord.ext import tasks
from discord.ext.commands import AutoShardedBot, when_mentioned_or
from sentry_sdk import capture_exception
from utils.clear_dir import clean_cache

logging.basicConfig(level=logging.INFO)


@lru_cache()
def settings():
    return Settings()


config = settings()

sentry_sdk.init(config.sentry_dsn, traces_sample_rate=1.0)


class LhBot(AutoShardedBot):
    def __init__(self, *args, **options) -> None:
        super().__init__(*args, **options)
        self.session = None
        self.db_client = None
        self.start_time = None
        self.version = config.bot_version
        self.config = config
        self.status = Status.online
        self.logger = logging.getLogger("discord")
        self.start_time = time.time()
        self.logo_url = "https://i.gyazo.com/fa23d3eb9c323b3f39b8ba9dadaa8f95.png"
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
        self.bot_app_info = await self.application_info()
        self.owner_id = self.bot_app_info.owner.id
        for cog in EXTENSIONS:
            try:
                await self.load_extension(cog)
                self.logger.info(f"Loaded extension: {cog}")
            except Exception as exc:
                self.logger.error(
                    f"Could not load extension: {cog} due to {exc.__class__.__name__}: {exc}"
                )

    def user_is_admin(self, user) -> bool:
        try:
            user_roles = [role.id for role in user.roles]
        except AttributeError as error:
            capture_exception(error)
            return False
        permitted_roles = self.config.admin_roles
        return any(role in permitted_roles for role in user_roles)

    def user_is_superuser(self, user) -> bool:
        superusers = self.config.superusers
        return user.id in superusers

    @property
    def get_uptime(self) -> str:
        return str(
            datetime.timedelta(seconds=int(round(time.time() - self.start_time)))
        )

    @property
    def get_bot_latency(self) -> float:
        return round(self.latency * 1000)

    @property
    def memory_usage(self) -> int:
        process = psutil.Process(self.pid)
        memory_info = process.memory_info()
        return round(memory_info.rss / (1024**2))

    @property
    def cpu_usage(self) -> float:
        return psutil.cpu_percent(interval=1)

    @property
    def git_revision(self):
        latest_revision = os.getenv("RAILWAY_GIT_COMMIT_SHA")
        if latest_revision is None:
            return None
        url = f"<https://github.com/alexraskin/lhbot/commit/{(short := latest_revision[:7])}>"
        return f"[{short}]({url})"

    @property
    def owner(self) -> User:
        return self.bot_app_info.owner


client = LhBot(
    command_prefix=when_mentioned_or(config.bot_prefix),
    description="Hi, I am LhBot!",
    max_messages=15000,
    intents=Intents.all(),
    allowed_mentions=AllowedMentions(everyone=False, users=True, roles=True),
)


@tasks.loop(minutes=60)
async def clean_dir() -> None:
    clean_cache("./bot/files", ".pdf")


@client.event
async def on_ready() -> bool:
    main_id = config.main_guild
    client.main_guild = client.get_guild(main_id) or client.guilds[0]
    logging.info(f"{client.user.name} started successfully")
    clean_dir.start()


client.run(token=config.bot_token, reconnect=True, log_handler=None)
logging.info("LhBot has exited")
