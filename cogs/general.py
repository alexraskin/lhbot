import platform
import re
from datetime import datetime as dt
from inspect import getsourcelines
from urllib.parse import quote_plus

import discord
from aiohttp import ContentTypeError
from discord.ext import commands


class General(commands.Cog, name="general"):
    """
    general bot commands
    """

    def __init__(self, client):
        self.client = client

    def get_year_string(self):
        now = dt.utcnow()
        year_end = dt(now.year + 1, 1, 1)
        year_start = dt(now.year, 1, 1)
        year_percent = (now - year_start) / (year_end - year_start) * 100
        return f'For your information, the year is {year_percent:.1f}% over!'

    @commands.command(name="info", aliases=["botinfo"])
    async def info(self, ctx):
        """
        information about the bot
        """
        embed = discord.Embed(description="LhBot", color=0x42F56C)
        embed.set_author(name="Bot Information")
        embed.add_field(name="Owner:", value="reinfrog#1738", inline=True)
        embed.add_field(
            name="Prefix:",
            value=f"{self.client.config['bot_prefix']}",
            inline=True)
        embed.add_field(
            name="Python Version:",
            value=f"{platform.python_version()}",
            inline=True)
        embed.add_field(
            name="URL:",
            value="https://github.com/alexraskin/lhbot",
            inline=True)
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
            text=f"Requested by {ctx.message.author}")
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
            r'(?i)^(?:hi|what\'s up|yo|hey|hello) lhbot',
            message.content
        ):
            await message.channel.send('hello')

        if re.search(
            r'(?i)(?:the|this) (?:current )?year is '
            + r'(?:almost |basically )?(?:over|done|finished)',
            message.content
        ):
            await message.channel.send(self.get_year_string())

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
                message.content):
            await message.channel.send('42')

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
                embed.set_image(
                    url=f'https://api.duckduckgo.com{answer["Image"]}')

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

    @commands.command(
        name='inspect'
    )
    async def inspect(self, ctx, *, command_name: str):
        """Print a link and the source code of a command"""
        cmd = self.client.get_command(command_name)
        if cmd is None:
            return
        module = cmd.module
        saucelines, startline = getsourcelines(cmd.callback)
        url = (
            '<https://github.com/alexraskin/lhbot/blob/main/'
            f'{"/".join(module.split("."))}.py#L{startline}>\n'
        )
        sauce = ''.join(saucelines)
        sanitized = sauce.replace('`', '\u200B`')
        if len(url) + len(sanitized) > 1950:
            sanitized = sanitized[:1950 - len(url)] + '\n[...]'
        await ctx.send(url + f'```python\n{sanitized}\n```')


def setup(client):
    client.add_cog(General(client))
