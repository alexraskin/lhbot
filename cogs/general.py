import platform
import re
from datetime import datetime as dt
from inspect import getsourcelines
from urllib.parse import quote_plus

import discord
from aiohttp import ContentTypeError
from discord.ext import commands


class General(commands.Cog, name="general"):
    def __init__(self, client):
        """
        The __init__ function is the constructor for a class. It is called when an instance of a class is created.
        It allows the newly created object to have some attributes that are specified at creation time.

        :param self: Used to refer to the object itself.
        :param client: Used to pass the client object to the class.
        :return: the object of the class.
        """
        self.client = client

    def get_year_string(self):
        """
        The get_year_string function is used to get the current year and then
        calculate the percentage of time that has passed in relation to the total
        number of days in a year. This is done by taking today's date, adding one
        year and subtracting today's date from that new date. Then dividing this
        difference by 365 (the number of days in a year) and multiplying it by 100.

        :param self: Used to refer to the object instance.
        :return: the percentage of the current year that has elapsed.
        """
        now = dt.utcnow()
        year_end = dt(now.year + 1, 1, 1)
        year_start = dt(now.year, 1, 1)
        year_percent = (now - year_start) / (year_end - year_start) * 100
        return f'For your information, the year is {year_percent:.1f}% over!'

    @commands.command(name="info", aliases=["botinfo"])
    async def info(self, ctx):
        """
        The info function specifically tells the user about the bot, and gives them a link to the github page.

        :param self: Used to access the class attributes and methods.
        :param ctx: Used to get the context of where the command was called.
        :return: an embed with the bot's information.
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
        The ping function is used to check the bot's latency.
        It returns a message with the time it takes for a message to reach Discord and be received by the bot.

        :param self: Used to access variables that belong to the class.
        :param ctx: Used to get the context of where the command was called.
        :return: a discord embed.
        """
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"The bot latency is {round(self.client.latency * 1000)}ms.",
            color=0x42F56C,
        )
        embed.set_footer(
            text=f"Requested by {ctx.message.author}")
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        The on_message function specifically handles messages that are sent to the bot.
        It checks if the message is a command, and then executes it if it is.

        :param self: Used to access the class' attributes and methods.
        :param message: Used to store information about the message.
        :return: None.
        """
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

    @commands.command(
        name='search',
        aliases=['lmgtfy', 'duck', 'duckduckgo', 'google']
    )
    async def search(self, ctx, query=None):
        """
        The search function is used to search for a query on duckduckgo.
        It returns the first result of the query and sends it as an embed.

        :param self: Used to access attributes and methods of the class.
        :param ctx: Used to access the context of the command.
        :param query=None: Used to make sure that the function cannot be called without a query.
        :return: a discord embed object with the following format:.
        """
        if query is None:
            await ctx.trigger_typing()
            await ctx.send('Please enter a search query!')

        if len(query) > 500:
            await ctx.trigger_typing()
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
        name='inspect',
        hidden=True
    )
    async def inspect(self, ctx, *, command_name: str):
        """
        The inspect function is used to print the source code of a command.
        It's useful for figuring out what exactly a command does, and how it works.

        :param self: Used to access the client object.
        :param ctx: Used to access the bot's context.
        :param *: Used to pass a list of arguments to the function.
        :param command_name:str: Used to specify the name of the command that we want to inspect.
        :return: a link to the github repo and the source code of a command.
        """
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
    """
    The setup function is used to register the commands that will be used in the bot.
    This function is run when you load a cog, and it allows you to use commands in your cogs.

    :param client: Used to pass in the client object.
    :return: a dictionary that contains the following keys:.
    """
    client.add_cog(General(client))
