import datetime
import logging
import os
import platform
import time
from functools import lru_cache

import motor.motor_asyncio
import psutil
import sentry_sdk
from aiohttp import ClientSession, ClientTimeout
from cogs import EXTENSIONS
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
    """
    Main bot class
    """

    def __init__(self, *args, **options) -> None:
        super().__init__(*args, **options)
        self.session = None
        self.db_client = None
        self.start_time = None
        self.version = config.bot_version
        self.config = config
        self.main_guild = 766217366568304660
        self.pid = os.getpid()
        self.status = Status.online
        self.logger = logging.getLogger("discord")
        self.start_time = time.time()
        self.logo_url: str = "https://i.gyazo.com/632f0e60dc0535128971887acad98993.png"
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
                capture_exception(exc)
                self.logger.error(
                    f"Could not load extension: {cog} due to {exc.__class__.__name__}: {exc}"
                )

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
    guild_ready_timeout=10,
    strip_after_prefix=True,
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
logging.info(f"{client.user.name} stopped successfully")
