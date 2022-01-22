import random

from discord import Embed
from discord.ext import commands


class OverwatchAPI(commands.Cog, name="Overwatch"):
    """Overwatch specify commands"""

    def __init__(self, client):
        self.client = client
        self.base_url = 'https://owapi.io'

    @commands.command(
        name="owstats",
        aliases=["stats", "profile"],
        description="?owstats pc us Jay3#11894"
    )
    async def get_overwatch_profile(self, ctx, *, info=None):
        if info is None:
            embed = Embed(
                title="Please Enter A Profile!",
                color=random.randint(
                    0,
                    0xFFFFFF))
            embed.add_field(
                name='Example:',
                value="!owstats pc us Jay3#11894",
                inline=True
            )
            embed.add_field(
                name='Platform of user:',
                value="pc/xbl/psn/nintendo-switch",
                inline=True
            )
            embed.add_field(
                name='Region of player:',
                value="us/eu/kr/cn/global",
                inline=True
            )
            embed.add_field(
                name='BattleTag of user:',
                value="Jay3#11894",
                inline=True
            )
            await ctx.send(embed=embed)
        else:
            platform, region, profile = str(info).split(" ")
            url = f'{self.base_url}/profile/{platform}/{region}/{str(profile).replace("#", "-")}'
            async with self.client.session.get(url) as response:
                user_data = await response.json()
                if "message" in user_data:
                    embed = Embed(title="Unable to find profile",
                                  color=random.randint(0, 0xFFFFFF)
                                  )
                    await ctx.send(embed=embed)
                if not user_data["private"]:
                    embed = Embed(color=random.randint(0, 0xFFFFFF))
                    embed.set_author(
                        name=user_data["username"],
                        icon_url=user_data["portrait"])
                    embed.add_field(
                        name='Player Level:',
                        value=user_data["level"],
                        inline=True
                    )
                    embed.add_field(
                        name='Competitive Tank Rating:',
                        value=user_data["competitive"]["tank"]["rank"],
                        inline=True
                    )
                    embed.add_field(
                        name='Competitive Damage Rating:',
                        value=user_data["competitive"]["damage"]["rank"],
                        inline=True
                    )
                    embed.add_field(
                        name='Competitive Support Rating:',
                        value=user_data["competitive"]["support"]["rank"],
                        inline=True
                    )
                    embed.set_footer(text=f"Requested by {ctx.message.author}")
                    await ctx.send(embed=embed)
                if user_data["private"]:
                    embed = Embed(color=random.randint(0, 0xFFFFFF))
                    embed.set_author(
                        name=f'{user_data["username"]} is not a public profile',
                        icon_url=user_data["portrait"])
                    await ctx.send(embed=embed)


def setup(client):
    client.add_cog(OverwatchAPI(client))
