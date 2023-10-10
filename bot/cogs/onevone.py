import asyncio
import random
from typing import Union

from discord import Embed, Member, app_commands, User, File
from discord.ext import commands

from utils.generatevs import GenerateVS

class OneVOne(commands.Cog, name="OneVOne"):
    def __init__(self, client: commands.Bot):
        self.client: commands.AutoShardedBot = client
        self.roles: list = ["tank", "damage", "support"]

    @commands.hybrid_command(
        name="1v1",
        description="Random Overwatch Hero 1v1",
        aliases=["onevone", "1vs1"],
    )
    @commands.guild_only()
    @app_commands.guild_only()
    async def one_v_one(
        self,
        ctx: commands.Context,
        user: Union[Member, User]
    ):
        if user is None or "":
            await ctx.send("Please target another user to 1v1")
            return
        hero_one = await self.client.session.get(
            f"https://overfast-api.tekrop.fr/heroes?role={random.choice(list(self.roles))}&locale=en-us"
        )
        hero_two = await self.client.session.get(
            f"https://overfast-api.tekrop.fr/heroes?role={random.choice(list(self.roles))}&locale=en-us"
        )

        hero_one_list = []
        hero_one_json = await hero_one.json()
        for i in hero_one_json:
            hero_one_list.append(i["key"].lower())

        hero_two_list = []
        hero_two_json = await hero_two.json()

        for i in hero_two_json:
            hero_two_list.append(i["key"].lower())

        hero_one = random.choice(list(hero_one_list))
        hero_two = random.choice(list(hero_two_list))

        hero_one_health_data = await self.client.session.get(
            f"https://overfast-api.tekrop.fr/heroes/{str(hero_one).replace('.', '')}?locale=en-us"
        )
        hero_two_health_data = await self.client.session.get(
            f"https://overfast-api.tekrop.fr/heroes/{str(hero_two).replace('.', '')}?locale=en-us"
        )
        hero_one_health_json = await hero_one_health_data.json()
        hero_two_health_json = await hero_two_health_data.json()
        hero_one_health = hero_one_health_json["hitpoints"]["health"]
        hero_one_name = hero_one_health_json["name"]
        hero_two_health = hero_two_health_json["hitpoints"]["health"]
        hero_two_name = hero_two_health_json["name"]
        hero_one_image = await self.client.session.get(hero_one_health_json["portrait"])
        hero_two_image = await self.client.session.get(hero_two_health_json["portrait"])
        hero_one_image = await hero_one_image.read()
        hero_two_image = await hero_two_image.read()

        image = GenerateVS(hero_one_image, hero_two_image)
        file = File(image.generate_vs_image(), filename="vs.png")

        embed = Embed(
            title="Overwatch Random Hero 1v1",
            color=0x00FF00,
            timestamp=ctx.message.created_at,
        )
        embed.set_image(url="attachment://vs.png")
        embed.add_field(
            name=f"{str(ctx.author.display_name)}",
            value=f"You are playing **{hero_one_name}** with **{hero_one_health}** health",
        )
        embed.add_field(
            name=f"{user.name}",
            value=f"Is play **{hero_two_name}** with **{hero_two_health}** health",
        )
        message = await ctx.send(embed=embed, file=file)
        game = True
        while game:
            for _ in range(3):
              hero_one_health -= random.randint(0, hero_one_health)
              hero_two_health -= random.randint(0, hero_two_health)
              if hero_one_health == 0 or hero_two_health == 0:
                  game = False
                  break
              await asyncio.sleep(random.randint(1, 3))
              embed.set_field_at(0,
                  name=f"{ctx.author.display_name}",
                  value=f"Spectating **{hero_one_name}** with **{hero_one_health}** health",
              )
              embed.set_field_at(1,
                  name=f"{user.name}",
                  value=f"Spectating **{hero_two_name}** with **{hero_two_health}** health",
              )
              embed.set_image(url="attachment://vs.png")
              await message.edit(embed=embed)
        if hero_one_health == 0:
            embed.set_field_at(0, name=ctx.author.display_name, value=f"**Won**, playing **{hero_one_name}**!")
            embed.set_field_at(1, name=user.name, value=f"**Lost**, playing **{hero_two_name}**!")

        elif hero_two_health == 0:
            embed.set_field_at(0, name=ctx.author.display_name, value=f"**Lost**, playing **{hero_one_name}**!")
            embed.set_field_at(1, name=user.name, value=f"**Won**, playing **{hero_two_name}**!")
        embed.set_image(url="attachment://vs.png")
        await message.edit(embed=embed)
        image.delete_images()


async def setup(client: commands.Bot):
    await client.add_cog(OneVOne(client))
