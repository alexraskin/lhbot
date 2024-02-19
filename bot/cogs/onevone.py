from __future__ import annotations

import asyncio
import random
from typing import Union, TYPE_CHECKING

from discord import Embed, Member, app_commands, User, File, Colour
from discord.ext import commands

from utils.generatevs import GenerateVS

if TYPE_CHECKING:
    from ..bot import LhBot


class OverwatchHero:
    API_BASE_URL = "https://overfast-api.tekrop.fr/heroes"

    def __init__(
        self,
        key: str,
        name: str,
        portrait: str,
        role: str,
        health: int,
        story: str,
        session,
    ):
        self.key = key
        self.name = name
        self.portrait = portrait
        self.role = role
        self.health = health
        self.story = story
        self.session = session

    @staticmethod
    def calculate_damage(health: float) -> int:
        min_damage = 10
        max_damage = 50

        damage = random.randint(min_damage, max_damage)

        damage = damage * (health / 100)

        return damage

    @classmethod
    async def get_random_hero(cls, session) -> Union[str, None]:
        url = f"{cls.API_BASE_URL}?role={cls.get_random_role()}&locale=en-us"
        async with session.get(url) as response:
            if response.status == 200:
                hero_data = await response.json()
                hero_list = [hero_data["key"] for hero_data in hero_data]
                return random.choice(hero_list)

    @classmethod
    async def fetch_hero_data(cls, session) -> Union[OverwatchHero, None]:
        random_hero = await cls.get_random_hero(session=session)
        url = f"{cls.API_BASE_URL}/{random_hero.replace('.', '')}?locale=en-us"
        async with session.get(url) as response:
            if response.status == 200:
                hero_data = await response.json()
                return cls(
                    key=hero_data.get("key"),
                    name=hero_data.get("name"),
                    portrait=hero_data.get("portrait"),
                    role=hero_data.get("role"),
                    health=hero_data["hitpoints"].get("total"),
                    story=hero_data["story"].get("summary"),
                    session=session,
                )
            else:
                return None

    async def fetch_hero_image(self) -> Union[bytes, None]:
        async with self.session.get(self.portrait) as response:
            if response.status == 200:
                return await response.read()
            else:
                return None

    @classmethod
    def get_random_role(cls) -> str:
        roles = ["tank", "damage", "support"]
        return random.choice(roles)

    def __str__(self):
        return f"{self.name}"


class OneVOne(commands.Cog):
    def __init__(self, client: LhBot):
        self.client: LhBot = client
        self.roles: list = ["tank", "damage", "support"]

    @commands.hybrid_command(
        name="1v1",
        description="Random Overwatch Hero 1v1",
        aliases=["onevone", "1vs1"],
    )
    @commands.guild_only()
    @app_commands.guild_only()
    async def one_v_one(self, ctx: commands.Context, user: Union[Member, User]):
        if user is None or "":
            await ctx.send("Please target another user to 1v1")
            return
        hero_one = await OverwatchHero.fetch_hero_data(self.client.session)
        hero_two = await OverwatchHero.fetch_hero_data(self.client.session)
        image = GenerateVS(
            await hero_one.fetch_hero_image(), await hero_two.fetch_hero_image()
        )
        file = File(image.generate_vs_image(), filename="vs.png")

        embed = Embed(
            title="Overwatch Random Hero 1v1",
            color=0x00FF00,
            timestamp=ctx.message.created_at,
        )
        embed.set_image(url="attachment://vs.png")
        embed.add_field(
            name=f"{str(ctx.author.display_name)}",
            value=f"You are playing **{hero_one.name}** with **{hero_one.health}** health",
        )
        embed.add_field(
            name=f"{user.name}",
            value=f"Is play **{hero_two.name}** with **{hero_two.health}** health",
        )
        message = await ctx.send(embed=embed, file=file)
        hero_one_health = hero_one.health
        hero_two_health = hero_two.health
        while hero_one_health > 0 and hero_two_health > 0:
            for _ in range(3):
                damage_to_hero_one = hero_two.calculate_damage(health=hero_two_health)
                damage_to_hero_two = hero_one.calculate_damage(health=hero_one_health)

                hero_one_health -= damage_to_hero_one
                hero_two_health -= damage_to_hero_two

                hero_one_health = max(0, round(hero_one_health))
                hero_two_health = max(0, round(hero_two_health))

                if hero_one_health <= 0 or hero_two_health <= 0:
                    break

                await asyncio.sleep(random.randint(1, 3))
                embed.set_field_at(
                    0,
                    name=f"{ctx.author.display_name}",
                    value=f"Spectating **{hero_one.name}** with **{round(hero_one_health)}** health",
                )
                embed.set_field_at(
                    1,
                    name=f"{user.name}",
                    value=f"Spectating **{hero_two.name}** with **{round(hero_two_health)}** health",
                )
                embed.set_image(url="attachment://vs.png")
                await message.edit(embed=embed)
        if hero_one_health <= 0:
            embed.set_field_at(
                0,
                name=ctx.author.display_name,
                value=f"**Won**, playing **{hero_one.name}**!",
            )
            embed.set_field_at(
                1, name=user.name, value=f"**Lost**, playing **{hero_two.name}**!"
            )

        else:
            embed.set_field_at(
                0,
                name=ctx.author.display_name,
                value=f"**Lost**, playing **{hero_one.name}**!",
            )
            embed.set_field_at(
                1, name=user.name, value=f"**Won**, playing **{hero_two.name}**!"
            )
        embed.set_image(url="attachment://vs.png")
        await message.edit(embed=embed)
        image.delete_images()

    @one_v_one.error
    async def one_v_one_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.UserNotFound):
            await ctx.send("Please target another user to 1v1")
        else:
            raise error

    @commands.hybrid_command(name="1v1info", description="Random Overwatch Hero")
    @commands.guild_only()
    @app_commands.guild_only()
    async def one_v_one_info(self, ctx: commands.Context):
        embed = Embed(
            title="Welcome to the Overwatch Hero Showdown!",
            description="Engage in epic battles with Overwatch heroes.",
            color=Colour.blurple(),
            timestamp=ctx.message.created_at,
        )

        embed.add_field(
            name="How to Play",
            value="1. Two Overwatch heroes will be randomly selected.\n"
            "2. They will take turns attacking each other.\n"
            "3. The game ends when one hero's health drops to 0\n"
            "4. The player with the winning hero is declared the champion.",
        )

        embed.add_field(
            name="Commands",
            value="Use the following command to start a game:\n"
            "`!1v1 <@user>`\n or \n`/1v1 <@user>`\n",
        )

        embed.add_field(
            name="Additional Notes",
            value="- Hero damage is influenced by their health and a touch of randomness.\n"
            "- You might need some luck to secure victory!\n"
            "- Enjoy the Overwatch-themed showdown!",
        )

        embed.set_image(url="https://i.gyazo.com/de5ef721b1e5f33c3995dbabad22026d.png")
        embed.set_footer(text="All data is provided by https://overfast-api.tekrop.fr/")
        await ctx.send(embed=embed)


async def setup(client: LhBot):
    await client.add_cog(OneVOne(client))
