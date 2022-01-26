import random

from discord import Embed
from discord.ext import commands


class OverwatchAPI(commands.Cog, name="Overwatch"):
    """Overwatch specify commands"""

    def __init__(self, client):
        """
        The __init__ function is the constructor for a class. It initializes the attributes of an object. In this case, it initializes
        the client attribute.

        :param self: Used to access variables that belong to the class.
        :param client: Used to store the reference to the client object.
        :return: a new instance of the class.

        """
        self.client = client
        self.base_url = "https://owapi.io"

    @commands.command(
        name="owstats",
        aliases=["stats", "profile"],
        description="?owstats pc us Jay3#11894",
    )
    async def get_overwatch_profile(self, ctx, *, info=None):
        """
        The get_overwatch_profile function specifically retrieves the Overwatch profile of a user.
        It takes in three parameters, which are the context, and two strings. The first string is for platform (pc/xbl/psn),
        and the second string is for region (us/eu/kr). It then splits these two strings into three separate variables.

        :param self: Used to access variables that belong to the class.
        :param ctx: Used to get the context of where the message was sent.
        :param *: Used to pass in unlimited parameters to this function.
        :param info=None: Used to pass in the user's information.
        :return: :.

        """
        if info is None:
            embed = Embed(
                title="Please Enter A Profile!", color=random.randint(0, 0xFFFFFF)
            )
            embed.add_field(
                name="Example:", value="!owstats pc us Jay3#11894", inline=True
            )
            embed.add_field(
                name="Platform of user:",
                value="pc/xbl/psn/nintendo-switch",
                inline=True,
            )
            embed.add_field(
                name="Region of player:", value="us/eu/kr/cn/global", inline=True
            )
            embed.add_field(name="BattleTag of user:", value="Jay3#11894", inline=True)
            await ctx.send(embed=embed)
        else:
            platform, region, profile = str(info).split(" ")
            url = f'{self.base_url}/profile/{platform}/{region}/{str(profile).replace("#", "-")}'
            async with self.client.session.get(url) as response:
                user_data = await response.json()
                if "message" in user_data:
                    embed = Embed(
                        title="Unable to find profile",
                        color=random.randint(0, 0xFFFFFF),
                    )
                    await ctx.send(embed=embed)
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
                    embed.set_footer(text=f"Requested by {ctx.message.author}")
                    await ctx.send(embed=embed)
                if user_data["private"]:
                    embed = Embed(color=random.randint(0, 0xFFFFFF))
                    embed.set_author(
                        name=f'{user_data["username"]} is not a public profile',
                        icon_url=user_data["portrait"],
                    )
                    await ctx.send(embed=embed)


def setup(client):
    """
    The setup function is used to register the commands that will be used in the bot.
    This function is run when you load a cog, and it allows you to use commands in your cogs.

    :param client: Used to pass in the discord client, which is used to interact with the Discord API.
    :return: a dictionary with the following keys:.

    """
    client.add_cog(OverwatchAPI(client))
