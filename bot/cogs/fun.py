import random
from typing import Union

from discord import Embed, Interaction, app_commands
from discord.ext import commands, tasks
from utils.bot_utils import get_time_string


class Fun(commands.Cog, name="Fun"):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.load_chuck_http_codes.start()
        self.headers = {"Accept": "application/json"}

    @tasks.loop(count=1)
    async def load_chuck_http_codes(self):
        response = await self.client.session.get(
            "https://api.chucknorris.io/jokes/categories"
        )
        categories = await response.json()
        self.chuck_categories = [x for x in categories if x != "explicit"]

    @app_commands.command()
    async def echo(self, interaction: Interaction, echo: str):
        await interaction.response.send_message(f"Echo: {echo}")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="chucknorris", aliases=["chuck", "cn"])
    async def chucknorris(self, ctx, category: str = None) -> Union[Embed, None]:
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
                color=random.randint(0, 0xFFFFFF),
                timestamp=ctx.message.created_at,
            )
            embed.set_author(
                name="Chuck Norris fun fact...",
                icon_url=f"https://assets.chucknorris.host/img/avatar/chuck-norris.png",
            )
            embed.set_footer(text=f"Category: {category} - https://api.chucknorris.io")
            await ctx.typing()
            await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="cat", aliases=["catpic", "catto"])
    async def cat(self, ctx):
        cat_url = "https://cataas.com"
        response = await self.client.session.get(f"{cat_url}/cat?json=true")
        data = await response.json()
        if response.status != 200:
            await ctx.send("Could not find a cat!")
            return
        else:
            await ctx.send(f"{cat_url}{data['url']}")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="dog", aliases=["dogpic", "doggo"])
    async def dog(self, ctx):
        """
        The dog function specifically gets a random dog picture from the website random.dog

        :param self: Used to access the client object.
        :param ctx: Used to get the channel and author of the message.
        :return: a dog picture in the form of a url.
        """
        response = await self.client.session.get("https://random.dog/woof.json")
        data = await response.json()
        if response.status != 200:
            await ctx.send("Could not find a dog!")
            return
        else:
            await ctx.send(data["url"])

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="meme", aliases=["memer"])
    async def get_meme(self, ctx):
        response = await self.client.session.get("https://meme-api.com/gimme")
        data = await response.json()
        if response.status != 200:
            await ctx.send("Could not find a meme!")
            return
        else:
            await ctx.send(data["url"])

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="joke", aliases=["dadjoke"])
    async def random_joke(self, ctx):
        response = await self.client.session.get("https://icanhazdadjoke.com/")
        response = await response.json()
        if response is None:
            await ctx.send("Could not find a joke!")
            return
        else:
            joke = response["joke"]
            embed = Embed(
                color=random.randint(0, 0xFFFFFF), timestamp=ctx.message.created_at
            )
            embed.add_field(name="Random Dad Joke", value=joke, inline=True)
            embed.set_footer(text=f"https://icanhazdadjoke.com/")
            await ctx.typing()
            await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="animechan", aliases=["animequote"])
    async def random_anime_chan(self, ctx) -> Union[Embed, None]:
        response = await self.client.session.get(
            "https://animechan.vercel.app/api/random"
        )
        response = await response.json()
        if response is None:
            await ctx.send("Could not find an anime quote!")
            return
        else:
            await ctx.typing()
            quote = str(response["quote"]).strip("[").strip("]")
            embed = Embed(
                color=random.randint(0, 0xFFFFFF), timestamp=ctx.message.created_at
            )
            embed.add_field(name="Quote", value=quote, inline=True)
            embed.set_footer(text=f"https://animechan.vercel.app/api/random")
            await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="waifu", aliases=["getwaifu"])
    async def random_waifu(self, ctx, category: str = None) -> Union[Embed, None]:
        random.seed(get_time_string())
        categories = ["waifu", "neko", "shinobu", "megumin", "bully", "cuddle"]
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
            await ctx.typing()
            url = response["url"]
            embed = Embed(
                color=random.randint(0, 0xFFFFFF), timestamp=ctx.message.created_at
            )
            embed.set_image(url=url)
            embed.set_footer(text=self.client.footer)
            await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(Fun(client))
