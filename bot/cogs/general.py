import random
import os

import discord
from discord.ext import commands, tasks
from sentry_sdk import capture_exception

from utils import gpt

class General(commands.Cog, name="General"):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.streamer_name = "lhcloudy27"
        self.cloudflare_url = os.environ.get("CLOUDFLARE_URL")
        self.cloudflare_token = os.environ.get('CLOUDFLARE_TOKEN')
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
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        
        if self.client.user.mentioned_in(message):
            if message.author.nick:
                name = message.author.nick
            else:
                name = message.author.name
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + self.cloudflare_token,
            }
            payload = {
                "messages": [
                    {
                        "role": "system",
                        "content": gpt.context + f"when you answer someone, answer them by {name}",
                    },
                    {
                        "role": "user",
                        "content": message.content.strip(f"<@!{self.client.user.id}>"),
                    },
                ]
            }
            await message.channel.typing()
            response = await self.client.session.post(
                url=self.cloudflare_url, headers=headers, json=payload
            )
            if response.status == 200:
                json_response = await response.json()
                await message.channel.send(json_response["result"]["response"])
            else:
                self.client.logger.error(
                    f"Error while trying to send message to Cloudflare: {response.status}, {response.reason}"
                )
                await message.channel.send(
                    "I couldn't respond to that, please try again later."
                )

    @commands.Cog.listener()
    async def on_command_completion(self, ctx) -> None:
        full_command_name = ctx.command.qualified_name
        split = full_command_name.split(" ")
        executed_command = str(split[0])
        self.client.logger.info(
            f"Executed {executed_command} command in {ctx.guild.name}"
            + f"(ID: {ctx.message.guild.id}) by {ctx.message.author} (ID: {ctx.message.author.id})"
        )


async def setup(client):
    await client.add_cog(General(client))
