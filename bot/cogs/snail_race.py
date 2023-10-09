import asyncio
import random
from typing import Dict, List, Optional, Union

import discord
from discord import Interaction, Member, app_commands
from discord.ext import commands

shuffled_participants: List = []
running_guilds: List = []
snail_positions: Dict = {}


class RaceButton(discord.ui.View):
    def __init__(self, *, timeout: int = 45):
        super().__init__(timeout=timeout)

    @discord.ui.button(label="Join Race", style=discord.ButtonStyle.blurple, emoji="🐌")
    async def race_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        global shuffled_participants
        await interaction.response.defer()

        if interaction.user.id not in shuffled_participants:
            await interaction.followup.send(
                f"You've entered into the race!", ephemeral=True
            )
            shuffled_participants.append(interaction.user.id)
        else:
            await interaction.followup.send(
                content="You already joined the race! 🐌", ephemeral=True
            )


class SnailRace(commands.Cog, name="Snail Racing"):
    def __init__(self, client: commands.Bot) -> None:
        self.client: commands.Bot = client

    async def randomize_snails(self) -> None:
        global shuffled_participants
        shuffled_participants = random.sample(
            shuffled_participants, len(shuffled_participants)
        )
        return shuffled_participants

    async def simulate_race(self, interaction: Interaction) -> None:
        global snail_positions
        global shuffled_participants
        winner: Member = None
        race_length: int = 10
        if len(shuffled_participants) <= 0:
            await interaction.channel.send(content="No one joined the race! 😢")
            return
        message = await interaction.channel.send("The Race is starting! 🚩")
        shuffled_participants.append(self.client.user.id)
        randomize_snail = await self.randomize_snails()
        snail_positions = {user_id: 0 for user_id in randomize_snail}
        while not winner:
            for user_id in snail_positions:
                snail_positions[user_id] += random.randint(1, 3)

                if snail_positions[user_id] >= race_length:
                    winner = self.client.get_user(user_id)
                    break
            race_progress: str = ""
            for user_id, position in snail_positions.items():
                user = self.client.get_user(user_id)
                race_progress += f"[{user.name}]: {'🐌' * position}\n"
            await asyncio.sleep(random.randint(1, 3))
            await message.edit(
                content=f"🏁 **The race is now in progress!** 🏁\n{race_progress}"
            )
        embed = discord.Embed(
            title="Congratulations!",
            description=f"{winner.mention} won the race! 🏁",
            color=discord.Color.green(),
            timestamp=interaction.created_at,
        )
        embed.set_thumbnail(url=winner.display_avatar.url)
        await interaction.channel.send(embed=embed)

    @app_commands.command(name="race", description="Start a Snail Race")
    @app_commands.guild_only()
    async def race(self, interaction: Interaction, delay: Optional[int] = 10) -> None:
        global running_guilds
        view: RaceButton = RaceButton()
        if interaction.guild.id in running_guilds:
            await interaction.response.send_message(
                content="A race is already running in this server!",
                ephemeral=True,
            )
            return
        if delay > 30:
            await interaction.response.send_message(
                "Delay must be less than 30 seconds",
                ephemeral=True,
            )
            return
        running_guilds.append(interaction.guild.id)
        await interaction.response.send_message(
            content=f"{interaction.user.mention} has started a race.\nRace will start in {delay} seconds.",
            view=view,
        )
        await asyncio.sleep(delay)
        await self.simulate_race(interaction)

    @commands.Cog.listener()
    async def on_app_command_completion(
        self,
        interaction: discord.Interaction,
        command: Union[app_commands.Command, app_commands.ContextMenu],
    ) -> None:
        try:
            snail_positions.clear()
            shuffled_participants.clear()
            running_guilds.remove(interaction.guild.id)
        except ValueError:
            pass
        self.client.logger.info(f"{interaction.user} used {command}")


async def setup(client: commands.Bot) -> None:
    await client.add_cog(SnailRace(client))
