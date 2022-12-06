import asyncio
import random

from discord import Embed, Member
from discord.ext import commands


class OneVOne(commands.Cog, name="OneVOne"):
    def __init__(self, client: commands.Bot):

        self.client = client

        self.tank_heros = {
            "D.Va": 650,
            "Doomfist": 450,
            "Orisa": 550,
            "Reinhardt": 665,
            "Roadhog": 700,
            "Sigma": 550,
            "Winston": 550,
            "Wrecking Ball": 750,
            "Zarya": 475,
            "Junker Queen": 425,
        }
        self.dmg_heros = {
            "Ashe": 200,
            "Bastion": 200,
            "Doomfist": 450,
            "Genji": 250,
            "Hanzo": 175,
            "Junkrat": 200,
            "McCree": 225,
            "Mei": 250,
            "Pharah": 200,
            "Reaper": 250,
            "Soldier: 76": 200,
            "Sombra": 200,
            "Symmetra": 200,
            "Torbjörn": 200,
            "Tracer": 150,
            "Widowmaker": 175,
        }
        self.support_heros = {
            "Ana": 200,
            "Baptiste": 200,
            "Brigitte": 350,
            "Kiriko": 200,
            "Lúcio": 200,
            "Mercy": 200,
            "Moira": 200,
            "Zenyatta": 200,
        }

    @commands.command(
        name="1v1",
        description="Random Hero 1v1",
    )
    async def one_v_one(
        self, ctx: commands.Context, user: Member,
    ):
        if user is None:
            await ctx.send("Please target another user to 1v1")
            return

        hero_one = self.get_random_hero()
        hero_two = self.get_random_hero()

        hero_one_health = self.get_hero_health(hero_one)
        hero_two_health = self.get_hero_health(hero_two)

        embed = Embed(title="Overwatch Random Hero 1v1", color=0x00FF00)

        embed.add_field(name=f"{str(ctx.author).strip('#')} is playing", value=f"{hero_one} with {hero_one_health} health")
        embed.add_field(name=f"{user} is playing", value=f"{hero_two} with {hero_two_health} health")

        first_message = await ctx.send(embed=embed)

        while hero_one_health > 0 and hero_two_health > 0:
            second_embed = Embed(title="Overwatch Random Hero 1v1", color=0x00FF00)
            hero_one_health -= random.randint(0, hero_one_health)
            hero_two_health -= random.randint(0, hero_two_health)
            await asyncio.sleep(1)
            second_embed.add_field(name=f"{ctx.author}", value=f"Playing {hero_one} with {hero_one_health} health")
            second_embed.add_field(name=f"{user}", value=f"Playing {hero_two} with {hero_two_health} health")
            final = await first_message.edit(embed=second_embed)
            win_embed = Embed(title="Overwatch Random Hero 1v1", color=0x00FF00)
        if hero_one_health == 0:
          win_embed.add_field(name=ctx.author, value=f"Won, playing {hero_one}!")
          win_embed.add_field(name=user, value=f"Lost, playing {hero_two}")
        elif hero_two_health == 0:
          win_embed.add_field(name=ctx.author, value=f"Lost, playing {hero_one}")
          win_embed.add_field(name=user, value=f"Won, playing {hero_two}")
        
        await final.edit(embed=win_embed)
              


    def get_random_hero(self) -> str:
        all = self.tank_heros | self.dmg_heros | self.support_heros
        return random.choice(list(all.keys()))

    def get_hero_health(self, hero) -> int:
        if hero in self.tank_heros:
            return self.tank_heros[hero]
        elif hero in self.dmg_heros:
            return self.dmg_heros[hero]
        elif hero in self.support_heros:
            return self.support_heros[hero]
        else:
            return 0


async def setup(client: commands.Bot):
    await client.add_cog(OneVOne(client))
