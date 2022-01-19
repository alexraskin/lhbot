import json
import os
import sys

import discord
from discord.ext import commands

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json", encoding="utf-8") as file:
        config = json.load(file)


class LhCloudy(commands.Cog, name="lhcloudy"):
    """
    commands from twitch chat
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="1frame")
    async def one_frame(self, ctx):
        url = 'https://www.twitch.tv/lhcloudy27/clip/AbstruseKindRuffFutureMan-dLWae-FGvNag2jtK'
        embed = discord.Embed(color=0x42F56C)
        embed.add_field(
                    name="1Frame", value=url, inline=True
                )
        embed_message = await ctx.send(embed=embed)
        await embed_message.add_reaction("📼")
    
    @commands.command(name='360')
    async def three_sixty(self, ctx):
        url = "https://clips.twitch.tv/GentleObservantJalapenoLeeroyJenkins-Z53XsWoa2wamtAlB"
        embed = discord.Embed(color=0x42F56C)
        embed.add_field(
                    name="360", value=url, inline=True
                )
        embed_message = await ctx.send(embed=embed)
        await embed_message.add_reaction("📼")
    
    @commands.command(name="ball")
    async def ball(self, ctx):
        url = "https://gyazo.com/7f7dc8b93c4a77054104ee3d2ed9a134"
        embed = discord.Embed(color=0x42F56C)
        embed.add_field(
                    name="Ball", value=url, inline=True
                )
        embed_message = await ctx.send(embed=embed)
        await embed_message.add_reaction("📼")

    @commands.command(name="bhop")
    async def bhop(self, ctx):
        url = "https://www.twitch.tv/lhcloudy27/clip/ToughAttractiveHerbsBlargNaut-GvSHZicwk7Sjs13X"
        embed = discord.Embed(color=0x42F56C)
        embed.add_field(
                    name="bhop", value=url, inline=True
                )
        embed_message = await ctx.send(embed=embed)
        await embed_message.add_reaction("📼")

    @commands.command(name="bhop2")
    async def bhop_two(self, ctx):
        url = "https://clips.twitch.tv/BovineAverageChimpanzeeOpieOP-x5nayUCnonkU2OKc"
        embed = discord.Embed(color=0x42F56C)
        embed.add_field(
                    name="bhop2", value=url, inline=True
                )
        embed_message = await ctx.send(embed=embed)
        await embed_message.add_reaction("📼")
    
    @commands.command(name="climb")
    async def climb(self, ctx):
        text = "Hey Cloudy. I am a diamond level tank player with aspirations to climb higher.\
            I watch your streams every day in order to learn and get better.\
            Now after studying your gameplay and applying it I have tanked to bronze. Thanks and much love."
        embed = discord.Embed(color=0x42F56C)
        embed.add_field(
                    name="climb", value=text, inline=True
                )
        embed_message = await ctx.send(embed=embed)
        await embed_message.add_reaction("📼")
    
    @commands.command(name="code")
    async def code(self, ctx):
        text = "rein: XEEAE | other: https://workshop.codes/u/Seita%232315"
        embed = discord.Embed(color=0x42F56C)
        embed.add_field(
                    name="code", value=text, inline=True
                )
        embed_message = await ctx.send(embed=embed)
        await embed_message.add_reaction("📼")


def setup(bot):
    bot.add_cog(LhCloudy(bot))