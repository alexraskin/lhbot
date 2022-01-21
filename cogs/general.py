import json
import os
import platform
import sys
from urllib.parse import quote_plus

import aiohttp
import discord
from aiohttp import ContentTypeError
from discord.ext import commands

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json", encoding="utf-8") as file:
        config = json.load(file)


class General(commands.Cog, name="general"):
    """
    general bot commands
    """

    def __init__(self, bot):
        self.bot = bot

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
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms.",
            color=0x42F56C,
        )
        embed.set_footer(text=f"Requested by {ctx.message.author}")
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

    
    async def duck_call(self, ctx, query):

        if len(query) > 500:
            await ctx.send('Query size is too long!')
            return

        query = '+'.join(query.split())
        async with aiohttp.ClientSession() as session:
            async with session.get(
                'https://api.duckduckgo.com/?format=json&t=lhbotdiscordbot&q='
                + f'{query}'
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


def setup(bot):
    bot.add_cog(General(bot))
