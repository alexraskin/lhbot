import random
import sys
from typing import Union
from functools import lru_cache

from discord import Embed
from discord.ext import commands, tasks
from sentry_sdk import capture_exception

sys.path.append("../bot")
from config import Settings

@lru_cache()
def settings():
    return Settings()


conf = settings()


class Fun(commands.Cog, name="Fun"):
    def __init__(self, client):
        """
        The __init__ function is the constructor for a class.
        It initializes the attributes of an object.
        In this case, it initializes the client attribute.

        :param self: Used to access variables that belong to the class.
        :param client: Used to pass in the client object to the class.
        :return: a class instance and sets up the client.
        """
        self.client = client
        self.load_chuck_http_codes.start()
        self.headers = {"Accept": "application/json"}
    
    async def fetch_url(self, url: str) -> Union[dict, None]:
        """
        The fetch_url function is used to fetch the url and return the response.

        :param url: url to get
        :return: the response from the url.
        """
        try:
            async with self.client.session.get(url, headers=self.headers) as response:
                response = await response.json()
                return response
        except BaseException as error:
            capture_exception(error)
            return None

    @tasks.loop(count=1)
    async def load_chuck_http_codes(self):
        """
        The load_chuck_http_codes function specifically loads the
        categories from the Chuck Norris API and stores them in a list.

        :param self: Used to store the bot object.
        :return: a list of categories.
        """
        response = await self.fetch_url("https://api.chucknorris.io/jokes/categories")
        self.chuck_categories = [x for x in response if x != "explicit"]

    @commands.command(name="chucknorris", aliases=["chuck", "cn"])
    async def chucknorris(self, ctx, category: str = None):
        """
        The chucknorris function is a command that allows the user to get a random chuck norris fact.
        The function takes in an optional argument, category, which can be any of the following:
            -   "animal"
            -   "career"
            -   "celebrity"

        :param self: Used to access attributes of the class.
        :param ctx: Used to get the channel and user that sent the command.
        :param category:str=None: Used to determine if the user has specified a category or not.
        :return: a random chuck norris fact from the API.
        """
        if not hasattr(self, "chuck_categories"):
            raise commands.BadArgument("Hold up partner, still locating Chuck!")

        if category is None:
            category = random.choice(self.chuck_categories)
        else:
            if category not in self.chuck_categories:
                raise commands.BadArgument(
                    f'Invalid category - please pick from:\n{", ".join(self.chuck_categories)}'
                )
        response = await self.fetch_url("https://api.chucknorris.io/jokes/random?category={category}")
        if response is None:
            raise commands.BadArgument("Hold up partner, still locating Chuck!")
        else:
            chuck = response["value"]
            embed = Embed(description=chuck, color=random.randint(0, 0xFFFFFF))
            embed.set_author(
                name="Chuck Norris fun fact...",
                icon_url=f"https://assets.chucknorris.host/img/avatar/chuck-norris.png",
            )
            embed.set_footer(
                text=f"Category: {category} - https://api.chucknorris.io"
            )
            await ctx.trigger_typing()
            await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="cat", aliases=["catpic", "catto"])
    async def cat(self, ctx):
        """
        The cat function specifically gets a random cat picture from the random.cat API and sends it to the channel.

        :param self: Used to access the client and other variables in this cog.
        :param ctx: Used to get the context of where the command was called.
        :return: a random cat picture from the random.
        """
        response = await self.fetch_url("https://aws.random.cat/meow")
        if response is None:
            raise commands.BadArgument("Could not find a cat!")
        else:
            await ctx.send(response["file"])

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="dog", aliases=["dogpic", "doggo"])
    async def dog(self, ctx):
        """
        The dog function specifically gets a random dog picture from the website random.dog

        :param self: Used to access the client object.
        :param ctx: Used to get the channel and author of the message.
        :return: a dog picture in the form of a url.
        """
        response = await self.fetch_url("https://random.dog/woof.json")
        if response is None:
            raise commands.BadArgument("Could not find a dog!")
        else:
            await ctx.send(response["url"])

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="meme", aliases=["memer"])
    async def get_meme(self, ctx):
        """
        The get_meme function specifically gets a random meme from the reddit api and returns it to the user

        :param self: Used to access the client object.
        :param ctx: Used to access the context of where the command was called.
        :return: the link to the meme from reddit.
        """
        response = await self.fetch_url("https://meme-api.herokuapp.com/gimme")
        if response is None:
            raise commands.BadArgument("Could not find a meme!")
        else:
            await ctx.send(response["url"])

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="kanye", aliases=["kw", "kanyewest"])
    async def get_kayne_west(self, ctx):

        """
        The get_kayne_west function specifically retrieves a random quote from the Kanye API and embeds it in a message.

        :param self: Used to access the client, which is needed to send messages.
        :param ctx: Used to get the context of where the command was called.
        :return: a random quote from Kanye West.
        """
        response = await self.fetch_url("https://api.kanye.rest")
        await ctx.trigger_typing()
        if response is None:
            raise commands.BadArgument("Kayne is busy!")
        else:
            quote = response["quote"]
            embed = Embed(color=random.randint(0, 0xFFFFFF))
            embed.add_field(
                name="Kayne West once said:", value=f'{quote}', inline=True
            )
            embed.set_image(url="https://c.tenor.com/73vhftW9zYMAAAAC/kanye-west-blink.gif")
            embed.set_footer(
                text=f"https://api.kanye.rest"
            )
            await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="catfact", aliases=["cf"])
    async def random_cat_fact(self, ctx):
        """
        The random_cat_fact function specifically retrieves a random cat fact
        from the meowfacts.herokuapp.com website and embeds it into an Embed object.

        :param self: Used to access the attributes and methods of your cog.
        :param ctx: Used to get the context of where the command was called.
        :return: a random cat fact from the MeowFact API.
        """
        response = await self.fetch_url("https://meowfacts.herokuapp.com/")
        await ctx.trigger_typing()
        if response is None:
            raise commands.BadArgument("Could not find a cat fact!")
        else:
            fact = response["data"]
            embed = Embed(color=random.randint(0, 0xFFFFFF))
            embed.add_field(
                name="Random Cat Fact:",
                value=str(fact).strip("[]").strip("'"),
                inline=True,
            )
            embed.set_footer(
                text=f"https://meowfacts.herokuapp.com/"
            )
            await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="joke", aliases=["dadjoke"])
    async def random_joke(self, ctx):
        """
        The random_joke function specifically retrieves a random joke from the icanhazdadjoke.

        :param self: Used to access the client and its functions.
        :param ctx: Used to get the context of where the command was called.
        :return: the joke from the icnhazdadjoke.
        """
        response = await self.fetch_url("https://icanhazdadjoke.com/")
        if response is None:
            raise commands.BadArgument("Could not find a joke!")
        else:
            joke = response["joke"]
            embed = Embed(color=random.randint(0, 0xFFFFFF))
            embed.add_field(name="Random Dad Joke", value=joke, inline=True)
            embed.set_footer(
                text=f"https://icanhazdadjoke.com/"
            )
            await ctx.trigger_typing()
            await ctx.send(embed=embed)

    @commands.command(name="animechan", aliases=["animequote"])
    async def random_anime_chan(self, ctx):
        """
        The random anime chan function specifically retrieves a random anime quote from an API.

        :param self: Used to access the client variable in this class.
        :param ctx: Used to get the context of where the command was called.
        :return: an embed that has the anime, character and quote of a random anime.
        """
        response = await self.fetch_url("https://animechan.herokuapp.com/api/random")
        if response is None:
            raise commands.BadArgument("Could not find an anime quote!")
        else:
            await ctx.trigger_typing()
            anime = response["anime"]
            character = response["character"]
            quote = str(response["quote"]).strip("[").strip("]")
            embed = Embed(title="Random Anime Quote", color=random.randint(0, 0xFFFFFF))
            embed.add_field(name="Anime:", value=anime, inline=True)
            embed.add_field(name="Character:", value=character, inline=True)
            embed.add_field(name="Quote:", value=quote, inline=True)
            embed.set_footer(text=f"https://animechan.herokuapp.com/api/random")
            await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="dogfact", aliases=["df"])
    async def random_dog_fact(self, ctx):
        """
        The random_dog_fact function retrieves a random dog fact
        from the Dog Fact API and embeds it in an Embed object.

        :param self: Used to access the client, which is used to access the bot's commands.
        :param ctx: Used to access the context of where the command was called.
        :return: discord embed
        """
        response = await self.fetch_url("https://dog-fact-api.herokuapp.com/api/v1/resources/dogs?number=1")
        if response is None:
            raise commands.BadArgument("Could not find a dog fact!")
        else:
            await ctx.trigger_typing()
            fact = response[0]["fact"]
            embed = Embed(color=random.randint(0, 0xFFFFFF))
            embed.add_field(name="Random Dog Fact:", value=fact, inline=True)
            embed.set_footer(text=f"https://dog-fact-api.herokuapp.com")
            await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="tswift", aliases=["ts", "taylor", "taylorswift"])
    async def random_taylor_swift_quote(self, ctx):
        """ """
        response = await self.fetch_url("https://taylorswiftapi.herokuapp.com/get")
        if response is None:
            raise commands.BadArgument("Problem getting a Taylor Swift quote!")
        else:
            await ctx.trigger_typing()
            quote = response["quote"]
            embed = Embed(color=random.randint(0, 0xFFFFFF))
            embed.set_author(
                name="Taylor Swift",
                icon_url=f"https://i.gyazo.com/97cd0059f957bf80d01672bdfe258357.png",
            )
            embed.add_field(name="Quote:", value=quote, inline=True)
            embed.set_image(url="https://c.tenor.com/DDIYEFpaAboAAAAC/taylor-swift-dance.gif")
            embed.set_footer(text=f"https://taylorswiftapi.herokuapp.com")
            await ctx.send(embed=embed)


def setup(client):
    """
    The setup function is used to register the commands that will be used in the bot.
    This function is run when you load a cog, and it allows you to use commands in your cogs.

    :param client: Used to pass in the discord.
    :return: the client object which is your entry point to the API.

    """
    client.add_cog(Fun(client))
