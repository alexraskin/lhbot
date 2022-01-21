import random

from discord import Embed
from discord.ext import commands, tasks


class Fun(commands.Cog, name="Fun"):
    """
    Fun bot commands
    """

    def __init__(self, client):
        self.client = client
        self.load_chuck_http_codes.start()

    @tasks.loop(count=1)
    async def load_chuck_http_codes(self):
        async with self.client.session.get('https://api.chucknorris.io/jokes/categories') as response:
            categories = await response.json()
            self.chuck_categories = [x for x in categories if x != 'explicit']

    @commands.command(
        name="chucknorris",
        aliases=["chuck", "cn"])
    async def chucknorris(self, ctx, category: str = None):
        """ Collects a random chuck norris joke, or collect a random joke
            by specifying a specific category of joke. """
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
        """Shows a random cat picture"""
        async with self.client.session.get('https://aws.random.cat/meow') as response:
            cat = await response.json()
            cat_photo = cat["file"]

            await ctx.send(cat_photo)

    @commands.command(
        name="dog",
        aliases=["dogpic"])
    async def dog(self, ctx):
        """Shows a random dog picture"""
        async with self.client.session.get('https://random.dog/woof.json') as response:
            dog = await response.json()
            dog_photo = dog["url"]

            await ctx.send(dog_photo)


def setup(client):
    client.add_cog(Fun(client))
