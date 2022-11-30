import asyncio
import os
import time
import datetime
from pathlib import Path

import aiohttp_jinja2
import jinja2
from aiohttp import web
from discord.ext import commands
from discord import __version__ as discord_version


class WebServer(commands.Cog, name="WebServer"):
    """WebServer cog for the bot."""
    def __init__(self, client):
        self.client = client
        self.path = os.path.join(Path(__file__).resolve().parent, "static/")

    def html_response(self, text: str) -> web.Response:
        """Returns a response with text/html content type."""
        return web.Response(text=text, content_type="text/html")

    @aiohttp_jinja2.template("index.html")
    async def index_handler(self, request: web.Request) -> dict:
        """
        Handles the / route
        params:
            request: The request object.
            returns: A dict with the data to be passed to the template.
        """
        return {
            "discord_version": discord_version,
            "bot_version": await self.client.get_bot_version(),
            "bot_latency": f"{self.client.get_bot_latency()}ms",
            "bot_uptime": self.client.get_uptime(),
        }

    async def webserver(self) -> None:
        """Starts the webserver."""
        app = web.Application()
        aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(self.path)))
        app.router.add_get("/", self.index_handler)
        runner = web.AppRunner(app)
        await runner.setup()
        self.site = web.TCPSite(runner, "0.0.0.0", self.client.config.port)
        await self.client.wait_until_ready()
        await self.site.start()

    def __unload(self):
        """Closes the webserver."""
        asyncio.ensure_future(self.site.stop())


async def setup(client):
    """Adds the cog to the bot."""
    server = WebServer(client)
    client.loop.create_task(server.webserver())
    await client.add_cog(WebServer(client))
