from os import listdir
from discord.ext import commands
import logging

class Management(commands.Cog, name='Management'):
    def __init__(self, client):
        self.client = client

    async def user_check(self, ctx):
        return self.client.user_is_superuser(ctx.author)
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.cog_crawl()
    
    def cog_crawl(self):
        self.extension_targets = []
        for self.cog in listdir("./bot/cogs"):
            if self.cog.endswith(".py"):
                self.extension_targets.append(f"cogs.{self.cog[:-3]}")
        return self.extension_targets

    @commands.command(
        name='reload',
        brief='Reload bot extension',
        description='Reload bot extension\n\nExample: lhbot reload cogs.stats',
        hidden=True,
        aliases=['re']
    )
    async def reload_extension(self, ctx, extension) -> None:
        try: 
            if f"cogs.{extension}" in self.extension_targets:
                await self.client.reload_extension(f"cogs.{extension}")
                await ctx.send(f"```Reloaded [{extension}] cog```")
            else:
                await ctx.send(f"```Extension [{extension}] cog not found```")
        except Exception as error:
            exc = f"{type(error).__name__}: {error}"
            logging.error(f"Failed to reload extension {extension}\n{exc}")
            await ctx.send(f"```Failed to reload [{extension}] cog```")


async def setup(client):
    await client.add_cog(Management(client))