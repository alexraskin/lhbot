from __future__ import annotations

import logging

from discord import Embed
from discord.ext import commands


class Management(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.is_owner()
    @commands.command(name="sync", hidden=True)
    async def sync(self, ctx: commands.Context):
        message = await ctx.send("Syncing slash commands... 🔄")
        await self.client.tree.sync()
        await message.edit(content="Synced slash commands successfully! ✅")

    @commands.is_owner()
    @commands.command(name="reload", hidden=True)
    async def reload(self, ctx, extension=None):
        if extension is None:
            for cog in self.client.extensions.copy():  # type: ignore
                await self.client.unload_extension(cog)
                await self.client.load_extension(cog)
            self.client.logger.info(f"Reload Command Executed by {ctx.author}")  # type: ignore
            embed = Embed(
                title="Cog Reload 🔃",
                description="I have reloaded all the cogs successfully ✅",
                color=0x00FF00,
                timestamp=ctx.message.created_at,
            )
            embed.set_author(name="🤖 LhBot")
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
            await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(Management(client))
