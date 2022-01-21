import json
import os
import platform
import sys
import re
import random
from urllib.parse import quote_plus

import discord
from aiohttp import ContentTypeError
from discord.ext import commands, tasks

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json", encoding="utf-8") as file:
        config = json.load(file)


class General(commands.Cog, name="general"):
    """
    general bot commands
    """

    def __init__(self, client):
        self.client = client
        self.load_chuck_http_codes.start()
    
    @tasks.loop(count=1)
    async def load_chuck_http_codes(self):
        async with self.client.session.get('https://api.chucknorris.io/jokes/categories') as response:
            categories = await response.json()
            self.chuck_categories = [x for x in categories if x != 'explicit']

    @commands.command(name="info", aliases=["botinfo"])
    async def info(self, ctx):
        """
        information about the bot
        """
        embed = discord.Embed(description="LhBot", color=0x42F56C)
        embed.set_author(name="Bot Information")
        embed.add_field(name="Owner:", value="reinfrog#1738", inline=True)
        embed.add_field(name="Prefix:", value=f"{config['bot_prefix']}", inline=True)
        embed.add_field(
            name="Python Version:", value=f"{platform.python_version()}", inline=True
        )
        embed.add_field(
            name="URL:", value="https://github.com/alexraskin/lhbot", inline=True
        )
        await ctx.send(embed=embed)

    @commands.command(name="ping")
    async def ping(self, ctx):
        """
        ping the bot
        """
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"The bot latency is {round(self.client.latency * 1000)}ms.",
            color=0x42F56C,
        )
        embed.set_footer(
            text=f"Requested by {ctx.message.author}",
            icon_url=ctx.author.display_avatar)
        await ctx.send(embed=embed)
    
    @commands.command(
        name='search',
        aliases=['lmgtfy', 'duck', 'duckduckgo', 'google']
    )
    async def search(self, ctx, *, search_text=None):
        if search_text is None:
            await ctx.trigger_typing()
            await ctx.send('Please enter a search query!')
        if search_text:
            await ctx.trigger_typing()
            await self.duck_call(ctx, search_text)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if isinstance(message.channel, discord.DMChannel):
            return

        if re.search(
            r'(?i)(?:the|this) (?:current )?year is '
            + r'(?:almost |basically )?(?:over|done|finished)',
            message.content
        ):
            await message.channel.send(self.get_year_string())

        if re.search(
            r'(?i)send bobs and vagene',
            message.content
        ):
            await message.channel.send('😏 *sensible chuckle*')

        if re.search(
            r'(?i)^(?:hi|what\'s up|yo|hey|hello) lhbot',
            message.content
        ):
            await message.channel.send('hello')

        if re.search(
            r'(?i)^you wanna fight, lhbot\?',
            message.content
        ):
            await message.channel.send('bring it on pal (╯°□°）╯︵ ┻━┻')

        if re.search(
            r'(?i)^lhbot meow',
            message.content
        ):
            await message.channel.send('ฅ^•ﻌ•^ฅ')

        if re.search(
            r'(?i)^lh what(?:\'s| is) the answer to life,? the universe and everything',
            message.content
        ):
            await message.channel.send('42')

    @commands.command(
        name='chucknorris',
        aliases=['chuck', 'cn']
    )
    async def chucknorris(self, ctx, category: str = None):
        """ Collects a random chuck norris joke, or collect a random joke
            by specifying a specific category of joke. """
        if not hasattr(self, 'chuck_categories'):
            raise commands.BadArgument('Hold up partner, still locating Chuck!')

        if category is None:
            category = random.choice(self.chuck_categories)
        else:
            if category not in self.chuck_categories:
                raise commands.BadArgument(
                    f'Invalid category - please pick from:\n{", ".join(self.chuck_categories)}'
                )

        try:
            async with self.client.session.get(
                f'https://api.chucknorris.io/jokes/random?category={category}'
            ) as response:
                chuck = await response.json()
                chuck = chuck['value']

                embed = discord.Embed(
                    description=chuck,
                    color=random.randint(0, 0xFFFFFF))
                embed.set_author(
                    name='Chuck Norris fun fact...',
                    icon_url=f'https://assets.chucknorris.host/img/avatar/chuck-norris.png'
                )
                embed.set_footer(text=f'Category: {category} - https://api.chucknorris.io')
                await ctx.send(embed=embed)

        except:
            raise commands.BadArgument('Chuck not found, currently evading GPS in Texas!')

    
    async def duck_call(self, ctx, query):

        if len(query) > 500:
            await ctx.send('Query size is too long!')
            return

        query = '+'.join(query.split())
        async with self.client.session.get(
            f'https://api.duckduckgo.com/?format=json&t=lhbotdiscordbot&q={query}'
            ) as response:
            try:
                answer = await response.json(content_type="application/x-javascript")
            except ContentTypeError:
                await ctx.send('Invalid query')
                return

            if (not answer) or (not answer['AbstractText']):
                await ctx.send(
                    'Couldn\'t find anything, here\'s duckduckgo link: '
                    + f'<https://duckduckgo.com/?q={quote_plus(query)}>'
                )
                return

            embed = discord.Embed(
                description=answer['AbstractText'],
                color=0x2ECC71
            )

            if answer['Image']:
                embed.set_image(url=f'https://api.duckduckgo.com{answer["Image"]}')

            embed.set_author(
                name=answer['Heading'],
                icon_url='https://api.duckduckgo.com/favicon.ico'
            )

            embed.set_footer(
                text=f'Info from {answer["AbstractSource"]}\n'
                + f'at {answer["AbstractURL"]}\n'
                + 'Provided By: https://api.duckduckgo.com'
            )
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(General(client))
