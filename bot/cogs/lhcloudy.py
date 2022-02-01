import sys
import datetime

from discord import Embed
from discord.ext import commands

sys.path.append("../bot/")
from utils.emojis import random_emoji


class LhCloudy(commands.Cog, name="lhcloudy"):
    def __init__(self, client):
        """
        The __init__ function is the constructor for a class. It is called when an instance of a class is created.
        It allows the newly created object to have some attributes that are defined by this function.

        :param self: Used to refer to the object itself.
        :param client: Used to store the client's information.
        :return: the object of the class.
        """
        self.client = client

    @commands.command(name="1frame")
    async def one_frame(self, ctx):
        await one_frame_execute(ctx)

    @commands.command(name="360")
    async def three_sixty(self, ctx):
        """
        The three_sixty function specifically plays the 360 clip from the streamer, and then sends a message with that link.

        :param self: Used to access the bot's attributes.
        :param ctx: Used to access the context of the command.
        :return: a link to an animated gif of a cat spinning around.

        """
        url = "https://clips.twitch.tv/GentleObservantJalapenoLeeroyJenkins-Z53XsWoa2wamtAlB"
        await ctx.trigger_typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @commands.command(name="ball")
    async def ball(self, ctx):
        """
        The ball function is a function that sends an image of the ball. It does this by sending the url of the image to discord.

        :param self: Used to access the attributes and methods of your cog.
        :param ctx: Used to access the context of where the command was called.
        :return: the url of the image.

        """
        url = "https://gyazo.com/7f7dc8b93c4a77054104ee3d2ed9a134"
        await ctx.trigger_typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @commands.command(name="bhop")
    async def bhop(self, ctx):
        """
        The bhop function specifically sends a message with the url of the clip.

        :param self: Used to reference the bot.
        :param ctx: Used to access the context of where the command was called.
        :return: a url to the youtube video that is posted on the twitch clip website.

        """
        url = "https://www.twitch.tv/lhcloudy27/clip/ToughAttractiveHerbsBlargNaut-GvSHZicwk7Sjs13X"
        await ctx.trigger_typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @commands.command(name="lhfurry")
    async def lhfurry(self, ctx):
        """
        :param self: Used to store data that is used by the bot.
        :param ctx: Used to access the context of where the command was called.
        :return: the url of the image.
        """
        url = "https://i.gyazo.com/3ae8376713000ab829a2853d0f31e6f2.png"
        await ctx.trigger_typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @commands.command(name="bhop2")
    async def bhop_two(self, ctx):
        """
        The bhop_two function specifically sends a message with the url of the clip.

        :param self: Used to access the attributes and methods of your cog.
        :param ctx: Used to get information about the message that triggered this command.
        :return: a URL.

        """
        url = "https://clips.twitch.tv/BovineAverageChimpanzeeOpieOP-x5nayUCnonkU2OKc"
        await ctx.trigger_typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @commands.command(name="climb")
    async def climb(self, ctx):
        """
        The climb function specifically accomplishes
        sending a message to the user that is requesting for help

        :param self: Used to reference the class instance.
        :param ctx: Used to access the context of the command.
        :return: the text as a message.

        """
        text = (
            "Hey Cloudy. I am a diamond level tank player with aspirations to climb higher. "
            + "I watch your streams every day in order to learn and get better. "
            + "Now after studying your gameplay and applying it I have tanked to bronze. Thanks and much love."
        )
        await ctx.trigger_typing()
        message = await ctx.send(text)
        await message.add_reaction(random_emoji())

    @commands.command(name="code", aliases=["workshop"])
    async def code(self, ctx):
        """
        The code function specifically creates a message that displays the code for my bot.
        It also sends it to the channel that is specified in the command.

        :param self: Used to access the class attributes and methods.
        :param ctx: Used to access the context of the command.
        :return: the message that is sent by the bot.

        """
        text = "rein: XEEAE | other: https://workshop.codes/u/Seita%232315"
        await ctx.trigger_typing()
        message = await ctx.send(text)
        await message.add_reaction(random_emoji())

    @commands.command(name="dva")
    async def dva(self, ctx):
        """
        The dva function specifically sends the url of a clip from D.Va on Overwatch.

        :param self: Used to reference the bot.
        :param ctx: Used to access the context of where the command was called.
        :return: the URL of the clip and sends it in a message to the channel.
        """
        url = "https://www.twitch.tv/lhcloudy27/clip/SmokyDifferentCobblerDoggo-rY6mWkS8b2Jj5kDm"
        await ctx.trigger_typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @commands.command(name="dva2")
    async def dva_two(self, ctx):
        """
        The dva_two function specifically sends a message with the url of the clip.

        :param self: Used to access the bot's attributes.
        :param ctx: Used to send messages to the channel.
        :return: a url
        """
        url = "https://clips.twitch.tv/WanderingLuckyClipzBrainSlug-0x2XxJjniDP_SSeX"
        await ctx.trigger_typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @commands.command(name="dva3")
    async def dva_three(self, ctx):
        """
        The dva_three function specifically sends a message containing the url of the clip.

        :param self: Used to access the bot's attributes.
        :param ctx: Used to access the context of the command.
        :return: a url.
        """
        url = "https://clips.twitch.tv/ThirstySavageMinkAsianGlow-drRcT2-cwpRSx2gE"
        await ctx.trigger_typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @commands.command(name="egirl")
    async def egirl(self, ctx):
        """
        The egirl function specifically accomplishes the following:
            - It sends a message to the channel that it was called in.
            - It adds two reactions to that message, one of which is 👉 and another of which is 👈.

        :param self: Used to access the bot's attributes.
        :param ctx: Used to get the context of where the command was called.
        :return: a message.
        """
        text = "hey big cwoudy man, cawn i pwease be uw egiww mewcy?"
        await ctx.trigger_typing()
        message = await ctx.send(text)
        await message.add_reaction("👉")
        await message.add_reaction("👈")
        await message.add_reaction("😌")

    @commands.command(name="firestrike")
    async def fire_strike(self, ctx):
        """
        The fire_strike function specifically sends a message with the url of the clip.

        :param self: Used to reference the bot.
        :param ctx: Used to access the context of the command.
        :return: a url
        """
        url = "https://www.twitch.tv/lhcloudy27/clip/CalmFurtiveVelociraptorTheTarFu-z0r_NEsmXN4_Xp9P"
        await ctx.trigger_typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @commands.command(name="genji")
    async def genji(self, ctx):
        """
        The genji function specifically sends a message with the url of the clip.

        :param self: Used to reference the bot itself.
        :param ctx: Used to access the context of a command.
        :return: a url
        """
        url = "https://clips.twitch.tv/InspiringRoundScorpionHeyGirl-gudJtViOZOW4z5tg"
        await ctx.trigger_typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @commands.command(name="hanzo")
    async def hanzo(self, ctx):
        """
        The hanzo function specifically sends a message with the url of the clip.

        :param self: Used to access the bot's attributes.
        :param ctx: Used to access the context of the command.
        :return: a url
        """
        url = "https://clips.twitch.tv/ThankfulArtsyWheelFrankerZ-Mh-4_e_SyGsCU-_c"
        await ctx.trigger_typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @commands.command(name="hype")
    async def hype(self, ctx):
        """
        The hype function is used to send a message

        :param self: Used to reference the bot itself.
        :param ctx: Used to access the context of where the command was called.
        :return: text
        """
        text = """What is all the hype around @LhCloudy ?
        Had him on my team today and the guy is a complete r*****,
        I didn’t have the best of games myself due to be playing 400sr above and on an offrole.
        This guy hard feeds into DS on Rein. Blinded by his own ego. How tf did he used to play in OWL"
        """
        await ctx.trigger_typing()
        message = await ctx.send(text)
        await message.add_reaction(random_emoji())

    @commands.command(name="instagram")
    async def instagram(self, ctx):
        """
        The instagram function specifically posts the link to my Instagram page.

        :param self: Used to access the attributes and methods in this cog.
        :param ctx: Used to access the context of where the command was called.
        :return: the url of the LHC's Instagram page.
        """
        url = "https://www.instagram.com/lhcloudy/"
        await ctx.trigger_typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @commands.command(name="lucio")
    async def lucio(self, ctx):
        """
        The lucio function specifically plays the lucio clip from a twitch stream.

        :param self: Used to reference the bot.
        :param ctx: Used to access the context of where the command was called.
        :return: the url link for the clip.
        """
        url = "https://clips.twitch.tv/ImpossibleBombasticAardvarkBlargNaut-2lnCp98G-ix8bmnw"
        await ctx.trigger_typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @commands.command(name="mercy")
    async def mercy(self, ctx):
        """
        :param self: Used to access the attributes and methods of your cog, as well as any other variables that.
        :param ctx: Used to access the context of where the command was called.
        :return: the url of the image.
        """
        url = "https://i.gyazo.com/thumb/1200/a394f225d5c384952909e498e324c5f5-jpg.jpg"
        await ctx.trigger_typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @commands.command(name="pokiw")
    async def pokiw(self, ctx):
        """
        The pokiw function specifically sends a message with the link to the pokiw image on imgur.

        :param self: Used to access the attributes and methods of your cog, such as self.
        :param ctx: Used to access the context of where the command was called.
        :return: a message with the url.
        """
        url = "https://imgur.com/a/SOZg7Lr"
        await ctx.trigger_typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @commands.command(name="pokiw2")
    async def pokiw_two(self, ctx):
        """
        The pokiw_two function specifically sends a message with the url of the clip.

        :param self: Used to reference the bot's instance.
        :param ctx: Used to access the context of the message.
        :return: the url of the video.
        """
        url = "https://clips.twitch.tv/CallousSassySaladPicoMause-gexEqHi49_OZ6vQz"
        await ctx.trigger_typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @commands.command(name="rollout")
    async def rollout(self, ctx):
        """
        The rollout function specifically sends a message with the url of the clip.

        :param self: Used to access the class attributes.
        :param ctx: Used to access the context of where the command was called.
        :return: a message.
        """
        url = "https://clips.twitch.tv/WanderingCheerfulTrollOpieOP-wovrMAmwVmXPeBWz"
        await ctx.trigger_typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @commands.command(name="sniper")
    async def sniper(self, ctx):
        """
        The sniper function is a function that sends the sniper clip from the game Overwatch.
        It does this by sending a message with an embedded video of the clip.

        :param self: Used to access the bot's attributes.
        :param ctx: Used to access the context of a command.
        :return: a message with the clip url.
        """
        url = "https://clips.twitch.tv/PunchyBoxyClipsdadBigBrother-bUVRYZljuBsYv-rK"
        await ctx.trigger_typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @commands.command(name="soldier")
    async def soldier(self, ctx):
        """
        The soldier function specifically sends a message with the url of an image of a soldier.

        :param self: Used to access the attributes and methods of the class in which it is used.
        :param ctx: Used to access the context of where the command was called.
        :return: a message with a url.
        """
        url = "https://gyazo.com/2e6fa3ff597b7865c6582759aa1e6ea0"
        await ctx.trigger_typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @commands.command(name="speed")
    async def speed(self, ctx):
        """
        The speed function is a function that will send the user a message with text.

        :param self: Used to access the attributes and methods of your cog.
        :param ctx: Used to send messages to the channel where the command was called.
        :return: the string 'you give me speed i give sr'.
        """
        text = '"you give me speed i give sr"'
        await ctx.trigger_typing()
        message = await ctx.send(text)
        await message.add_reaction(random_emoji())

    @commands.command(name="spotify")
    async def spotify(self, ctx):
        """
        The spotify function specifically links to the spotify playlist that I have created for this server.
        It is a list of songs that are currently trending on the internet, and it is updated every week.

        :param self: Used to reference the bot.
        :param ctx: Used to get the context of where the command was called.
        :return: a link to the playlist.
        """
        url = "https://open.spotify.com/playlist/3JuA2BZjl0aZsEHKry1B67?si=14278d6ea4c04330"
        await ctx.trigger_typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @commands.command(name="playlist")
    async def playlist(self, ctx):
        """
        The playlist function specifically sends a message with the link to the playlist.

        :param self: Used to reference the bot.
        :param ctx: Used to access the context of where the command was called.
        :return: the url of the playlist.
        """
        url = "https://www.youtube.com/watch?v=p1SlBlB5pzU&list=RDHiu1hPdJk-Y&index=23"
        await ctx.trigger_typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @commands.command(name="srpeak")
    async def srpeak(self, ctx):
        """
        The srpeak function specifically sends a message with text

        :param self: Used to reference the bot's instance.
        :param ctx: Used to get the context of where the command was called.
        :return: a message that Cloudy has sent to the server.

        """
        text = (
            "I saw Cloudy in a 4K lobby one time. "
            + "I told him how cool it was to meet him in game, "
            + "but I didn’t want to be a douche and bother him and "
            + "ask him for friend request or anything. He said, "
            + "“Oh, sr peak check?” I was taken aback, and all I could say was “Huh?” "
            + "but he kept cutting me off and going “huh? huh? huh?” "
            + "while using the “No” voiceline repeatedly."
        )
        await ctx.trigger_typing()
        message = await ctx.send(text)
        await message.add_reaction(random_emoji())

    @commands.command(name="stairs")
    async def stair(self, ctx):
        """
        :param self: Used to access the bot's attributes.
        :param ctx: Used to get information about the message that invoked this command.
        :return: a url
        """
        url = "https://clips.twitch.tv/ProductiveSuspiciousReubenChocolateRain-apmCaU0TwTIFuF2Z"
        await ctx.trigger_typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @commands.command(name="strength")
    async def strength(self, ctx):
        """
        :param self: Used to reference the class itself.
        :param ctx: Used to get information about the message that invoked the command.
        :return: a string with the description of Cloudy's strength.
        """
        text = (
            "Cloudys strength is aggression, "
            + "catching people off guard with it. "
            + "But I’ve noticed it gets him in bad positions because a lack of patience."
        )
        await ctx.trigger_typing()
        message = await ctx.send(text)
        await message.add_reaction(random_emoji())

    @commands.command(name="tips")
    async def tips(self, ctx):
        """
        :param self: Used to access the class attributes.
        :param ctx: Used to access the context of where the command was called.
        :return: a message in the channel.
        """
        text = "W+M1"
        await ctx.trigger_typing()
        message = await ctx.send(text)
        await message.add_reaction(random_emoji())

    @commands.command(name="twitter")
    async def twitter(self, ctx):
        """
        :param self: Used to access the attributes and methods in the class.
        :param ctx: Used to access the context of where the command was called.
        :return: a message with a link to the twitter page for LhCloudy.
        """
        url = "https://twitter.com/LhCloudy"
        await ctx.trigger_typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @commands.command(name="tracer")
    async def tracer(self, ctx):
        """
        :param self: Used to access the bot's attributes.
        :param ctx: Used to access the context of where the command was called.
        :return: a message object, containing the url.
        """
        url = "https://gyazo.com/444bd292aa15ca168bddb563aefc1191"
        await ctx.trigger_typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @commands.command(name="volskaya")
    async def volskaya(self, ctx):
        """
        The volskaya function specifically sends a message with the url of the clip.

        :param self: Used to access the attributes and methods of your cog, as well as any other cogs that are loaded.
        :param ctx: Used to get the context of where the command was called.
        :return: a url from twitch clips.
        """
        url = "https://clips.twitch.tv/ColdSuccessfulFlyTheTarFu-Tg_R4sjZyjCMO5cY"
        await ctx.trigger_typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @commands.command(name="wallbang")
    async def wallbang(self, ctx):
        """
        The wallbang function specifically sends a message with the link to the wallbang clip of lhcloudy27 on twitch.
        The function also triggers typing in discord so that it looks like something is happening.

        :param self: Used to access the attributes and methods of your cog, as well as any other cogs that are loaded.
        :param ctx: Used to get the channel and user that sent the command.
        :return: the twitch clip link.
        """
        url = "hhttps://www.twitch.tv/lhcloudy27/clip/RudeAbstruseHummingbirdPunchTrees-y7H3Pk3hrdoKarhP?filter=clips&range=7d&sort=time"
        await ctx.trigger_typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @commands.command(name="widow")
    async def widow(self, ctx):
        """
        :param self: Used to access the attributes and methods of your cog.
        :param ctx: Used to access the context of where the command was called.
        :return: a message.
        """
        url = "https://gyazo.com/4939b21f5db58b259314a5cf70390341"
        await ctx.trigger_typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @commands.command(name="youtube")
    async def youtube(self, ctx):
        """
        :param self: Used to access the bot's attributes.
        :param ctx: Used to access the context of where the command was called.
        :return: the url of the youtube channel.
        """
        url = "SMÄSH THAT LIKE AND SUBSCRIBE BUTTON -> https://www.youtube.com/channel/UC2CV-HWvIrMO4mUnYtNS-7A"
        await ctx.trigger_typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @commands.command(name="zarya")
    async def zarya(self, ctx):
        """
        The zarya function specifically plays a clip of Zarya from Overwatch.
        It also sends the link to that clip.

        :param self: Used to reference the bot.
        :param ctx: Used to get the context of the message.
        :return: a message with the URL of a clip.
        """
        url = "https://clips.twitch.tv/PeacefulAstuteClintTwitchRaid-iVjcGr7u5ZGr_6Sz"
        await ctx.trigger_typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @commands.command(name="zarya2")
    async def zarya_two(self, ctx):
        """
        The zarya_two function specifically sends a message with the url of the clip.

        :param self: Used to access the attributes and methods of your cog, as well as any ctx objects that are passed in.
        :param ctx: Used to send messages to the channel where the command was called.
        :return: a url link in a string format.
        """
        url = "https://clips.twitch.tv/UninterestedWealthyDurian4Head-F-XGgZtBOwdvBAdU"
        await ctx.trigger_typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @commands.command(name="age", aliases=["oldman"])
    async def age(self, ctx):
        """
        The age function specifically calculates the age of the user and sends it to discord.

        :param self: Used to reference the bot's instance, which is passed in as an argument when the command is called.
        :param ctx: Used to access the context of the message.
        :return: the age of the bot in years.

        """
        td = datetime.datetime.now().date()
        bd = datetime.date(1999, 5, 21)
        age_years = int((td - bd).days / 365.25)
        await ctx.trigger_typing()
        message = await ctx.send(age_years)
        await message.add_reaction(random_emoji())

    @commands.command(name="backlane")
    async def backlane(self, ctx):
        """
        :param self: Used to access the attributes and methods of your cog, as well as any other cogs which are loaded.
        :param ctx: Used to access the context of where the message was sent.
        :return: the text in the variable text.
        """
        text = "fuck this game, their is no teamplay its about who gonna headshot backlane first, make goat great again"
        await ctx.trigger_typing()
        message = await ctx.send(text)
        await message.add_reaction(random_emoji())

    @commands.command(name="chair")
    async def chair(self, ctx):
        """
        The chair function specifically tells the user what the chair is and where to buy it.

        :param self: Used to access the class attributes.
        :param ctx: Used to access the context of where the command was called.
        :return: the link to the Aeron chair.
        """
        text = "Herman Miller Aeron\nhttps://www.hermanmiller.com/products/seating/office-chairs/aeron-chairs/"
        await ctx.trigger_typing()
        message = await ctx.send(text)
        await message.add_reaction(random_emoji())

    @commands.command(name="cloudycree")
    async def cloudycree(self, ctx):
        """
        The cloudycree function specifically posts the link to the clip of cloudycree's stream.
        It also sends a message that says it is posting the link.

        :param self: Used to access the class functions.
        :param ctx: Used to access the context of the command.
        :return: a URL for the clip of the streamer 'LepOw' playing a game called 'Creeper World 3'.
        """
        url = "https://www.twitch.tv/lep_ow/clip/DifficultAmusedBillSpicyBoy--UBV2xxbcIsLlQKW?filter=clips&range=30d&sort=time"
        await ctx.trigger_typing()
        message = await ctx.send(url)
        await message.add_reaction(random_emoji())

    @commands.command(name="from")
    async def from_(self, ctx):
        """
        :param self: Used to access the attributes and methods of the class in which it is used.
        :param ctx: Used to access the context of the command.
        :return: a discord.
        """
        text = "kotka of south eastern finland of the continent of europe"
        await ctx.trigger_typing()
        message = await ctx.send(text)
        await message.add_reaction(random_emoji())

    @commands.command(
        name="links",
        aliases=["urls"],
    )
    async def links(self, ctx):
        """
        The links function specifically outputs a list of links to social media,
           and other websites that are relevant to the LhCloudy.

        :param self: Used to access the attributes and methods of your cog,.
        :param ctx: Used to get the context of the command.
        :return: a string containing the links to the social media accounts of LhCloudy.
        """
        links = (
            "• Twitch <https://www.twitch.tv/lhcloudy27>"
            "\n• Youtube: <https://www.youtube.com/channel/UC2CV-HWvIrMO4mUnYtNS-7A>"
            + "\n• Discord: <https://discord.gg/jd6CZSj8jb>"
            + "\n• Twitter: <https://twitter.com/LhCloudy>"
            + "\n• Instagram: <https://www.instagram.com/lhcloudy/>"
            + "\n• Reddit: <https://www.reddit.com/r/overwatchSRpeakCHECK/>"
        )
        embed = Embed(title="LhCloudy Links", description=links, color=0x2ECC71)
        await ctx.trigger_typing()
        await ctx.send(embed=embed)


def setup(client):
    """
    The setup function is used to register the commands that will be used in the bot.
    This function is run when you load a cog, and it allows you to use commands in your cogs.

    :param client: Used to pass in the discord.
    :return: a dictionary of the following form:.

    """
    client.add_cog(LhCloudy(client))


async def one_frame_execute(ctx):
    url = "https://www.twitch.tv/lhcloudy27/clip/AbstruseKindRuffFutureMan-dLWae-FGvNag2jtK"
    await ctx.trigger_typing()
    message = await ctx.send(url)
    # await message.add_reaction(random_emoji())
