import asyncio
import random

from discord import Embed
from discord.ext import commands
from utils.bot_utils import get_time_string
from utils.reinquotes import quotes


class OverwatchAPI(commands.Cog, name="Overwatch"):
    """Overwatch specify commands"""

    def __init__(self, client: commands.Bot):
        self.client = client
        self.rein_quotes = quotes.split("\n")
        self.base_url = "https://owapi.io"

    @commands.cooldown(1, 20, commands.BucketType.user)
    @commands.command(
        name="owstats",
        aliases=["stats", "profile"],
        description="Get overwatch profile details. EX: !owstats pc us Jay3#11894",
    )
    async def get_overwatch_profile(self, ctx: commands.Context, info=None) -> Embed:
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
                if response.status != 200:
                    self.client.logger.error("Error getting Overwatch profile")
                    await ctx.send(
                        f"Overwatch API is currently down. Please try again later."
                    )
                    return
                else:
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

    @commands.command(name="reinquote", description="Random Rein Quote")
    async def random_rein_quote(self, ctx: commands.Context) -> Embed:
        
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
    async def shatter(self, ctx: commands.Context, target_user: str = None):
        lh_cloudy_list = ["@127122091139923968", "lhcloudy", "cloudy", "lhcloudy27"]
        lh_cloudy_block_list = [
            "Blocked.. cloudy is immune to your shatter!",
            "LhCloudy is immune to your shatter!",
            "Blocked - MTD",
            "ez block... L + ratio",
            "sr peak check?",
        ]

        miss = "You shattered no one, so it missed. Your team is now flaming you, and the enemy mercy typed MTD."

        

        if ctx.interaction:
            if target_user is None or target_user == "":
                await ctx.send(miss)
                return

            if target_user in lh_cloudy_list:
                await ctx.send(random.choice(lh_cloudy_block_list))
                return

        if target_user == None or target_user == "":
            await ctx.send(miss)
            return

        if len(target_user) > 500:
            await ctx.send("Username is too long!")
            return

        if target_user.lower() in lh_cloudy_list:
            await ctx.send(random.choice(list(lh_cloudy_block_list)))
            return

        random.seed(get_time_string())
        roll_shatter = random.randint(0, 100)
        did_shatter = "hit" if roll_shatter < 25 else "was blocked by"

        embed = Embed(
            description=f"Your shatter {did_shatter} {target_user}.",
            color=random.randint(0, 0xFFFFFF),
        )
        embed.set_author(
            name="Shatter!",
            icon_url=f"https://i.gyazo.com/2efdc733e050027c24b6670aaf4f9684.png",
        )
        embed_message = await ctx.send(embed=embed)
        if did_shatter == "hit":
            await embed_message.add_reaction("🔨")
        else:
            await embed_message.add_reaction("🥶")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="nano", description="Nano Boost a user in the server!")
    async def nano_execute(self, ctx, target_user=None):
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
            description=f"{random.choice(list(nano_boost_sayings))} {target_user}",
            color=random.randint(0, 0xFFFFFF),
        )
        embed.set_author(
            name="Nano Boost!",
            icon_url=f"https://i.gyazo.com/ac15d47b93ebf141deb5b8b7846e46a5.png",
        )
        await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="lamp", description="Lamp a user in the server!")
    async def lamp(self, ctx, target_user=None):
        random.seed(get_time_string())
        lamp_sayings = [
            f"Get in the Immortality Field {target_user}!",
            f"Step inside {target_user}, stay alive",
            f"Get inside, {target_user}!",
            f"Get in here, {target_user}!",
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

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="boop", description="Boop a user in the server!")
    async def boop(self, ctx, target_user=None):
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
        
        await ctx.send(f"{random.choice(list(boop_sayings))}, {target_user}")


async def setup(client):
    await client.add_cog(OverwatchAPI(client))
