from __future__ import annotations

import datetime
from typing import Optional

from discord import Embed, Interaction, Member, TextChannel, app_commands
from discord.ext import commands
from discord.ext.commands.context import Context


class Mod(commands.Cog, name="Mod"):
    def __init__(self, client: commands.Bot) -> None:
        self.client: commands.Bot = client

    @app_commands.command(description="Check if you are a mod")
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

    @commands.hybrid_group(description="Mod Only Commands", without_command=True)
    @commands.guild_only()
    @app_commands.guild_only()
    async def mod(self, ctx: commands.Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    async def admin_check(self, ctx: commands.Context):
        if ctx.author.guild_permissions.administrator:
            return True
        else:
            await ctx.reply(
                "You don't have permission to manage the server!", ephemeral=True
            )
            return False

    async def mod_check(self, ctx: commands.Context):
        if ctx.author.guild_permissions.manage_guild:
            return True
        else:
            await ctx.reply(
                "You don't have permission to manage the server!", ephemeral=True
            )
            return False

    async def ban_check(self, ctx: commands.Context):
        if ctx.author.guild_permissions.ban_members:
            return True
        else:
            await ctx.reply("You don't have permission to ban members!", ephemeral=True)
            return False

    async def kick_check(self, ctx: commands.Context):
        if ctx.author.guild_permissions.kick_members:
            return True
        else:
            await ctx.reply(
                "You don't have permission to kick members!", ephemeral=True
            )
            return False

    async def check_if_bot(self, ctx: commands.Context, member: Member):
        if member == ctx.guild.me:
            await ctx.reply("I can't ban myself!", ephemeral=True)
            return False
        else:
            return True

    async def check_if_owner(self, ctx: commands.Context):
        if ctx.author.id == self.client.owner_id:
            await ctx.reply("You can't ban the owner!", ephemeral=True)
            return False
        else:
            return True

    async def top_role_check(self, ctx: commands.Context, member: Member):
        if member.top_role >= ctx.author.top_role:
            await ctx.reply("You can't ban someone with a higher role!", ephemeral=True)
            return False
        else:
            return True

    async def top_role_check_me(self, ctx: commands.Context, member: Member):
        if member.top_role >= ctx.guild.me.top_role:
            await ctx.reply("I can't ban someone with a higher role!", ephemeral=True)
            return False
        else:
            return True

    @mod.command(name="ban", description="Ban a user")
    @commands.has_permissions(ban_members=True)
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.describe(member="The member to ban")
    @app_commands.describe(reason="The reason for the ban")
    async def ban(
        self, ctx: commands.Context, member: Member, reason: Optional[str]
    ) -> None:
        if not await self.check_if_bot(ctx, member):
            return
        if not await self.check_if_owner(ctx):
            return
        if not await self.top_role_check(ctx, member):
            return
        if not await self.top_role_check_me(ctx, member):
            return
        if not await self.ban_check(ctx):
            return
        await ctx.guild.ban(member, reason=reason)
        await ctx.reply(f"Banned {member.name}", ephemeral=True)

    @mod.command(description="Softban a user")
    @commands.has_permissions(ban_members=True)
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.describe(member="The member to softban")
    @app_commands.describe(reason="The reason for the softban")
    async def softban(
        self, ctx: commands.Context, member: Member, reason: Optional[str]
    ) -> None:
        if not await self.check_if_bot(ctx, member):
            return
        if not await self.check_if_owner(ctx):
            return
        if not await self.top_role_check(ctx, member):
            return
        if not await self.top_role_check_me(ctx, member):
            return
        if not await self.ban_check(ctx):
            return
        if not await self.admin_check(ctx):
            return
        await ctx.guild.ban(member, reason=reason)
        await ctx.guild.unban(member, reason=reason)
        await ctx.reply(f"Softbanned {member.name}", ephemeral=True)

    @mod.command(name="kick", description="Kick a user")
    @commands.has_permissions(kick_members=True)
    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.describe(member="The member to kick")
    @app_commands.describe(reason="The reason for the kick")
    async def _kick(self, ctx: commands.Context, member: Member, reason: str) -> None:
        if not await self.check_if_bot(ctx, member):
            return
        if not await self.check_if_owner(ctx):
            return
        if not await self.top_role_check(ctx, member):
            return
        if not await self.top_role_check_me(ctx, member):
            return
        if not await self.ban_check(ctx):
            return
        await ctx.guild.kick(member, reason=reason)
        await ctx.reply(f"Kicked {member.name}", ephemeral=True)

    @mod.command(name="timeout", description="Timeout a user")
    @commands.has_permissions(manage_roles=True)
    @app_commands.checks.has_permissions(manage_roles=True)
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
        if not await self.check_if_bot(ctx, member):
            return
        if not await self.check_if_owner(ctx):
            return
        if not await self.top_role_check(ctx, member):
            return
        if not await self.top_role_check_me(ctx, member):
            return
        if not await self.ban_check(ctx):
            return
        unmute_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=duration)
        await member.timeout(until=unmute_time, reason=reason)
        await ctx.reply(f"Timed out {member.name}", ephemeral=True)

    @mod.command(name="unban", description="Unban a user")
    @commands.has_permissions(ban_members=True)
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.describe(member="The member to unban")
    @app_commands.describe(reason="The reason for the unban")
    async def unban(self, ctx: commands.Context, member: Member, reason: str) -> None:
        if not await self.check_if_bot(ctx, member):
            return
        if not await self.check_if_owner(ctx):
            return
        if not await self.top_role_check(ctx, member):
            return
        if not await self.top_role_check_me(ctx, member):
            return
        if not await self.ban_check(ctx):
            return
        await ctx.guild.unban(member, reason=reason)
        await ctx.reply(f"Unbanned {member.name}", ephemeral=True)

    @mod.command(name="purge", description="Purge a specified amount of messages.")
    @commands.has_permissions(manage_messages=True)
    @app_commands.checks.has_permissions(manage_messages=True)
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
            self.client.log.error(f"Error: {e}")
            await ctx.reply("An error occurred while purging messages.", ephemeral=True)
            return

    @mod.command(name="lockdown", description="Lockdowns a specified channel.")
    @commands.guild_only()
    @app_commands.guild_only()
    @app_commands.describe(
        channel="The channel to lockdown. Defaults to the current channel."
    )
    @app_commands.describe(reason="The reason for locking down the channel.")
    @commands.has_permissions(manage_channels=True)
    @app_commands.checks.has_permissions(manage_channels=True)
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
        channel = channel or ctx.channel
        try:
            await channel.set_permissions(ctx.guild.default_role, send_messages=False)
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
            self.client.log.error(f"Error: {e}")
            await ctx.send(
                "An error occurred while locking down the channel.", ephemeral=True
            )
            return

    @mod.command(name="unlock", description="Unlocks a specified channel.")
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
        channel = channel or ctx.channel
        try:
            await channel.set_permissions(
                ctx.guild.default_role, send_messages=True, reason=reason
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
            self.client.log.error(f"Error: {e}")
            await ctx.send(
                "An error occurred while unlocking the channel.", ephemeral=True
            )
            return


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Mod(client))
