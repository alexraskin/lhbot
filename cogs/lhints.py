import random

import discord
from discord.ext import commands


class LhHint(commands.Cog, name="lhhint"):
    def __init__(self, bot):
        self.bot = bot
        self.hints = [
            "It is in English", "Made by 10 year old finnish lad", "Clever",
            "Masaa can be bribed", "It's not long hammer"
        ]

    @commands.command(name="lhhint")
    async def lh_hints(self, ctx):
        """
        random hint about the meaning of LH
        """
        embed = discord.Embed(description="LhHints", color=0x42F56C)
        random_hint = random.choice(list(self.hints))
        embed.set_author(name="Random LH Hint")
        embed.add_field(name="Hint:", value=random_hint, inline=False)
        embed.set_footer(text=f"Requested by {ctx.message.author}")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(LhHint(bot))
