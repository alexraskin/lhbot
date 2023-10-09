import platform
import pkg_resources

import discord
from discord.ext import commands
from discord import Embed, Member, app_commands, Colour

from utils.bot_utils import date


class Info(commands.Cog, name="Info"):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @commands.command(
        name="uptime", aliases=["up"], description="Shows the uptime of the bot"
    )
    async def uptime(self, ctx):
        embed = discord.Embed(
            title="Bot Uptime",
            description=f"Uptime: {self.client.get_uptime}",
            timestamp=ctx.message.created_at,
        )
        embed.colour = Colour.blurple()
        embed.set_thumbnail(url=self.client.user.avatar.url)

        await ctx.send(embed=embed)

    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.command(name="ping")
    async def ping(self, ctx):
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"The bot latency is {self.client.get_bot_latency}ms.",
            timestamp=ctx.message.created_at,
        )
        embed.colour = Colour.blurple()
        embed.set_thumbnail(url=self.client.user.avatar.url)
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="info", help="Get info about the bot", with_app_command=True
    )
    @commands.guild_only()
    @app_commands.guild_only()
    async def get_info(self, ctx: commands.Context) -> None:
        version = pkg_resources.get_distribution("discord.py").version
        embed = Embed(
            description=self.client.description,
            timestamp=ctx.message.created_at,
        )
        embed.title = "LhBot"
        embed.url = "https://lhbot.twizy.dev/"
        embed.colour = Colour.blurple()
        embed.set_author(
            name=str(self.client.owner), icon_url=self.client.owner.display_avatar.url
        )
        embed.add_field(
            name="Process",
            value=f"{self.client.memory_usage:.2f} MiB\n{self.client.cpu_usage:.2f}% CPU",
        )
        embed.add_field(name="Uptime", value=self.client.get_uptime)
        embed.add_field(name="Bot Version", value=self.client.version)
        embed.add_field(name="Git Revision", value=self.client.git_revision)
        embed.add_field(name="Python Version", value=platform.python_version())
        embed.set_footer(
            text=f"Made with discord.py v{version}",
            icon_url="http://i.imgur.com/5BFecvA.png",
        )
        embed.set_thumbnail(url=self.client.logo_url)
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="serverinfo", aliases=["guildinfo"])
    @commands.guild_only()
    async def serverinfo(self, ctx: commands.Context):
        """Get server information"""
        find_bots = sum(1 for member in ctx.guild.members if member.bot)
        embed = Embed()
        embed.colour = Colour.blurple()
        embed.title = f"{ctx.guild.name}"

        if ctx.guild.icon:
            embed.set_thumbnail(url=ctx.guild.icon)
        if ctx.guild.banner:
            embed.set_image(url=ctx.guild.banner.with_format("png").with_size(1024))

        embed.add_field(name="Server Name", value=ctx.guild.name)
        embed.add_field(name="Server ID", value=ctx.guild.id)
        embed.add_field(name="Members", value=ctx.guild.member_count)
        embed.add_field(name="Bots", value=find_bots)
        embed.add_field(name="Owner", value=ctx.guild.owner)
        embed.add_field(name="Created", value=date(ctx.guild.created_at, ago=True))
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="user", aliases=["member"])
    @commands.guild_only()
    @app_commands.guild_only()
    async def user(self, ctx: commands.Context, *, user: Member = None):
        """Get user information"""
        user = user or ctx.author

        show_roles = "None"
        if len(user.roles) > 1:
            show_roles = ", ".join(
                [
                    f"<@&{x.id}>"
                    for x in sorted(user.roles, key=lambda x: x.position, reverse=True)
                    if x.id != ctx.guild.default_role.id
                ]
            )

        embed = Embed(colour=user.top_role.colour.value)
        embed.title = f"{user.name}#{user.discriminator}"
        embed.set_thumbnail(url=user.avatar)

        embed.add_field(name="Full name", value=user)
        embed.add_field(
            name="Nickname", value=user.nick if hasattr(user, "nick") else "None"
        )
        embed.add_field(name="Account created", value=date(user.created_at, ago=True))
        embed.add_field(name="Joined this server", value=date(user.joined_at, ago=True))
        embed.add_field(name="Roles", value=show_roles, inline=False)

        await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(Info(client))
