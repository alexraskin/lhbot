import asyncio

from aiohttp import web
from discord.ext import commands


class WebServer(commands.Cog, name="WebServer"):
    def __init__(self, client):
        self.client = client

    async def webserver(self):
        async def handler(request):
            return web.json_response({"message": "Hello, world"})

        app = web.Application()
        app.router.add_get("/", handler)
        runner = web.AppRunner(app)
        await runner.setup()
        self.site = web.TCPSite(runner, "0.0.0.0", 8000)
        await self.client.wait_until_ready()
        await self.site.start()

    def __unload(self):
        asyncio.ensure_future(self.site.stop())


async def setup(client):
    server = WebServer(client)
    client.loop.create_task(server.webserver())
    await client.add_cog(WebServer(client))
