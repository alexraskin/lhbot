import platform
from inspect import getsourcelines
import datetime, time

from discord import DMChannel, Embed
from discord.ext import commands
from utils.bot_utils import get_year_round, progress_bar


class General(commands.Cog, name="General"):
    def __init__(self, client: commands.Bot):
        """
        General commands
        :param self: Used to refer to the object itself.
        :param client: Used to pass the client object to the class.
        :return: the object of the class.
        """
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        global startTime
        startTime = time.time()

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

        if isinstance(message.channel, DMChannel):
            return

    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.command(name="info", aliases=["botinfo"])
    async def info_execute(self, ctx):
        """
        The info function specifically tells the user about the bot,
        and gives them a link to the github page.

        :param ctx: Used to get the context of where the command was called.
        :return: an embed with the bot's information.
        """
        embed = Embed(description="LhBot", color=0x42F56C)
        embed.set_author(
            name="Bot Information",
            icon_url="https://i.gyazo.com/632f0e60dc0535128971887acad98993.png",
        )
        embed.add_field(
            name="Owners:", value=str("reinfrog#1738, PayMeToThrow#2129"), inline=True
        )
        embed.add_field(
            name="Prefix:", value=self.client.config.bot_prefix, inline=True
        )
        embed.add_field(
            name="Python Version:", value=f"{platform.python_version()}", inline=True
        )
        embed.add_field(
            name="URL:", value="https://github.com/alexraskin/lhbot", inline=True
        )
        await ctx.send(embed=embed)

    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.command(name="ping")
    async def ping_execute(self, ctx):
        """
        The ping function is used to check the bot's latency.
        It returns a message with the time it takes for a message
        to reach Discord and be received by the bot.

        :param ctx: Used to get the context of where the command was called.
        :param latency: Latency of the bot.
        :return: a discord embed.
        """
        embed = Embed(
            title="🏓 Pong!",
            description=f"The bot latency is {round(self.client.latency * 1000)}ms.",
            color=0x42F56C,
        )
        embed.set_footer(text=f"Requested by {ctx.message.author}")
        await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="year", aliases=["yearprogress"])
    async def year_execute(self, ctx):
        """
        The year function tells the user how much of the current year has passed.

        :param ctx: Used to get the context of where the command was called.
        :return: an embed with the percentage of the year that has passed.
        """
        await ctx.typing()
        embed = Embed(color=0x42F56C)
        embed.set_author(
            name="Year Progress",
            icon_url="https://i.gyazo.com/db74b90ebf03429e4cc9873f2990d01e.png",
        )
        embed.add_field(
            name="Progress:", value=progress_bar(get_year_round()), inline=True
        )
        await ctx.send(embed=embed)

    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.command(name="inspect", hidden=True)
    async def inspect(self, ctx, command_name: str):
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
            "<https://github.com/alexraskin/lhbot/blob/main/"
            f'{"/".join(module.split("."))}.py#L{startline}>\n'
        )
        sauce = "".join(saucelines)
        sanitized = sauce.replace("`", "\u200B`")
        if len(url) + len(sanitized) > 1950:
            sanitized = sanitized[: 1950 - len(url)] + "\n[...]"
        await ctx.typing()
        await ctx.send(url + f"```python\n{sanitized}\n```")

    @commands.command(
        name="uptime", aliases=["up"], description="Shows the uptime of the bot"
    )
    async def uptime(self, ctx):
        """
        The uptime function is used to show the uptime of the bot.
        """
        await ctx.typing()
        uptime = str(datetime.timedelta(seconds=int(round(time.time() - startTime))))

        embed = Embed(
            title="Bot Uptime", description=f"Uptime: {uptime}", color=0x42F56C
        )
        embed.set_footer(text=f"Requested by {ctx.message.author}")

        await ctx.send(embed=embed)


async def setup(client):
    """
    The setup function is used to register the commands that will be used in the bot.
    This function is run when you load a cog, and it allows you to use commands in your cogs.

    :param client: Used to pass in the client object.
    :return: a dictionary that contains the following keys:.
    """
    await client.add_cog(General(client))
