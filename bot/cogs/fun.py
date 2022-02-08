import random

from discord import Embed
from discord.ext import commands, tasks
from sentry_sdk import capture_exception


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

    @tasks.loop(count=1)
    async def load_chuck_http_codes(self):
        """
        The load_chuck_http_codes function specifically loads the
        categories from the Chuck Norris API and stores them in a list.

        :param self: Used to store the bot object.
        :return: a list of categories.
        """
        async with self.client.session.get(
            "https://api.chucknorris.io/jokes/categories"
        ) as response:
            categories = await response.json()
            self.chuck_categories = [x for x in categories if x != "explicit"]

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
        try:
            async with self.client.session.get(
                f"https://api.chucknorris.io/jokes/random?category={category}"
            ) as response:
                chuck = await response.json()
                chuck = chuck["value"]
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

        except BaseException as e:
            capture_exception(e)
            raise commands.BadArgument(
                "Chuck not found, currently evading GPS in Texas!"
            )

    @commands.command(name="cat", aliases=["catpic", "catto"])
    async def cat(self, ctx):
        """
        The cat function specifically gets a random cat picture from the random.cat API and sends it to the channel.

        :param self: Used to access the client and other variables in this cog.
        :param ctx: Used to get the context of where the command was called.
        :return: a random cat picture from the random.
        """
        async with self.client.session.get("https://aws.random.cat/meow") as response:
            cat = await response.json()
            cat_photo = cat["file"]
            await ctx.send(cat_photo)

    @commands.command(name="dog", aliases=["dogpic", "doggo"])
    async def dog(self, ctx):
        """
        The dog function specifically gets a random dog picture from the website random.dog

        :param self: Used to access the client object.
        :param ctx: Used to get the channel and author of the message.
        :return: a dog picture in the form of a url.
        """
        async with self.client.session.get("https://random.dog/woof.json") as response:
            dog = await response.json()
            dog_photo = dog["url"]

            await ctx.send(dog_photo)

    @commands.command(name="meme", aliases=["memer"])
    async def get_meme(self, ctx):
        """
        The get_meme function specifically gets a random meme from the reddit api and returns it to the user

        :param self: Used to access the client object.
        :param ctx: Used to access the context of where the command was called.
        :return: the link to the meme from reddit.
        """
        async with self.client.session.get(
            "https://meme-api.herokuapp.com/gimme"
        ) as response:
            data = await response.json()
            meme = data["url"]

            await ctx.send(meme)

    @commands.command(name="kanye", aliases=["kw", "kanyewest"])
    async def get_kayne_west(self, ctx):

        """
        The get_kayne_west function specifically retrieves a random quote from the Kanye API and embeds it in a message.

        :param self: Used to access the client, which is needed to send messages.
        :param ctx: Used to get the context of where the command was called.
        :return: a random quote from Kanye West.
        """
        async with self.client.session.get("https://api.kanye.rest/") as response:
            data = await response.json()
            quote = data["quote"]
            embed = Embed(color=random.randint(0, 0xFFFFFF))
            embed.add_field(
                name="Random Kayne Quote:", value=f'"{quote}" - Kayne West', inline=True
            )
            await ctx.trigger_typing()
            await ctx.send(embed=embed)

    @commands.command(name="catfact", aliases=["cf"])
    async def random_cat_fact(self, ctx):
        """
        The random_cat_fact function specifically retrieves a random cat fact
        from the meowfacts.herokuapp.com website and embeds it into an Embed object.

        :param self: Used to access the attributes and methods of your cog.
        :param ctx: Used to get the context of where the command was called.
        :return: a random cat fact from the MeowFact API.
        """

        async with self.client.session.get(
            "https://meowfacts.herokuapp.com/"
        ) as response:
            data = await response.json()
            fact = data["data"]
            embed = Embed(color=random.randint(0, 0xFFFFFF))
            embed.add_field(
                name="Random Cat Fact:",
                value=str(fact).strip("[]").strip("'"),
                inline=True,
            )
            await ctx.trigger_typing()
            await ctx.send(embed=embed)

    @commands.command(name="joke", aliases=["dadjoke"])
    async def random_joke(self, ctx):
        """
        The random_joke function specifically retrieves a random joke from the icanhazdadjoke.

        :param self: Used to access the client and its functions.
        :param ctx: Used to get the context of where the command was called.
        :return: the joke from the icnhazdadjoke.
        """
        headers = {"Accept": "application/json"}
        async with self.client.session.get(
            "https://icanhazdadjoke.com/", headers=headers
        ) as response:
            data = await response.json()
            joke = data["joke"]
            embed = Embed(color=random.randint(0, 0xFFFFFF))
            embed.add_field(name="Random Dad Joke", value=joke, inline=True)
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
        async with self.client.session.get(
            "https://animechan.vercel.app/api/random"
        ) as response:
            data = await response.json()
            anime = data["anime"]
            character = data["character"]
            quote = str(data["quote"]).strip("[").strip("]")
            await ctx.trigger_typing()
            embed = Embed(title="Random Anime Quote", color=random.randint(0, 0xFFFFFF))
            embed.add_field(name="Anime:", value=anime, inline=True)
            embed.add_field(name="Character:", value=character, inline=True)
            embed.add_field(name="Quote:", value=quote, inline=True)
            await ctx.send(embed=embed)

    @commands.command(name="dogfact", aliases=["df"])
    async def random_dog_fact(self, ctx):
        """
        The random_dog_fact function retrieves a random dog fact
        from the Dog Fact API and embeds it in an Embed object.

        :param self: Used to access the client, which is used to access the bot's commands.
        :param ctx: Used to access the context of where the command was called.
        :return: discord embed
        """
        headers = {"Accept": "application/json"}
        async with self.client.session.get(
            "https://dog-fact-api.herokuapp.com/api/v1/resources/dogs?number=1",
            headers=headers,
        ) as response:
            data = await response.json()
            fact = data[0]["fact"]
            embed = Embed(color=random.randint(0, 0xFFFFFF))
            embed.add_field(name="Random Dog Fact:", value=fact, inline=True)
            await ctx.trigger_typing()
            await ctx.send(embed=embed)


def setup(client):
    """
    The setup function is used to register the commands that will be used in the bot.
    This function is run when you load a cog, and it allows you to use commands in your cogs.

    :param client: Used to pass in the discord.
    :return: the client object which is your entry point to the API.

    """
    client.add_cog(Fun(client))
