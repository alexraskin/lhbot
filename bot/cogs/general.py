import platform
import random
from inspect import getsourcelines

import discord
from discord.ext import commands, tasks
from sentry_sdk import capture_exception
from utils.bot_utils import get_year_round, progress_bar


class General(commands.Cog, name="General"):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.streamer_name = "lhcloudy27"
        self.twitch_url = "https://www.twitch.tv/lhcloudy27"
        self.body = {
            "client_id": self.client.config.twitch_client_id,
            "client_secret": self.client.config.twitch_client_secret,
            "grant_type": "client_credentials",
        }
        self.status_task.start()

    async def check_if_live(self) -> set:
        async with self.client.session.post(
            "https://id.twitch.tv/oauth2/token", data=self.body
        ) as response:
            keys = await response.json()
            headers = {
                "Client-ID": self.client.config.twitch_client_id,
                "Authorization": "Bearer " + keys["access_token"],
            }
        async with self.client.session.get(
            f"https://api.twitch.tv/helix/streams?user_login={self.streamer_name}",
            headers=headers,
        ) as response:
            stream_data = await response.json()
            if len(stream_data["data"]) == 1:
                if stream_data["data"][0]["type"] == "live":
                    return (
                        True,
                        stream_data["data"][0]["game_name"],
                        stream_data["data"][0]["title"],
                        stream_data["data"][0]["thumbnail_url"],
                    )
            else:
                return False, None, None, None

    @tasks.loop(seconds=60)
    async def status_task(self) -> None:
        statuses = [
            "Overwatch",
            "Overwatch 2",
            "Diffing LhCloudy",
            f"{self.client.config.bot_prefix}help",
            f"{self.client.config.bot_prefix}info",
            f"{self.client.config.bot_prefix}dog",
            f"{self.client.config.bot_prefix}cat",
            f"{self.client.config.bot_prefix}meme",
        ]
        check = await self.check_if_live()
        if check[0] == True:
            await self.client.change_presence(
                activity=discord.Streaming(
                    name="LhCloudy is Live!",
                    url=self.twitch_url,
                    platform="Twitch",
                    game=check[1],
                )
            )
        else:
            await self.client.change_presence(
                activity=discord.Game(random.choice(statuses))
            )

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error) -> None:
        if hasattr(ctx.command, "on_error"):
            return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return
        if isinstance(error, commands.CheckFailure):
            await ctx.send("You don't have the permissions needed to use this command")
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing required argument: {error.param.name}")
            return

        if isinstance(error, commands.CommandNotFound):
            await ctx.send(
                f"Command not found, try `{self.client.config.bot_prefix}help` for a list of available commands."
            )
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f"{ctx.command} has been disabled.")
            return

        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                "This command is on cool down."
                + f" Please try again in {round(error.retry_after)} "
                + f'{"second" if round(error.retry_after) <= 1 else "seconds"}.'
            )
            self.client.logger.info("Command on cooldown")
            return
        else:
            await ctx.send(
                f"An error occurred, this has been reported to the developers.",
                ephemeral=True,
            )
            self.client.logger.error(error)
            capture_exception(error)
            return

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if isinstance(message.channel, discord.DMChannel):
            try:
                await message.author.send(
                    f"{message.command} can not be used in Private Messages."
                )
            except discord.HTTPException:
                self.client.logger.error(f"Failed to send message to {message.author}")
                pass

    @commands.Cog.listener()
    async def on_command_completion(self, ctx) -> None:
        full_command_name = ctx.command.qualified_name
        split = full_command_name.split(" ")
        executed_command = str(split[0])
        self.client.logger.info(
            f"Executed {executed_command} command in {ctx.guild.name}"
            + f"(ID: {ctx.message.guild.id}) by {ctx.message.author} (ID: {ctx.message.author.id})"
        )

    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.command(name="info", aliases=["botinfo"])
    async def info(self, ctx):
        embed = discord.Embed(
            description="LhBot is a Discord bot that was created by twizykat.",
            color=0x42F56C,
            timestamp=ctx.message.created_at,
        )
        embed.set_author(
            name="LhBot",
            icon_url="https://i.gyazo.com/632f0e60dc0535128971887acad98993.png",
        )
        embed.add_field(name="Owners:", value=str("twizykat"), inline=True)
        embed.add_field(
            name="Prefix:", value=self.client.config.bot_prefix, inline=True
        )
        embed.add_field(
            name="Python Version:", value=f"{platform.python_version()}", inline=True
        )
        embed.add_field(
            name="URL:", value="https://github.com/alexraskin/lhbot", inline=True
        )
        embed.set_footer(text=self.client.footer, icon_url=self.client.logo_url)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.command(name="ping")
    async def ping(self, ctx):
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"The bot latency is {self.client.get_bot_latency()}ms.",
            color=0x42F56C,
            timestamp=ctx.message.created_at,
        )
        embed.set_footer(text=self.client.footer, icon_url=self.client.logo_url)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="year", aliases=["yearprogress"])
    async def year(self, ctx):
        await ctx.typing()
        embed = discord.Embed(color=0x42F56C, timestamp=ctx.message.created_at)
        embed.set_author(
            name="Year Progress",
            icon_url="https://i.gyazo.com/db74b90ebf03429e4cc9873f2990d01e.png",
        )
        embed.add_field(
            name="Progress:", value=progress_bar(get_year_round()), inline=True
        )
        embed.set_footer(text=self.client.footer, icon_url=self.client.logo_url)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.command(name="inspect", hidden=True)
    async def inspect(self, ctx, command_name: str):
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
        await ctx.typing()

        embed = discord.Embed(
            title="Bot Uptime",
            description=f"Uptime: {self.client.get_uptime()}",
            color=0x42F56C,
            timestamp=ctx.message.created_at,
        )
        embed.set_footer(text=self.client.footer, icon_url=self.client.logo_url)

        await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(General(client))
