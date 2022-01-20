import json
import os
import sys
import random

from discord.ext import commands

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json", encoding="utf-8") as file:
        config = json.load(file)


class LhCloudy(commands.Cog, name="lhcloudy"):
    """
    commands from twitch chat
    """

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def random_emoji():
        emoji_list = [
            "😁",
            "🥶",
            "👌",
            "👀",
            "🤖",
            "👽",
            "💀",
            "🤯",
            "🤠",
            "📼",
            "📈",
            "🧡",
            "✨",
            "🍑",
            "🔨",
            "🛡️",
            "🇫🇮",
            "🐸",
            "🐈"
        ]
        return random.choice(list(emoji_list))

    @commands.command(name="1frame")
    async def one_frame(self, ctx):
        url = "https://www.twitch.tv/lhcloudy27/clip/AbstruseKindRuffFutureMan-dLWae-FGvNag2jtK"
        message = await ctx.send(url)
        await message.add_reaction(LhCloudy.random_emoji())

    @commands.command(name="360")
    async def three_sixty(self, ctx):
        url = "https://clips.twitch.tv/GentleObservantJalapenoLeeroyJenkins-Z53XsWoa2wamtAlB"
        message = await ctx.send(url)
        await message.add_reaction(LhCloudy.random_emoji())

    @commands.command(name="ball")
    async def ball(self, ctx):
        url = "https://gyazo.com/7f7dc8b93c4a77054104ee3d2ed9a134"
        message = await ctx.send(url)
        await message.add_reaction(LhCloudy.random_emoji())

    @commands.command(name="bhop")
    async def bhop(self, ctx):
        url = "https://www.twitch.tv/lhcloudy27/clip/ToughAttractiveHerbsBlargNaut-GvSHZicwk7Sjs13X"
        message = await ctx.send(url)
        await message.add_reaction(LhCloudy.random_emoji())

    @commands.command(name="bhop2")
    async def bhop_two(self, ctx):
        url = "https://clips.twitch.tv/BovineAverageChimpanzeeOpieOP-x5nayUCnonkU2OKc"
        message = await ctx.send(url)
        await message.add_reaction(LhCloudy.random_emoji())

    @commands.command(name="climb")
    async def climb(self, ctx):
        text = """Hey Cloudy. I am a diamond level tank player with aspirations to climb higher. I watch your streams every day in order to learn and get better. Now after studying your gameplay and applying it I have tanked to bronze. Thanks and much love."""
        message = await ctx.send(text)
        await message.add_reaction(LhCloudy.random_emoji())

    @commands.command(name="code")
    async def code(self, ctx):
        text = "rein: XEEAE | other: https://workshop.codes/u/Seita%232315"
        message = await ctx.send(text)
        await message.add_reaction(LhCloudy.random_emoji())

    @commands.command(name="dva")
    async def dva(self, ctx):
        url = "https://www.twitch.tv/lhcloudy27/clip/SmokyDifferentCobblerDoggo-rY6mWkS8b2Jj5kDm"
        message = await ctx.send(url)
        await message.add_reaction(LhCloudy.random_emoji())
    
    @commands.command(name="dva2")
    async def dva(self, ctx):
        url = "https://clips.twitch.tv/WanderingLuckyClipzBrainSlug-0x2XxJjniDP_SSeX"
        message = await ctx.send(url)
        await message.add_reaction(LhCloudy.random_emoji())
    
    @commands.command(name="dva2")
    async def dva(self, ctx):
        url = "https://clips.twitch.tv/ThirstySavageMinkAsianGlow-drRcT2-cwpRSx2gE"
        message = await ctx.send(url)
        await message.add_reaction(LhCloudy.random_emoji())

    @commands.command(name="egirl")
    async def dva(self, ctx):
        text = "hey big cwoudy man, cawn i pwease be uw egiww mewcy?"
        message = await ctx.send(text)
        await message.add_reaction("👉")
        await message.add_reaction("👈")
        await message.add_reaction("😌")
    
    @commands.command(name="firestrike")
    async def fire_strike(self, ctx):
        url = "https://www.twitch.tv/lhcloudy27/clip/CalmFurtiveVelociraptorTheTarFu-z0r_NEsmXN4_Xp9P"
        message = await ctx.send(url)
        await message.add_reaction(LhCloudy.random_emoji())
    
    @commands.command(name="genji")
    async def genji(self, ctx):
        url = "https://clips.twitch.tv/InspiringRoundScorpionHeyGirl-gudJtViOZOW4z5tg"
        message = await ctx.send(url)
        await message.add_reaction(LhCloudy.random_emoji())

    @commands.command(name="hanzo")
    async def hanzo(self, ctx):
        url = "https://clips.twitch.tv/ThankfulArtsyWheelFrankerZ-Mh-4_e_SyGsCU-_c"
        message = await ctx.send(url)
        await message.add_reaction(LhCloudy.random_emoji())

    @commands.command(name="hype")
    async def hype(self, ctx):
        text = "What is all the hype around @LhCloudy ? Had him on my team today and the guy is a complete r*****, I didn’t have the best of games myself due to be playing 400sr above and on an offrole. This guy hard feeds into DS on Rein. Blinded by his own ego. How tf did he used to play in OWL"
        message = await ctx.send(text)
        await message.add_reaction(LhCloudy.random_emoji())
    
    @commands.command(name="instagram")
    async def instagram(self, ctx):
        url = "https://www.instagram.com/lhcloudy/"
        message = await ctx.send(url)
        await message.add_reaction(LhCloudy.random_emoji())
    
    @commands.command(name="lucio")
    async def lucio(self, ctx):
        url = "https://clips.twitch.tv/ImpossibleBombasticAardvarkBlargNaut-2lnCp98G-ix8bmnw"
        message = await ctx.send(url)
        await message.add_reaction(LhCloudy.random_emoji())
    
    @commands.command(name="mercy")
    async def mercy(self, ctx):
        url = "https://i.gyazo.com/thumb/1200/a394f225d5c384952909e498e324c5f5-jpg.jpg"
        message = await ctx.send(url)
        await message.add_reaction(LhCloudy.random_emoji())

    @commands.command(name="pokiw")
    async def pokiw(self, ctx):
        url = "https://imgur.com/a/SOZg7Lr"
        message = await ctx.send(url)
        await message.add_reaction(LhCloudy.random_emoji())

    @commands.command(name="pokiw2")
    async def pokiw_two(self, ctx):
        url = "https://clips.twitch.tv/CallousSassySaladPicoMause-gexEqHi49_OZ6vQz"
        message = await ctx.send(url)
        await message.add_reaction(LhCloudy.random_emoji())

    @commands.command(name="rollout")
    async def rollout(self, ctx):
        url = "https://clips.twitch.tv/WanderingCheerfulTrollOpieOP-wovrMAmwVmXPeBWz"
        message = await ctx.send(url)
        await message.add_reaction(LhCloudy.random_emoji())
    
    @commands.command(name="sniper")
    async def sniper(self, ctx):
        url = "https://clips.twitch.tv/PunchyBoxyClipsdadBigBrother-bUVRYZljuBsYv-rK"
        message = await ctx.send(url)
        await message.add_reaction(LhCloudy.random_emoji())
    
    @commands.command(name="soldier")
    async def soldier(self, ctx):
        url = "https://gyazo.com/2e6fa3ff597b7865c6582759aa1e6ea0"
        message = await ctx.send(url)
        await message.add_reaction(LhCloudy.random_emoji())
    
    @commands.command(name="speed")
    async def speed(self, ctx):
        text = '"you give me speed i give sr"'
        message = await ctx.send(text)
        await message.add_reaction(LhCloudy.random_emoji())
    
    @commands.command(name="spotify")
    async def spotify(self, ctx):
        url = "https://open.spotify.com/playlist/3JuA2BZjl0aZsEHKry1B67?si=14278d6ea4c04330"
        message = await ctx.send(url)
        await message.add_reaction(LhCloudy.random_emoji())
    
    @commands.command(name="playlist")
    async def playlist(self, ctx):
        url = "https://www.youtube.com/watch?v=p1SlBlB5pzU&list=RDHiu1hPdJk-Y&index=23"
        message = await ctx.send(url)
        await message.add_reaction(LhCloudy.random_emoji())
    
    @commands.command(name="srpeak")
    async def srpeak(self, ctx):
        text = "I saw Cloudy in a 4K lobby one time. I told him how cool it was to meet him in game, but I didn’t want to be a douche and bother him and ask him for friend request or anything. He said, “Oh, sr peak check?” I was taken aback, and all I could say was “Huh?” but he kept cutting me off and going “huh? huh? huh?” while using the “No” voiceline repeatedly."
        message = await ctx.send(text)
        await message.add_reaction(LhCloudy.random_emoji())
    
    @commands.command(name="stairs")
    async def stair(self, ctx):
        url = "https://clips.twitch.tv/ProductiveSuspiciousReubenChocolateRain-apmCaU0TwTIFuF2Z"
        message = await ctx.send(url)
        await message.add_reaction(LhCloudy.random_emoji())
    
    @commands.command(name="strength")
    async def strength(self, ctx):
        text = "Cloudys strength is aggression, catching people off guard with it. But I’ve noticed it gets him in bad positions because a lack of patience."
        message = await ctx.send(text)
        await message.add_reaction(LhCloudy.random_emoji())
    
    @commands.command(name="tips")
    async def tips(self, ctx):
        text = "W+M1"
        message = await ctx.send(text)
        await message.add_reaction(LhCloudy.random_emoji())
    
    @commands.command(name="twitter")
    async def twitter(self, ctx):
        url = "https://twitter.com/LhCloudy"
        message = await ctx.send(url)
        await message.add_reaction(LhCloudy.random_emoji())
    
    @commands.command(name="tracer")
    async def tracer(self, ctx):
        url = "https://gyazo.com/444bd292aa15ca168bddb563aefc1191"
        message = await ctx.send(url)
        await message.add_reaction(LhCloudy.random_emoji())
    
    @commands.command(name="volskaya")
    async def volskaya(self, ctx):
        url = "https://clips.twitch.tv/ColdSuccessfulFlyTheTarFu-Tg_R4sjZyjCMO5cY"
        message = await ctx.send(url)
        await message.add_reaction(LhCloudy.random_emoji())
    
    @commands.command(name="wallbang")
    async def wallbang(self, ctx):
        url = "hhttps://www.twitch.tv/lhcloudy27/clip/RudeAbstruseHummingbirdPunchTrees-y7H3Pk3hrdoKarhP?filter=clips&range=7d&sort=time"
        message = await ctx.send(url)
        await message.add_reaction(LhCloudy.random_emoji())
    
    @commands.command(name="widow")
    async def widow(self, ctx):
        url = "https://gyazo.com/4939b21f5db58b259314a5cf70390341"
        message = await ctx.send(url)
        await message.add_reaction(LhCloudy.random_emoji())
    
    @commands.command(name="youtube")
    async def youtube(self, ctx):
        url = "SMÄSH THAT LIKE AND SUBSCRIBE BUTTON -> https://www.youtube.com/channel/UC2CV-HWvIrMO4mUnYtNS-7A"
        message = await ctx.send(url)
        await message.add_reaction(LhCloudy.random_emoji())
    
    @commands.command(name="zarya")
    async def zarya(self, ctx):
        url = "https://clips.twitch.tv/PeacefulAstuteClintTwitchRaid-iVjcGr7u5ZGr_6Sz"
        message = await ctx.send(url)
        await message.add_reaction(LhCloudy.random_emoji())
    
    @commands.command(name="zarya2")
    async def zarya_two(self, ctx):
        url = "https://clips.twitch.tv/UninterestedWealthyDurian4Head-F-XGgZtBOwdvBAdU"
        message = await ctx.send(url)
        await message.add_reaction(LhCloudy.random_emoji())
    
    

def setup(bot):
    bot.add_cog(LhCloudy(bot))
