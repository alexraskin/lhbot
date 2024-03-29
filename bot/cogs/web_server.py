from __future__ import annotations

import asyncio
import os
from pathlib import Path

from aiohttp import web
from discord import __version__ as discord_version
from discord.ext import commands


class WebServer(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client: commands.Bot = client
        self.path = os.path.join(Path(__file__).resolve().parent, "static/")

    @commands.Cog.listener()
    async def on_ready(self):
        self.client.logger.info(f"Webserver ready on port {self.client.config.port}")

    async def get_all_commands(self) -> list:
        commands: list = []
        for command in self.client.commands:
            if command.hidden is False:
                commands.append({"name": command.name, "description": command.help})
        return commands

    async def index_handler(self, request: web.Request) -> web.Response:
        self.client.logger.info(f"Webserver request from {request.remote}")
        self.client.logger.info(f"Webserver request for {request.path}")
        self.client.logger.info(f"Webserver request for {request.query_string}")
        return web.json_response(
            {
                "discord_version": discord_version,
                "bot_version": self.client.config.bot_version,
                "bot_latency": f"{self.client.get_bot_latency}ms",
                "bot_uptime": self.client.get_uptime,
                "bot_ram": f"{self.client.memory_usage}MB",
                "bot_cpu": f"{self.client.cpu_usage}%",
                "commands": await self.get_all_commands(),
            }
        )

    async def webserver(self) -> None:
        app = web.Application()
        app.router.add_get("/", self.index_handler)
        runner = web.AppRunner(app)
        await runner.setup()
        self.site = web.TCPSite(runner, "0.0.0.0", self.client.config.port)
        await self.client.wait_until_ready()
        await self.site.start()

    def __unload(self):
        asyncio.ensure_future(self.site.stop())


async def setup(client):
    server = WebServer(client)
    client.loop.create_task(server.webserver())
    await client.add_cog(WebServer(client))
