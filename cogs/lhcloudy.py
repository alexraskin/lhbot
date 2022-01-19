import json
import os
import sys
import random

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

    @staticmethod
    def random_emoji():
        emoji_list = [
            "😁",
            "🥶",
            "👌",
            "👀",
            "🤖",
            "👽",
            "💀",
            "🤯",
            "🤠",
            "📼",
            "📈",
            "🧡",
            "✨"
        ]
        return random.choice(list(emoji_list))

    @commands.command(name="1frame")
    async def one_frame(self, ctx):
        url = "https://www.twitch.tv/lhcloudy27/clip/AbstruseKindRuffFutureMan-dLWae-FGvNag2jtK"
        message = await ctx.send(url)
        await message.add_reaction(LhCloudy.random_emoji())

    @commands.command(name="360")
    async def three_sixty(self, ctx):
        url = "https://clips.twitch.tv/GentleObservantJalapenoLeeroyJenkins-Z53XsWoa2wamtAlB"
        message = await ctx.send(url)
        await message.add_reaction(LhCloudy.random_emoji())

    @commands.command(name="ball")
    async def ball(self, ctx):
        url = "https://gyazo.com/7f7dc8b93c4a77054104ee3d2ed9a134"
        message = await ctx.send(url)
        await message.add_reaction(LhCloudy.random_emoji())

    @commands.command(name="bhop")
    async def bhop(self, ctx):
        url = "https://www.twitch.tv/lhcloudy27/clip/ToughAttractiveHerbsBlargNaut-GvSHZicwk7Sjs13X"
        message = await ctx.send(url)
        await message.add_reaction(LhCloudy.random_emoji())

    @commands.command(name="bhop2")
    async def bhop_two(self, ctx):
        url = "https://clips.twitch.tv/BovineAverageChimpanzeeOpieOP-x5nayUCnonkU2OKc"
        message = await ctx.send(url)
        await message.add_reaction(LhCloudy.random_emoji())

    @commands.command(name="climb")
    async def climb(self, ctx):
        text = """Hey Cloudy. I am a diamond level tank player with aspirations to climb higher. I watch your streams every day in order to learn and get better. Now after studying your gameplay and applying it I have tanked to bronze. Thanks and much love."""
        message = await ctx.send(text)
        await message.add_reaction(LhCloudy.random_emoji())

    @commands.command(name="code")
    async def code(self, ctx):
        text = "rein: XEEAE | other: https://workshop.codes/u/Seita%232315"
        message = await ctx.send(text)
        await message.add_reaction(LhCloudy.random_emoji())

    @commands.command(name="dva")
    async def dva(self, ctx):
        url = "https://www.twitch.tv/lhcloudy27/clip/SmokyDifferentCobblerDoggo-rY6mWkS8b2Jj5kDm"
        message = await ctx.send(url)
        await message.add_reaction(LhCloudy.random_emoji())
    
    @commands.command(name="dva2")
    async def dva(self, ctx):
        url = "	https://clips.twitch.tv/WanderingLuckyClipzBrainSlug-0x2XxJjniDP_SSeX"
        message = await ctx.send(url)
        await message.add_reaction(LhCloudy.random_emoji())
    
    @commands.command(name="dva2")
    async def dva(self, ctx):
        url = "	https://clips.twitch.tv/ThirstySavageMinkAsianGlow-drRcT2-cwpRSx2gE"
        message = await ctx.send(url)
        await message.add_reaction(LhCloudy.random_emoji())

    @commands.command(name="egirl")
    async def dva(self, ctx):
        text = "hey big cwoudy man, cawn i pwease be uw egiww mewcy?"
        message = await ctx.send(text)
        await message.add_reaction("👉")
        await message.add_reaction("👈")
        await message.add_reaction("😌")



def setup(bot):
    bot.add_cog(LhCloudy(bot))
