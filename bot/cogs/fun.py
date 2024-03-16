from __future__ import annotations

import random
from typing import Union, TYPE_CHECKING

from discord import Colour, Embed, app_commands
from discord.ext import commands, tasks
from utils import bot_utils

if TYPE_CHECKING:
    from ..bot import LhBot


class Fun(commands.Cog):
    def __init__(self, client: LhBot):
        self.client: LhBot = client
        self.load_chuck_http_codes.start()
        self.headers = {"Accept": "application/json"}

    @tasks.loop(count=1)
    async def load_chuck_http_codes(self) -> None:
        response = await self.client.session.get(
            "https://api.chucknorris.io/jokes/categories"
        )
        categories = await response.json()
        self.chuck_categories = [x for x in categories if x != "explicit"]

    @commands.hybrid_command(with_app_command=True)
    @commands.guild_only()
    @app_commands.guild_only()
    @app_commands.describe(category="Category of Chuck Norris fact")
    async def chucknorris(
        self, ctx: commands.Context, category: str = None
    ) -> Union[Embed, None]:
        """
        Get a random Chuck Norris fact
        """
        if not hasattr(self, "chuck_categories"):
            await ctx.send("Hold up partner, still locating Chuck!")
            return
        if category is None:
            category = random.choice(self.chuck_categories)
        else:
            if category not in self.chuck_categories:
                await ctx.send(
                    f'```Invalid category - please pick from:\n{", ".join(self.chuck_categories)}```'
                )
                return
        response = await self.client.session.get(
            f"https://api.chucknorris.io/jokes/random?category={category}"
        )
        if response is None:
            await ctx.send("Hold up partner, still locating Chuck!")
            return
        else:
            response = await response.json()
            chuck = response["value"]
            embed = Embed(
                description=chuck,
                timestamp=ctx.message.created_at,
            )
            embed.colour = Colour.blurple()
            embed.set_author(
                name="Chuck Norris fun fact...",
                icon_url=f"https://assets.chucknorris.host/img/avatar/chuck-norris.png",
            )
            embed.set_footer(text=f"Category: {category} - https://api.chucknorris.io")
            await ctx.send(embed=embed)

    @commands.hybrid_command(with_app_command=True)
    @commands.guild_only()
    @app_commands.guild_only()
    async def cat(self, ctx: commands.Context):
        """
        Get a random cat from cataas.com
        """
        cat_url = "https://cataas.com"
        response = await self.client.session.get(f"{cat_url}/cat?json=true")
        data = await response.json()
        if response.status != 200:
            await ctx.send("Could not find a cat!")
            return
        else:
            await ctx.send(f"{cat_url}/cat/{data['_id']}")

    @commands.hybrid_command(
        name="dog", aliases=["dogpic", "doggo"], with_app_command=True
    )
    @commands.guild_only()
    @app_commands.guild_only()
    async def dog(self, ctx: commands.Context):
        """
        Get a random dog from random.dog
        """
        response = await self.client.session.get("https://random.dog/woof.json")
        data = await response.json()
        if response.status != 200:
            await ctx.send("Could not find a dog!")
            return
        else:
            await ctx.send(data["url"])

    @commands.hybrid_command(name="meme", aliases=["memer"], with_app_command=True)
    @commands.guild_only()
    @app_commands.guild_only()
    async def get_meme(self, ctx: commands.Context):
        """
        Get a random meme from meme-api.com
        """
        response = await self.client.session.get("https://meme-api.com/gimme")
        data = await response.json()
        if response.status != 200:
            await ctx.send("Could not find a meme!")
            return
        else:
            await ctx.send(data["url"])

    @commands.hybrid_command(name="joke", aliases=["dadjoke"], with_app_command=True)
    @commands.guild_only()
    @app_commands.guild_only()
    async def random_joke(self, ctx: commands.Context):
        """
        Get a random dad joke from icanhazdadjoke.com
        """
        response = await self.client.session.get(
            "https://icanhazdadjoke.com/", headers={"Accept": "application/json"}
        )
        response = await response.json()
        if response is None:
            await ctx.send("Could not find a joke!")
            return
        else:
            joke = response["joke"]
            embed = Embed(timestamp=ctx.message.created_at)
            embed.colour = Colour.blurple()
            embed.add_field(name="Random Dad Joke", value=joke, inline=True)
            embed.set_footer(text=f"https://icanhazdadjoke.com/")
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="waifu", aliases=["getwaifu"], with_app_command=True)
    @commands.guild_only()
    @app_commands.guild_only()
    async def random_waifu(
        self, ctx: commands.Context, category: str = None
    ) -> Union[Embed, None]:
        """
        Get a random waifu from waifu.pics
        """
        random.seed(get_time_string())
        categories = ["cuddle", "cry", "hug", "awoo", "kiss"]
        if category is None:
            category = random.choice(categories)
        else:
            if category not in categories:
                await ctx.send(
                    f'Invalid category - please pick from:\n{", ".join(categories)}'
                )
                return
        response = await self.client.session.get(
            f"https://api.waifu.pics/sfw/{category}"
        )
        response = await response.json()
        if response is None:
            await ctx.send("No waifu for you!")
            return
        else:
            url = response["url"]
            embed = Embed(timestamp=ctx.message.created_at)
            embed.colour = Colour.blurple()
            embed.set_image(url=url)
            embed.set_footer(text=f"https://waifu.pics/")
            await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="year", aliases=["yearprogress"], with_app_command=True
    )
    @commands.guild_only()
    @app_commands.guild_only()
    async def year(self, ctx: commands.Context):
        """
        Get the progress of the year
        """
        embed = Embed(timestamp=ctx.message.created_at)
        embed.colour = Colour.blurple()
        embed.set_author(
            name="Year Progress",
            icon_url="https://i.gyazo.com/db74b90ebf03429e4cc9873f2990d01e.png",
        )
        embed.add_field(
            name="Progress:",
            value=bot_utils.progress_bar(bot_utils.get_year_round()),
            inline=True,
        )
        await ctx.send(embed=embed)


async def setup(client: LhBot):
    await client.add_cog(Fun(client))
