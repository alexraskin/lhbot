from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from discord import Colour, Embed
from discord.ext import commands

if TYPE_CHECKING:
    from ..bot import LhBot


class LhCloudy(commands.Cog):
    def __init__(self, client: LhBot):
        self.client: LhBot = client

    @commands.hybrid_command(name="lhfurry", with_app_command=True)
    async def lhfurry(self, ctx: commands.Context) -> None:
        """
        LhCloudy's furry side
        """
        await ctx.send("https://i.gyazo.com/3ae8376713000ab829a2853d0f31e6f2.png")

    @commands.hybrid_command(name="code", aliases=["workshop"], with_app_command=True)
    async def code(self, ctx: commands.Context) -> None:
        """
        LhCloudy's workshop code
        """
        await ctx.send("rein: XEEAE | other: https://workshop.codes/u/Seita%232315")

    @commands.hybrid_command(name="egirl", with_app_command=True)
    async def egirl(self, ctx: commands.Context):
        """
        Egirl Quote
        """
        text = "hey big cwoudy man, cawn i pwease be uw egiww mewcy?"
        message = await ctx.send(text)
        await message.add_reaction("👉")
        await message.add_reaction("👈")
        await message.add_reaction("😌")

    @commands.hybrid_command(name="instagram", with_app_command=True)
    async def instagram(self, ctx: commands.Context):
        """
        Get a link to LhCloudy's Instagram
        """
        await ctx.send("https://www.instagram.com/lhcloudy/")

    @commands.hybrid_command(name="spotify", with_app_command=True)
    async def spotify(self, ctx: commands.Context):
        """
        Get a link to LhCloudy's Spotify Playlist
        """
        await ctx.send(
            "https://open.spotify.com/playlist/3JuA2BZjl0aZsEHKry1B67?si=14278d6ea4c04330"
        )

    @commands.hybrid_command(name="playlist", with_app_command=True)
    async def playlist(self, ctx: commands.Context):
        """
        Get a link to LhCloudy's Youtube Music Playlist
        """
        await ctx.send(
            "https://www.youtube.com/watch?v=p1SlBlB5pzU&list=RDHiu1hPdJk-Y&index=23"
        )

    @commands.hybrid_command(name="tips", with_app_command=True)
    async def tips(self, ctx: commands.Context):
        """
        Get a link to LhCloudy's Rein Tips
        """
        await ctx.send("W+M1")

    @commands.hybrid_command(name="twitter", with_app_command=True)
    async def twitter(self, ctx: commands.Context):
        """
        Get a link to LhCloudy's Twitter
        """
        await ctx.send("https://twitter.com/LhCloudy")

    @commands.hybrid_command(name="youtube", with_app_command=True)
    async def youtube(self, ctx: commands.Context):
        """
        Get a link to LhCloudy's Youtube Channel
        """
        url = "SMÄSH THAT LIKE AND SUBSCRIBE BUTTON -> https://www.youtube.com/channel/UC2CV-HWvIrMO4mUnYtNS-7A"
        await ctx.send(url)

    @commands.hybrid_command(name="age", aliases=["oldman"], with_app_command=True)
    async def age(self, ctx: commands.Context):
        """
        Get LhCloudy's age
        """
        td = datetime.datetime.now().date()
        bd = datetime.date(1999, 5, 21)
        age_years = int((td - bd).days / 365.25)
        await ctx.send(content=str(age_years))

    @commands.hybrid_command(name="birthday", with_app_command=True)
    async def birthday(self, ctx: commands.Context):
        """
        Get days until next birthday
        """
        birthday_str = "21.5.1999"
        birthday = datetime.datetime.strptime(birthday_str, "%d.%m.%Y").date()

        today = datetime.date.today()
        current_year_birthday = birthday.replace(year=today.year)
        next_birthday = current_year_birthday

        if today > current_year_birthday:
            next_birthday = birthday.replace(year=today.year + 1)

        days_until_next_birthday = (next_birthday - today).days

        if days_until_next_birthday == 0:
            await ctx.send("Today is Cloudy's birthday! 🎉")
            await ctx.send("https://tenor.com/bmYbD.gif")
        else:
            await ctx.send(
                f"There are {days_until_next_birthday} days until Cloudy's birthday."
            )

    @commands.hybrid_command(name="from", with_app_command=True)
    async def from_(self, ctx: commands.Context):
        """
        Where is LhCloudy from?
        """
        await ctx.send("kotka of south eastern finland of the continent of europe")

    @commands.hybrid_command(name="links", aliases=["urls"], with_app_command=True)
    async def links(self, ctx: commands.Context) -> None:
        """
        List of LhCloudy's links
        """
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

    @commands.hybrid_command(name="fact", with_app_command=True)
    async def fact(self, ctx: commands.Context) -> None:
        """
        A fact about LhCloudy
        """
        f = """On February 23, 2021, LhCloudy hit rank 1 tank on both the North American and European ladders, although very briefly, playing only Reinhardt. 
            He achieved this again on February 26th for a longer, but still brief period. 
            It’s considered an achievement because the game's meta at the time was very unfriendly towards Reinhardt. 
            To mitigate this, he played a unique playstyle centered around clearing angles and taking high grounds.
            """
        await ctx.send(f)

    @commands.hybrid_command(name="interview", with_app_command=True)
    async def interview(self, ctx: commands.Context):
        """
        LhCloudy's interview
        """
        await ctx.send("https://www.youtube.com/watch?v=sM_PkcoFgM8&t=1s")

    @commands.hybrid_command(name="photo", with_app_command=True)
    async def photo(self, ctx: commands.Context):
        """
        LhCloudy's photo
        """
        await ctx.send(
            "https://liquipedia.net/commons/images/e/e8/ENCE_LhCloudy_2024.jpg"
        )

    @commands.hybrid_command(name="about", with_app_command=True)
    async def about(self, ctx: commands.Context):
        """
        About LhCloudy
        """
        await ctx.send(
            "Roni 'LhCloudy' Tiihonen (born May 21, 1999) is a Finnish player who is currently playing for [ENCE](https://liquipedia.net/overwatch/ENCE)"
        )

    @commands.hybrid_command(name="satu", with_app_command=True)
    async def satu(self, ctx: commands.Context):
        """
        Satu
        """
        await ctx.send("https://imgur.com/a/C4uAiHK")


async def setup(client: LhBot):
    await client.add_cog(LhCloudy(client))
