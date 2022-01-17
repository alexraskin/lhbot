import json
import os
import platform
import random
import sys

import discord
from discord.ext import commands

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)


class general(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="info", aliases=["botinfo"])
    async def info(self, ctx):
        """
        information about the bot
        """
        embed = discord.Embed(description="LhBot", color=0x42F56C)
        embed.set_author(name="Bot Information")
        embed.add_field(name="Owner:", value="reinfrog#1738", inline=True)
        embed.add_field(name="Prefix:",
                        value=f"{config['bot_prefix']}",
                        inline=True)
        embed.add_field(name="Python Version:",
                        value=f"{platform.python_version()}",
                        inline=True)
        embed.add_field(name="URL:",
                        value="https://github.com/alexraskin/lhbot",
                        inline=True)
        await ctx.send(embed=embed)

    @commands.command(name="ping")
    async def ping(self, ctx):
        """
        ping the bot
        """
        embed = discord.Embed(
            title="🏓 Pong!",
            description=
            f"The bot latency is {round(self.bot.latency * 1000)}ms.",
            color=0x42F56C)
        embed.set_footer(text=f"Requested by {ctx.message.author}")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(general(bot))
