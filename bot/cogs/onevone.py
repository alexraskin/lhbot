import asyncio
import random

from discord import Embed, Member
from discord.ext import commands


class OneVOne(commands.Cog, name="OneVOne"):
    """
    One V One another user in the server!
    """

    def __init__(self, client: commands.Bot):
        self.client = client
        self.roles = ['tank', 'damage', 'support']

    @commands.command(
        name="1v1",
        description="Random Overwatch Hero 1v1",
    )
    async def one_v_one(
        self,
        ctx: commands.Context,
        user: Member = "",
    ):
        if user is None or "":
            await ctx.send("Please target another user to 1v1")
            return
        hero_one = await self.client.session.get(f"https://overfast-api.tekrop.fr/heroes?role={random.choice(list(self.roles))}&locale=en-us")
        hero_two = await self.client.session.get(f"https://overfast-api.tekrop.fr/heroes?role={random.choice(list(self.roles))}&locale=en-us")

        hero_one_list = []
        hero_one_json = await hero_one.json()
        for i in hero_one_json:
            hero_one_list.append(i['key'].lower())
        
        hero_two_list = []
        hero_two_json = await hero_two.json()

        for i in hero_two_json:
            hero_two_list.append(i['key'].lower())

        hero_one = random.choice(list(hero_one_list))
        hero_two = random.choice(list(hero_two_list))
        
        hero_one_health_data = await self.client.session.get(f"https://overfast-api.tekrop.fr/heroes/{str(hero_one).replace('.', '')}?locale=en-us")
        hero_two_health_data = await self.client.session.get(f"https://overfast-api.tekrop.fr/heroes/{str(hero_two).replace('.', '')}?locale=en-us")

        hero_one_health_json = await hero_one_health_data.json()
        hero_two_health_json = await hero_two_health_data.json()

        hero_one_health = hero_one_health_json['hitpoints']['health']
        hero_one_name = hero_one_health_json['name']
        hero_two_health = hero_two_health_json['hitpoints']['health']
        hero_two_name = hero_two_health_json['name']

        embed = Embed(title="Overwatch Random Hero 1v1", color=0x00FF00, timestamp=ctx.message.created_at)

        embed.add_field(
            name=f"{str(ctx.author.name)} is playing",
            value=f"{hero_one_name} with {hero_one_health} health",
        )
        embed.add_field(
            name=f"{user} is playing", value=f"{hero_two_name} with {hero_two_health} health"
        )
        embed.set_footer(text=self.client.footer)
        first_message = await ctx.send(embed=embed)

        while hero_one_health > 0 and hero_two_health > 0:
            second_embed = Embed(title="Overwatch Random Hero 1v1", color=0x00FF00, timestamp=ctx.message.created_at)
            hero_one_health -= random.randint(0, hero_one_health)
            hero_two_health -= random.randint(0, hero_two_health)
            await asyncio.sleep(1)
            second_embed.add_field(
                name=f"{ctx.author.name}",
                value=f"Playing {hero_one_name} with {hero_one_health} health",
            )
            second_embed.add_field(
                name=f"{user}",
                value=f"Playing {hero_two_name} with {hero_two_health} health",
            )
            second_embed.set_footer(text=self.client.footer)
            final = await first_message.edit(embed=second_embed)
            win_embed = Embed(title="Overwatch Random Hero 1v1", color=0x00FF00, timestamp=ctx.message.created_at)
            win_embed.set_footer(text=self.client.footer)

        if hero_one_health == 0:
            win_embed.add_field(name=ctx.author, value=f"Won, playing {hero_one_name}!")
            win_embed.add_field(name=user, value=f"Lost, playing {hero_two_name}")

        elif hero_two_health == 0:
            win_embed.add_field(name=ctx.author, value=f"Lost, playing {hero_one_name}")
            win_embed.add_field(name=user, value=f"Won, playing {hero_two_name}")

        await final.edit(embed=win_embed)



async def setup(client: commands.Bot):
    await client.add_cog(OneVOne(client))
