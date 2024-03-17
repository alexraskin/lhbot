from __future__ import annotations

import datetime
from typing import Optional, TYPE_CHECKING

from discord import Embed, Interaction, Member, TextChannel, app_commands
from discord.ext import commands
from sentry_sdk import capture_exception
from utils import checks

if TYPE_CHECKING:
    from ..bot import LhBot


class Mod(commands.Cog):
    def __init__(self, client: LhBot) -> None:
        self.client: LhBot = client

    @app_commands.command(description="Check if you are a mod")
    @app_commands.guild_only()
    async def amimod(self, interaction: Interaction) -> None:
        if (
            interaction.user.guild_permissions.administrator
            or interaction.user.guild_permissions.manage_guild
        ):
            await interaction.response.send_message(
                "Yes", ephemeral=True, delete_after=5
            )
        else:
            await interaction.response.send_message(
                "No", ephemeral=True, delete_after=5
            )

    @commands.hybrid_group(
        description="Mod Only Commands", without_command=True, hidden=True
    )
    @checks.is_mod()
    @commands.guild_only()
    @app_commands.guild_only()
    async def mod(self, ctx: commands.Context) -> None:
        if ctx.invoked_subcommand is None:
            if ctx.author.guild_permissions.manage_guild:  # type: ignore
                await ctx.send_help(ctx.command)

    @mod.command(name="ban", description="Ban a user", hidden=True)
    @checks.is_mod()
    @app_commands.guild_only()
    @app_commands.describe(member="The member to ban")
    @app_commands.describe(reason="The reason for the ban")
    async def ban(
        self, ctx: commands.Context, member: Member, reason: Optional[str]
    ) -> None:
        try:
            await ctx.guild.ban(member, reason=reason)  # type: ignore
            await ctx.reply(f"Banned {member.name}", ephemeral=True)
        except Exception as e:
            capture_exception(e)
            self.client.logger.error(f"Error: {e}")
            await ctx.reply("An error occurred while banning the user.", ephemeral=True)
            return

    @mod.command(description="Softban a user", hidden=True)
    @checks.is_mod()
    @app_commands.describe(member="The member to softban")
    @app_commands.describe(reason="The reason for the softban")
    async def softban(
        self, ctx: commands.Context, member: Member, reason: Optional[str]
    ) -> None:
        try:
            await ctx.guild.ban(member, reason=reason)  # type: ignore
            await ctx.guild.unban(member, reason=reason)  # type: ignore
            await ctx.reply(f"Softbanned {member.name}", ephemeral=True)
        except Exception as e:
            capture_exception(e)
            self.client.logger.error(f"Error: {e}")
            await ctx.reply(
                "An error occurred while softbanning the user.", ephemeral=True
            )
            return

    @mod.command(name="kick", description="Kick a user")
    @checks.hybrid_permissions_check(kick_members=True)
    @app_commands.describe(member="The member to kick")
    @app_commands.describe(reason="The reason for the kick")
    async def kick(self, ctx: commands.Context, member: Member, reason: str) -> None:
        try:
            await ctx.guild.kick(member, reason=reason)  # type: ignore
            await ctx.reply(f"Kicked {member.name}", ephemeral=True)
        except Exception as e:
            capture_exception(e)
            self.client.logger.error(f"Error: {e}")
            await ctx.reply("An error occurred while kicking the user.", ephemeral=True)
            return

    @mod.command(name="timeout", description="Timeout a user")
    @checks.hybrid_permissions_check(manage_roles=True)
    @app_commands.describe(member="The member to timeout")
    @app_commands.describe(reason="The reason for the timeout")
    @app_commands.describe(duration="The duration of the timeout")
    async def timeout(
        self,
        ctx: commands.Context,
        member: Member,
        duration: int,
        reason: str,
    ) -> None:
        unmute_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=duration)
        try:
            await member.timeout(until=unmute_time, reason=reason)  # type: ignore
            await ctx.reply(f"Timed out {member.name}", ephemeral=True)
        except Exception as e:
            capture_exception(e)
            self.client.logger.error(f"Error: {e}")
            await ctx.reply(
                "An error occurred while timing out the user.", ephemeral=True
            )
            return

    @mod.command(name="unban", description="Unban a user")
    @checks.hybrid_permissions_check(ban_members=True)
    @app_commands.describe(member="The member to unban")
    @app_commands.describe(reason="The reason for the unban")
    async def unban(self, ctx: commands.Context, member: Member, reason: str) -> None:
        try:
            await ctx.guild.unban(member, reason=reason)  # type: ignore
            await ctx.reply(f"Unbanned {member.name}", ephemeral=True)
        except Exception as e:
            capture_exception(e)
            self.client.logger.error(f"Error: {e}")
            await ctx.reply(
                "An error occurred while unbanning the user.", ephemeral=True
            )
            return

    @mod.command(name="purge", description="Purge a specified amount of messages.")
    @checks.hybrid_permissions_check(manage_messages=True)
    @commands.guild_only()
    @app_commands.guild_only()
    @app_commands.describe(amount="The amount of messages to purge.")
    @app_commands.describe(reason="The reason for purging the messages.")
    async def purge(
        self, ctx: commands.Context, amount: int, reason: Optional[str] = None
    ) -> None:
        """
        Purges a specified amount of messages from the channel.
        """
        if amount <= 0:
            await ctx.reply("Please specify a positive number of messages to delete.")
            return
        try:
            amount += 1
            await ctx.channel.purge(limit=amount, reason=reason)
            embed = Embed(
                title="Purge 🗑️",
                description=f"Purged {amount} messages.",
                color=0x00FF00,
                timestamp=ctx.message.created_at,
            )
            await ctx.reply(embed=embed, delete_after=5)
        except Exception as e:
            capture_exception(e)
            self.client.logger.error(f"Error: {e}")
            await ctx.reply("An error occurred while purging messages.", ephemeral=True)
            return

    @mod.command(name="lockdown", description="Lockdowns a specified channel.")
    @checks.hybrid_permissions_check(manage_channels=True)
    @commands.guild_only()
    @app_commands.guild_only()
    @app_commands.describe(
        channel="The channel to lockdown. Defaults to the current channel."
    )
    @app_commands.describe(reason="The reason for locking down the channel.")
    async def lockdown(
        self,
        ctx: commands.Context,
        channel: Optional[TextChannel] = None,
        *,
        reason: Optional[str] = None,
    ) -> None:
        """
        Lockdowns a specified channel.
        """
        channel = channel or ctx.channel  # type: ignore
        try:
            await channel.set_permissions(ctx.guild.default_role, send_messages=False)  # type: ignore
            embed = Embed(
                title="Lockdown Notice 🔒",
                description=f"This channel is currently under lockdown.",
                color=0x00FF00,
                timestamp=ctx.message.created_at,
            )
            if reason:
                embed.add_field(name="Reason:", value=reason)
            embed.set_footer(text="Please be patient and follow server rules")
            await ctx.send(embed=embed)
        except Exception as e:
            capture_exception(e)
            self.client.logger.error(f"Error: {e}")
            await ctx.send(
                "An error occurred while locking down the channel.", ephemeral=True
            )
            return

    @mod.command(name="unlock", description="Unlocks a specified channel.")
    @checks.hybrid_permissions_check(manage_channels=True)
    @commands.guild_only()
    @app_commands.guild_only()
    @app_commands.describe(
        channel="The channel to unlock. Defaults to the current channel."
    )
    @app_commands.describe(reason="The reason for unlocking the channel.")
    @commands.has_permissions(manage_channels=True)
    @app_commands.checks.has_permissions(manage_channels=True)
    async def unlock(
        self,
        ctx: commands.Context,
        channel: Optional[TextChannel] = None,
        *,
        reason: Optional[str] = None,
    ) -> None:
        """
        Unlocks a specified channel.
        """
        channel = channel or ctx.channel  # type: ignore
        try:
            await channel.set_permissions(  # type: ignore
                ctx.guild.default_role, send_messages=True, reason=reason  # type: ignore
            )
            embed = Embed(
                title="Lockdown Ended 🔓",
                description=f"The lockdown has been lifted.",
                color=0x00FF00,
                timestamp=ctx.message.created_at,
            )
            if reason:
                embed.add_field(name="Reason:", value=reason)
            embed.set_footer(text="Please be patient and follow server rules")
            await ctx.send(embed=embed)
        except Exception as e:
            capture_exception(e)
            self.client.logger.error(f"Error: {e}")
            await ctx.send(
                "An error occurred while unlocking the channel.", ephemeral=True
            )
            return


async def setup(client: LhBot) -> None:
    await client.add_cog(Mod(client))
