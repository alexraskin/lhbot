import datetime
import sys

from discord import Embed
from discord.ext import commands

sys.path.append("../bot/")
from utils.emojis import random_emoji


class LhCloudy(commands.Cog, name="LhCloudy"):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.group(invoke_without_command=True)
    async def twitch(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(
                f"Please use `{self.client.config.bot_prefix}twitch help` to see the list of commands."
            )

    @twitch.command(name="1frame")
    async def one_frame(self, ctx):
        url = "https://www.twitch.tv/lhcloudy27/clip/AbstruseKindRuffFutureMan-dLWae-FGvNag2jtK"
        await ctx.typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @twitch.command(name="360")
    async def three_sixty(self, ctx):
        url = "https://clips.twitch.tv/GentleObservantJalapenoLeeroyJenkins-Z53XsWoa2wamtAlB"
        await ctx.typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @twitch.command(name="ball")
    async def ball(self, ctx):
        url = "https://gyazo.com/7f7dc8b93c4a77054104ee3d2ed9a134"
        await ctx.typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @twitch.command(name="bhop")
    async def bhop(self, ctx):
        url = "https://www.twitch.tv/twitch27/clip/ToughAttractiveHerbsBlargNaut-GvSHZicwk7Sjs13X"
        await ctx.typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @twitch.command(name="lhfurry")
    async def lhfurry(self, ctx):
        url = "https://i.gyazo.com/3ae8376713000ab829a2853d0f31e6f2.png"
        await ctx.typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @twitch.command(name="bhop2")
    async def bhop_two(self, ctx):
        url = "https://clips.twitch.tv/BovineAverageChimpanzeeOpieOP-x5nayUCnonkU2OKc"
        await ctx.typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @twitch.command(name="climb")
    async def climb(self, ctx):
        text = (
            "Hey Cloudy. I am a diamond level tank player with aspirations to climb higher. "
            + "I watch your streams every day in order to learn and get better. "
            + "Now after studying your gameplay and applying it I have tanked to bronze. Thanks and much love."
        )
        await ctx.typing()
        message = await ctx.send(text)
        await message.add_reaction(random_emoji())

    @twitch.command(name="code", aliases=["workshop"])
    async def code(self, ctx):
        text = "rein: XEEAE | other: https://workshop.codes/u/Seita%232315"
        await ctx.typing()
        message = await ctx.send(text)
        await message.add_reaction(random_emoji())

    @twitch.command(name="dva")
    async def dva(self, ctx):
        url = "https://www.twitch.tv/lhcloudy27/clip/SmokyDifferentCobblerDoggo-rY6mWkS8b2Jj5kDm"
        await ctx.typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @twitch.command(name="dva2")
    async def dva_two(self, ctx):
        url = "https://clips.twitch.tv/WanderingLuckyClipzBrainSlug-0x2XxJjniDP_SSeX"
        await ctx.typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @twitch.command(name="dva3")
    async def dva_three(self, ctx):
        url = "https://clips.twitch.tv/ThirstySavageMinkAsianGlow-drRcT2-cwpRSx2gE"
        await ctx.typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @twitch.command(name="egirl")
    async def egirl(self, ctx):
        text = "hey big cwoudy man, cawn i pwease be uw egiww mewcy?"
        await ctx.typing()
        message = await ctx.send(text)
        await message.add_reaction("👉")
        await message.add_reaction("👈")
        await message.add_reaction("😌")

    @twitch.command(name="firestrike")
    async def fire_strike(self, ctx):
        url = "https://www.twitch.tv/lhcloudy27/clip/CalmFurtiveVelociraptorTheTarFu-z0r_NEsmXN4_Xp9P"
        await ctx.typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @twitch.command(name="genji")
    async def genji(self, ctx):
        url = "https://clips.twitch.tv/InspiringRoundScorpionHeyGirl-gudJtViOZOW4z5tg"
        await ctx.typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @twitch.command(name="hanzo")
    async def hanzo(self, ctx):
        url = "https://clips.twitch.tv/ThankfulArtsyWheelFrankerZ-Mh-4_e_SyGsCU-_c"
        await ctx.typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @twitch.command(name="hype")
    async def hype(self, ctx):
        text = """What is all the hype around @LhCloudy ?
        Had him on my team today and the guy is a complete r*****,
        I didn’t have the best of games myself due to be playing 400sr above and on an offrole.
        This guy hard feeds into DS on Rein. Blinded by his own ego. How tf did he used to play in OWL"
        """
        await ctx.typing()
        message = await ctx.send(text)
        await message.add_reaction(random_emoji())

    @twitch.command(name="instagram")
    async def instagram(self, ctx):
        url = "https://www.instagram.com/lhcloudy/"
        await ctx.typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @twitch.command(name="lucio")
    async def lucio(self, ctx):
        url = "https://clips.twitch.tv/ImpossibleBombasticAardvarkBlargNaut-2lnCp98G-ix8bmnw"
        await ctx.typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @twitch.command(name="mercy")
    async def mercy(self, ctx):
        url = "https://i.gyazo.com/thumb/1200/a394f225d5c384952909e498e324c5f5-jpg.jpg"
        await ctx.typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @twitch.command(name="pokiw")
    async def pokiw(self, ctx):
        url = "https://imgur.com/a/SOZg7Lr"
        await ctx.typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @twitch.command(name="pokiw2")
    async def pokiw_two(self, ctx):
        url = "https://clips.twitch.tv/CallousSassySaladPicoMause-gexEqHi49_OZ6vQz"
        await ctx.typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @twitch.command(name="rollout")
    async def rollout(self, ctx):
        url = "https://clips.twitch.tv/WanderingCheerfulTrollOpieOP-wovrMAmwVmXPeBWz"
        await ctx.typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @twitch.command(name="sniper")
    async def sniper(self, ctx):
        url = "https://clips.twitch.tv/PunchyBoxyClipsdadBigBrother-bUVRYZljuBsYv-rK"
        await ctx.typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @twitch.command(name="soldier")
    async def soldier(self, ctx):
        url = "https://gyazo.com/2e6fa3ff597b7865c6582759aa1e6ea0"
        await ctx.typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @twitch.command(name="speed")
    async def speed(self, ctx):
        text = '"you give me speed i give sr"'
        await ctx.typing()
        message = await ctx.send(text)
        await message.add_reaction(random_emoji())

    @twitch.command(name="spotify")
    async def spotify(self, ctx):
        url = "https://open.spotify.com/playlist/3JuA2BZjl0aZsEHKry1B67?si=14278d6ea4c04330"
        await ctx.typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @twitch.command(name="playlist")
    async def playlist(self, ctx):
        url = "https://www.youtube.com/watch?v=p1SlBlB5pzU&list=RDHiu1hPdJk-Y&index=23"
        await ctx.typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @twitch.command(name="srpeak")
    async def srpeak(self, ctx):
        text = (
            "I saw Cloudy in a 4K lobby one time. "
            + "I told him how cool it was to meet him in game, "
            + "but I didn’t want to be a douche and bother him and "
            + "ask him for friend request or anything. He said, "
            + "“Oh, sr peak check?” I was taken aback, and all I could say was “Huh?” "
            + "but he kept cutting me off and going “huh? huh? huh?” "
            + "while using the “No” voiceline repeatedly."
        )
        await ctx.typing()
        message = await ctx.send(text)
        await message.add_reaction(random_emoji())

    @twitch.command(name="stairs")
    async def stair(self, ctx):
        url = "https://clips.twitch.tv/ProductiveSuspiciousReubenChocolateRain-apmCaU0TwTIFuF2Z"
        await ctx.typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @twitch.command(name="strength")
    async def strength(self, ctx):
        text = (
            "Cloudys strength is aggression, "
            + "catching people off guard with it. "
            + "But I’ve noticed it gets him in bad positions because a lack of patience."
        )
        await ctx.typing()
        message = await ctx.send(text)
        await message.add_reaction(random_emoji())

    @twitch.command(name="tips")
    async def tips(self, ctx):
        text = "W+M1"
        await ctx.typing()
        message = await ctx.send(text)
        await message.add_reaction(random_emoji())

    @twitch.command(name="twitter")
    async def twitter(self, ctx):
        url = "https://twitter.com/LhCloudy"
        await ctx.typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @twitch.command(name="tracer")
    async def tracer(self, ctx):
        url = "https://gyazo.com/444bd292aa15ca168bddb563aefc1191"
        await ctx.typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @twitch.command(name="volskaya")
    async def volskaya(self, ctx):
        url = "https://clips.twitch.tv/ColdSuccessfulFlyTheTarFu-Tg_R4sjZyjCMO5cY"
        await ctx.typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @twitch.command(name="wallbang")
    async def wallbang(self, ctx):
        url = "https://www.twitch.tv/lhcloudy27/clip/RudeAbstruseHummingbirdPunchTrees-y7H3Pk3hrdoKarhP?filter=clips&range=7d&sort=time"
        await ctx.typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @twitch.command(name="widow")
    async def widow(self, ctx):
        url = "https://gyazo.com/4939b21f5db58b259314a5cf70390341"
        await ctx.typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @twitch.command(name="youtube")
    async def youtube(self, ctx):
        url = "SMÄSH THAT LIKE AND SUBSCRIBE BUTTON -> https://www.youtube.com/channel/UC2CV-HWvIrMO4mUnYtNS-7A"
        await ctx.typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @twitch.command(name="zarya")
    async def zarya(self, ctx):
        url = "https://clips.twitch.tv/PeacefulAstuteClintTwitchRaid-iVjcGr7u5ZGr_6Sz"
        await ctx.typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @twitch.command(name="zarya2")
    async def zarya_two(self, ctx):
        url = "https://clips.twitch.tv/UninterestedWealthyDurian4Head-F-XGgZtBOwdvBAdU"
        await ctx.typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @twitch.command(name="age", aliases=["oldman"])
    async def age(self, ctx):
        td = datetime.datetime.now().date()
        bd = datetime.date(1999, 5, 21)
        age_years = int((td - bd).days / 365.25)
        await ctx.typing()
        message = await ctx.send(age_years)
        await message.add_reaction(random_emoji())

    @twitch.command(name="backlane")
    async def backlane(self, ctx):
        text = "fuck this game, their is no teamplay its about who gonna headshot backlane first, make goat great again"
        await ctx.typing()
        message = await ctx.send(text)
        await message.add_reaction(random_emoji())

    @twitch.command(name="chair")
    async def chair(self, ctx):
        text = "Herman Miller Aeron\nhttps://www.hermanmiller.com/products/seating/office-chairs/aeron-chairs/"
        await ctx.typing()
        message = await ctx.send(text)
        await message.add_reaction(random_emoji())

    @twitch.command(name="cloudycree")
    async def cloudycree(self, ctx):
        url = "https://www.twitch.tv/lep_ow/clip/DifficultAmusedBillSpicyBoy--UBV2xxbcIsLlQKW?filter=clips&range=30d&sort=time"
        await ctx.typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @twitch.command(name="from")
    async def from_(self, ctx):
        text = "kotka of south eastern finland of the continent of europe"
        await ctx.typing()
        message = await ctx.send(text)
        await message.add_reaction(random_emoji())

    @twitch.command(
        name="links",
        aliases=["urls"],
    )
    async def links(self, ctx):
        links = (
            "• Twitch <https://www.twitch.tv/lhcloudy27>"
            "\n• Youtube: <https://www.youtube.com/channel/UC2CV-HWvIrMO4mUnYtNS-7A>"
            + "\n• Discord: <https://discord.gg/jd6CZSj8jb>"
            + "\n• Twitter: <https://twitter.com/LhCloudy>"
            + "\n• Instagram: <https://www.instagram.com/lhcloudy/>"
            + "\n• Reddit: <https://www.reddit.com/r/overwatchSRpeakCHECK/>"
        )
        embed = Embed(title="LhCloudy Links", description=links, color=0x2ECC71)
        await ctx.typing()
        await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(LhCloudy(client))
