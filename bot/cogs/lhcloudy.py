import datetime
import sys

from discord import Embed, Colour
from discord.ext import commands


class LhCloudy(commands.Cog, name="LhCloudy"):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.hybrid_group(invoke_without_command=True)
    async def twitch(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(
                f"Please use `{self.client.config.bot_prefix}twitch help` to see the list of commands."
            )

    @twitch.command(name="lhfurry", with_app_command=True)
    async def lhfurry(self, ctx: commands.Context):
        await ctx.send("https://i.gyazo.com/3ae8376713000ab829a2853d0f31e6f2.png")

    @twitch.command(name="code", aliases=["workshop"], with_app_command=True)
    async def code(self, ctx: commands.Context):
        await ctx.send("rein: XEEAE | other: https://workshop.codes/u/Seita%232315")

    @twitch.command(name="egirl", with_app_command=True)
    async def egirl(self, ctx: commands.Context):
        text = "hey big cwoudy man, cawn i pwease be uw egiww mewcy?"
        message = await ctx.send(text)
        await message.add_reaction("👉")
        await message.add_reaction("👈")
        await message.add_reaction("😌")

    @twitch.command(name="instagram", with_app_command=True)
    async def instagram(self, ctx: commands.Context):
        await ctx.send("https://www.instagram.com/lhcloudy/")

    @twitch.command(name="spotify", with_app_command=True)
    async def spotify(self, ctx: commands.Context):
        await ctx.send(
            "https://open.spotify.com/playlist/3JuA2BZjl0aZsEHKry1B67?si=14278d6ea4c04330"
        )

    @twitch.command(name="playlist", with_app_command=True)
    async def playlist(self, ctx: commands.Context):
        await ctx.send(
            "https://www.youtube.com/watch?v=p1SlBlB5pzU&list=RDHiu1hPdJk-Y&index=23"
        )

    @twitch.command(name="srpeak", with_app_command=True)
    async def srpeak(self, ctx: commands.Context):
        text = (
            "I saw Cloudy in a 4K lobby one time. "
            + "I told him how cool it was to meet him in game, "
            + "but I didn’t want to be a douche and bother him and "
            + "ask him for friend request or anything. He said, "
            + "“Oh, sr peak check?” I was taken aback, and all I could say was “Huh?” "
            + "but he kept cutting me off and going “huh? huh? huh?” "
            + "while using the “No” voiceline repeatedly."
        )
        await ctx.send(text)

    @twitch.command(name="tips", with_app_command=True)
    async def tips(self, ctx: commands.Context):
        await ctx.send("W+M1")

    @twitch.command(name="twitter", with_app_command=True)
    async def twitter(self, ctx: commands.Context):
        await ctx.send("https://twitter.com/LhCloudy")

    @twitch.command(name="youtube", with_app_command=True)
    async def youtube(self, ctx: commands.Context):
        url = "SMÄSH THAT LIKE AND SUBSCRIBE BUTTON -> https://www.youtube.com/channel/UC2CV-HWvIrMO4mUnYtNS-7A"
        await ctx.send(url)

    @twitch.command(name="age", aliases=["oldman"], with_app_command=True)
    async def age(self, ctx: commands.Context):
        td = datetime.datetime.now().date()
        bd = datetime.date(1999, 5, 21)
        age_years = int((td - bd).days / 365.25)
        await ctx.send(age_years)

    @twitch.command(name="from", with_app_command=True)
    async def from_(self, ctx: commands.Context):
        await ctx.send("kotka of south eastern finland of the continent of europe")

    @twitch.command(name="links", aliases=["urls"], with_app_command=True)
    async def links(self, ctx: commands.Context):
        links = (
            "• Twitch <https://www.twitch.tv/lhcloudy27>"
            "\n• Youtube: <https://www.youtube.com/channel/UC2CV-HWvIrMO4mUnYtNS-7A>"
            + "\n• Discord: <https://discord.gg/jd6CZSj8jb>"
            + "\n• Twitter: <https://twitter.com/LhCloudy>"
            + "\n• Instagram: <https://www.instagram.com/lhcloudy/>"
            + "\n• Reddit: <https://www.reddit.com/r/overwatchSRpeakCHECK/>"
        )
        embed = Embed(title="LhCloudy Links", description=links)
        embed.colour = Colour.blurple()
        await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(LhCloudy(client))
