import logging

from discord import Embed
from discord.ext import commands


class Management(commands.Cog, name="Management"):
    def __init__(self, client: commands.Bot):
        self.client = client

    async def user_check(self, ctx: commands.Context):
        return self.client.user_is_superuser(ctx.author)

    @commands.Cog.listener()
    async def on_ready(self):
        self.cog_crawl()

    def cog_crawl(self):
        self.extension_targets = []
        for self.cog in self.client.abs_path:
            if self.cog.endswith(".py"):
                self.extension_targets.append(f"cogs.{self.cog[:-3]}")
        return self.extension_targets

    @commands.is_owner()
    @commands.command(name="sync", hidden=True)
    async def sync(self, ctx: commands.Context):
        tree = await self.client.tree.sync()
        await ctx.send(f"Synced slash commands. ```{tree}```")

    @commands.is_owner()
    @commands.command(name="reload", hidden=True)
    async def reload(self, ctx, extension=None):
        if extension is None:
            for cog in self.client.extensions.copy():
                await self.client.unload_extension(cog)
                await self.client.load_extension(cog)
            self.client.logger.info(f"Reload Command Executed by {ctx.author}")
            embed = Embed(
                title="Cog Reload 🔃",
                description="I have reloaded all the cogs successfully ✅",
                color=0x00FF00,
                timestamp=ctx.message.created_at,
            )
            embed.set_author(name="🤖 LhBot")
            embed.set_footer(text=self.client.footer)
            await ctx.send(embed=embed)
        else:
            self.client.logger.info(
                f"Reloaded: {str(extension).upper()} COG - Command Executed by {ctx.author}"
            )
            await self.client.unload_extension(f"cogs.{extension}")
            await self.client.load_extension(f"cogs.{extension}")
            embed = Embed(
                title="Cog Reload 🔃",
                description=f"I have reloaded the **{str(extension).upper()}** cog successfully ✅",
                color=0x00FF00,
                timestamp=ctx.message.created_at,
            )
            embed.set_author(name="🤖 LhBot")
            embed.set_footer(text=self.client.footer)
            await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(Management(client))
