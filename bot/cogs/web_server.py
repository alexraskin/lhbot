import asyncio
import os
from pathlib import Path

import aiohttp_jinja2
import jinja2
from aiohttp import web
from discord import __version__ as discord_version
from discord.ext import commands


class WebServer(commands.Cog, name="WebServer"):
    def __init__(self, client):
        self.client = client
        self.path = os.path.join(Path(__file__).resolve().parent, "static/")

    def html_response(self, text: str) -> web.Response:
        return web.Response(text=text, content_type="text/html")

    @aiohttp_jinja2.template("index.html")
    async def index_handler(self, request: web.Request) -> dict:
        return {
            "discord_version": discord_version,
            "bot_version": self.client.config.bot_version,
            "bot_latency": f"{self.client.get_bot_latency}ms",
            "bot_uptime": self.client.get_uptime,
        }

    async def webserver(self) -> None:
        app = web.Application()
        aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(self.path)))
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
