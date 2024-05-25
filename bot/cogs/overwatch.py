from __future__ import annotations

import asyncio
import random
from typing import TYPE_CHECKING, Literal, Union

from discord import Colour, Embed, Interaction, Member, User, app_commands
from discord.ext import commands
from utils.bot_utils import get_time_string
from utils.reinquotes import quotes

if TYPE_CHECKING:
    from ..bot import LhBot


class OverwatchAPI(commands.Cog):
    """Overwatch specify commands"""

    def __init__(self, client: LhBot):
        self.client: LhBot = client
        self.rein_quotes = quotes.split("\n")
        self.base_url = "https://owapi.io"

    @app_commands.command(
        name="owstats",
        description="Get overwatch profile details",
    )
    @app_commands.describe(
        platform="The platform the user is on",
    )
    @app_commands.describe(
        region="The region the user is in",
    )
    @app_commands.describe(
        battletag="The battletag of the user (ex. LhCloudy#1234)",
    )
    async def get_overwatch_profile(
        self,
        interaction: Interaction,
        platform: Literal["pc", "xbl", "psn", "nintendo-switch"],
        region: Literal["us", "eu", "kr"],
        battletag: str,
    ) -> None:
        """
        Get Overwatch profile details
        """
        url = f'{self.base_url}/profile/{platform}/{region}/{str(battletag).replace("#", "-")}'
        await interaction.response.defer()
        async with self.client.session.get(url) as response:
            if response.status != 200:
                self.client.logger.error("Error getting Overwatch profile")
                await interaction.followup.send(
                    f"Overwatch API is currently down. Please try again later.",
                    ephemeral=True,
                )
                return
            else:
                user_data = await response.json()
                if "message" in user_data:
                    await interaction.followup.send(
                        "Unable to find profile", ephemeral=True
                    )
                if not user_data["private"]:
                    embed = Embed(color=random.randint(0, 0xFFFFFF))
                    embed.set_author(
                        name=user_data["username"], icon_url=user_data["portrait"]
                    )
                    embed.add_field(
                        name="Player Level:", value=user_data["level"], inline=True
                    )
                    embed.add_field(
                        name="Competitive Tank Rating:",
                        value=user_data["competitive"]["tank"]["rank"],
                        inline=True,
                    )
                    embed.add_field(
                        name="Competitive Damage Rating:",
                        value=user_data["competitive"]["damage"]["rank"],
                        inline=True,
                    )
                    embed.add_field(
                        name="Competitive Support Rating:",
                        value=user_data["competitive"]["support"]["rank"],
                        inline=True,
                    )
                    embed.set_footer(text="Provided by owapi.io")
                    await interaction.followup.send(embed=embed)
                if user_data["private"]:
                    embed = Embed(color=random.randint(0, 0xFFFFFF))
                    embed.set_author(
                        name=f'{user_data["username"]} is not a public profile',
                        icon_url=user_data["portrait"],
                    )
                    embed.set_footer(text="Provided by owapi.io")
                    await interaction.followup.send(embed=embed)

    @commands.command(name="reinquote", description="Random Rein Quote")
    @commands.guild_only()
    @app_commands.guild_only()
    async def random_rein_quote(self, ctx: commands.Context) -> None:
        """
        Random Rein Quote
        """
        embed = Embed(
            color=random.randint(0, 0xFFFFFF),
        )
        embed.add_field(
            name="Random Rein Quote:",
            value=random.choice(list(self.rein_quotes)),
            inline=True,
        )
        embed.set_footer(text=f"Requested by {ctx.message.author}")
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="shatter", description="Shatter a user")
    @commands.guild_only()
    @app_commands.guild_only()
    async def shatter(
        self, ctx: commands.Context, target_user: Union[Member, User]
    ) -> None:
        lh_cloudy_list = ["@127122091139923968", "lhcloudy", "cloudy", "lhcloudy27"]
        lh_cloudy_block_list = [
            "Blocked.. immune to your shatter!",
            "LhCloudy is immune to your shatter!",
            "Blocked - MTD",
            "ez block... L + ratio",
            "sr peak check?",
        ]

        miss = "You shattered no one, so it missed. Your team is now flaming you, and the enemy mercy typed MTD."

        if target_user.name in lh_cloudy_list:
            await ctx.send(random.choice(list(lh_cloudy_block_list)))
            return

        random.seed(get_time_string())
        match random.choice(["hit", miss, "was blocked by"]):
            case "hit":
                message = f"Your shatter hit {target_user.mention}! 💥🔨"
                color = Colour.green()
                emoji = "💥"

            case "was blocked by":
                message = f"Your shatter was blocked by {target_user.mention}, the enemy mercy typed MTD."
                color = Colour.red()
                emoji = "🧱"

            case _:
                message = miss
                color = Colour.red()
                emoji = "🤡"

        embed = Embed(
            description=message,
            timestamp=ctx.message.created_at,
        )
        embed.colour = color
        embed.set_author(
            name="Earthshatter!",
            icon_url=f"https://i.gyazo.com/cc82531d22c9b608d745b296048c8f48.png",
        )
        embed.set_footer(text=f"Requested by {ctx.message.author.display_name}")
        d_message = await ctx.send(embed=embed)
        await d_message.add_reaction(emoji)

    @commands.hybrid_command(
        name="nano", description="Nano Boost a user in the server!"
    )
    @commands.guild_only()
    @app_commands.guild_only()
    async def nano(self, ctx: commands.Context, target_user: Union[Member, User]):
        nano_boost_sayings = [
            "Nano Boost administered",
            "You're powered up, get in there",
            "Why would you nano a purple 50 hp Reinhardt?",
        ]

        if target_user == None or target_user == "":
            return

        if len(target_user) > 500:
            await ctx.send("Username is too long!")
            return

        random.seed(get_time_string())
        embed = Embed(
            description=f"{random.choice(list(nano_boost_sayings))} {target_user.mention}",
            color=random.randint(0, 0xFFFFFF),
        )
        embed.set_author(
            name="Nano Boost!",
            icon_url=f"https://i.gyazo.com/ac15d47b93ebf141deb5b8b7846e46a5.png",
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="lamp", description="Lamp a user in the server!")
    @commands.guild_only()
    @app_commands.guild_only()
    async def lamp(self, ctx: commands.Context, target_user: Union[Member, User]):
        random.seed(get_time_string())
        lamp_sayings = [
            f"Get in the Immortality Field {target_user.mention}!",
            f"Step inside {target_user.mention}, stay alive",
            f"Get inside, {target_user.mention}!",
            f"Get in here, {target_user.mention}!",
        ]
        lamp_answers = [
            str(
                "Congratulations, you lamped Cloudy's dead corpse, now he's flaming you on stream LULW"
            ),
            "You lamped a Mercy Main and now she wants to duo ;)",
            "Immortality bubble's down",
            "Immortality field destroyed!",
            "Immortality field down",
            "Immortality field's down. Watch yourself!",
        ]

        await ctx.send(random.choice(lamp_sayings))
        await asyncio.sleep(2)
        await ctx.send(random.choice(lamp_answers))

    @commands.command(name="boop", description="Boop a user in the server!")
    async def boop(self, ctx: commands.Context, target_user: Union[Member, User]):
        boop_sayings = [
            "That was the sound of science",
            "I could do this with my eyes closed",
            "I'm feeling some good vibrations",
            "When the music hits, you feel no pain",
            "Ah, garoto",
            "Hah! Too good",
            "Haha! Served",
            "Whoo! Check yourself",
            "Get back",
            "Push off",
            "Step to this",
        ]
        random.seed(get_time_string())

        await ctx.send(f"{random.choice(list(boop_sayings))}, {target_user.mention}")


async def setup(client: LhBot):
    await client.add_cog(OverwatchAPI(client))
