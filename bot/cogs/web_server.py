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

def get_uptime(start_time):
    return str(datetime.timedelta(seconds=int(round(time.time() - start_time))))

class WebServer(commands.Cog, name="WebServer"):
    def __init__(self, client):
        self.client = client
        self.path = os.path.join(Path(__file__).resolve().parent, "static/")

    def html_response(self, text):
        return web.Response(text=text, content_type="text/html")

    @aiohttp_jinja2.template("index.html")
    async def index_handler(self, request):
        return {
          "discord_version": discord_version,
          "bot_version": self.client.version,
          "bot_latency": f"{round(self.client.latency * 1000)}ms",
          "bot_uptime": get_uptime(self.client.start_time),
          }

    async def webserver(self):

        app = web.Application()
        aiohttp_jinja2.setup(
            app, loader=jinja2.FileSystemLoader(str(self.path))
        )
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
