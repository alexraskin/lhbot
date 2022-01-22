import random

from discord import Embed
from discord.ext import commands, tasks


class Fun(commands.Cog, name="Fun"):
    def __init__(self, client):
        """
        The __init__ function is the constructor for a class. It initializes the attributes of an object. In this case, it initializes
        the client attribute.
        
        :param self: Used to access variables that belong to the class.
        :param client: Used to pass in the client object to the class.
        :return: a class instance and sets up the client.
        :doc-author: Trelent
        """
        self.client = client
        self.load_chuck_http_codes.start()

    @tasks.loop(count=1)
    async def load_chuck_http_codes(self):
        """
        The load_chuck_http_codes function specifically loads the categories from the Chuck Norris API and stores them in a list.
        
        :param self: Used to store the bot object.
        :return: a list of categories.
        :doc-author: Trelent
        """
        async with self.client.session.get('https://api.chucknorris.io/jokes/categories') as response:
            categories = await response.json()
            self.chuck_categories = [x for x in categories if x != 'explicit']

    @commands.command(
        name="chucknorris",
        aliases=["chuck", "cn"])
    async def chucknorris(self, ctx, category: str = None):
        """
        The chucknorris function is a command that allows the user to get a random chuck norris fact.
        The function takes in an optional argument, category, which can be any of the following:
            -   "animal"
            -   "career"
            -   "celebrity"
            -   "dev" (NSFW)  # I'm not sure if this is NSFW or not but it's definitely weird...  # noQA: E501
        
        :param self: Used to access attributes of the class.
        :param ctx: Used to get the channel and user that sent the command.
        :param category:str=None: Used to determine if the user has specified a category or not.
        :return: a random joke from the API.
        :doc-author: Trelent
        """
        if not hasattr(self, 'chuck_categories'):
            raise commands.BadArgument(
                'Hold up partner, still locating Chuck!')

        if category is None:
            category = random.choice(self.chuck_categories)
        else:
            if category not in self.chuck_categories:
                raise commands.BadArgument(
                    f'Invalid category - please pick from:\n{", ".join(self.chuck_categories)}'
                )
        try:
            async with self.client.session.get(
                    f'https://api.chucknorris.io/jokes/random?category={category}') as response:
                chuck = await response.json()
                chuck = chuck['value']
                embed = Embed(
                    description=chuck,
                    color=random.randint(0, 0xFFFFFF))
                embed.set_author(
                    name='Chuck Norris fun fact...',
                    icon_url=f'https://assets.chucknorris.host/img/avatar/chuck-norris.png')
                embed.set_footer(
                    text=f'Category: {category} - https://api.chucknorris.io')
                await ctx.send(embed=embed)

        except BaseException:
            raise commands.BadArgument(
                'Chuck not found, currently evading GPS in Texas!')

    @commands.command(
        name="cat",
        aliases=["catpic"])
    async def cat(self, ctx):
        """
        The cat function specifically gets a random cat picture from the random.cat API and sends it to the channel.
        
        :param self: Used to access the client and other variables in this cog.
        :param ctx: Used to get the context of where the command was called.
        :return: a random cat picture from the random.
        :doc-author: Trelent
        """
        async with self.client.session.get('https://aws.random.cat/meow') as response:
            cat = await response.json()
            cat_photo = cat["file"]

            await ctx.send(cat_photo)

    @commands.command(
        name="dog",
        aliases=["dogpic"])
    async def dog(self, ctx):
        """
        The dog function specifically gets a random dog picture from the website random.dog
        
        :param self: Used to access the client object.
        :param ctx: Used to get the channel and author of the message.
        :return: a dog picture in the form of a url.
        :doc-author: Trelent
        """
        async with self.client.session.get('https://random.dog/woof.json') as response:
            dog = await response.json()
            dog_photo = dog["url"]

            await ctx.send(dog_photo)

    @commands.command(
        name="meme",
        aliases=["memer"]
    )
    async def get_meme(self, ctx):
        """
        The get_meme function specifically gets a random meme from the reddit api and returns it to the user
        
        :param self: Used to access the client object.
        :param ctx: Used to access the context of where the command was called.
        :return: the link to the meme from reddit.
        :doc-author: Trelent
        """
        async with self.client.session.get('https://meme-api.herokuapp.com/gimme') as response:
            data = await response.json()
            meme = data["url"]

            await ctx.send(meme)


def setup(client):
    client.add_cog(Fun(client))
