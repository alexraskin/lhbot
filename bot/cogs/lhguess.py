import random

from bson.objectid import ObjectId
from discord import Embed
from discord.ext import commands, tasks
from utils.banwords import banned_words
from utils.emojis import random_emoji
from utils.generate_pdf import PdfReport
from utils.hints import lh_hints
from utils.return_helper import helper
from utils.s3_client import S3Upload


class LhGuess(commands.Cog, name="LhGuess"):
    def __init__(self, client: commands.Bot) -> None:
        """
        The __init__ function is used to initialize the class. It's called when an instance of a class is created, and it
        creates space in memory for the new object. In this case, it creates space for self (the bot) and then initializes
        variables that will be used later on.

        :param self: Used to reference the class itself.
        :param client: Used to access the bot's attributes.
        :return: the client that we will use to interact with the Discord API.
        """
        self.client = client
        self.banned_words_list = banned_words.split("\n")
        self.hints = lh_hints.split("\n")
        self.error_color = 0xE74C3C
        self.success_color = 0x42F56C
        self.database = self.client.db_client.lhbot
        self.collection = self.database.get_collection("lhbot_collection")
        self.load_collection_list.start()

    @tasks.loop(seconds=30)
    async def load_collection_list(self) -> list:
        """
        The load_collection_list function specifically loads the collection list from the database and stores it in a variable.
        It then iterates through each guess in the collection and appends them to a list.

        :param self: Used to access the class attributes.
        :return: a list of all the guesses in the collection.
        """
        self.guess_list = []
        async for guess in self.collection.find():
            data = helper(guess)
            self.guess_list.append(
                {"guess": data["guess"], "guessedBy": data["guessedBy"]}
            )

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="lhguess")
    async def lh_guess(self, ctx, *, guess) -> Embed:
        """
        The lh_guess function is used to add a guess to the database.
        It takes in a string as an argument and adds it to the database.
        The function also returns some information about the guess that was just added.

        :param self: Used to access the bot's attributes.
        :param ctx: Used to get the context of the message.
        :param *: Used to pass in unlimited arguments.
        :param guess: Used to store the user's guess.
        :return: an embed message
        """
        if not ctx.channel.guild.id == self.client.main_guild.id:
            # Don't allow guesses messages on servers other than the main server
            return

        if not str(guess).lower().startswith("l"):
            embed = Embed(title="Guess not allowed!", color=self.error_color)
            await ctx.typing()
            embed_message = await ctx.send(embed=embed)
            await embed_message.add_reaction("❌")
            return

        if str(guess).lower() in self.banned_words_list:
            embed = Embed(title="Guess not allowed!", color=self.error_color)
            await ctx.typing()
            embed_message = await ctx.send(embed=embed)
            await embed_message.add_reaction("❌")
            return

        guessed = await self.collection.count_documents({"lhguess": str(guess).lower()})
        if guessed > 0:
            embed = Embed(
                title="This has already been guessed 🚨",
                description=f"LhGuess: {guess}",
            )
            await ctx.typing()
            embed_message = await ctx.send(embed=embed)
            await embed_message.add_reaction("👎")
        else:
            guess_dict = {
                "lhguess": str(guess).lower(),
                "guessedBy": str(ctx.message.author),
            }
            new_guess = await self.collection.insert_one(guess_dict)
            return_guess = await self.collection.find_one(
                {"_id": new_guess.inserted_id}
            )
            pretty_return = helper(return_guess)
            embed = Embed(color=self.success_color)
            embed.set_author(name="🛡️ LhGuess added to the Database 🔥")
            embed.add_field(name="LhGuess:", value=pretty_return["guess"], inline=True)
            embed.add_field(
                name="Guessed by:", value=pretty_return["guessedBy"], inline=False
            )
            embed.add_field(name="Guess ID:", value=pretty_return["id"], inline=False)
            await ctx.typing()
            embed_message = await ctx.send(embed=embed)
            await embed_message.add_reaction(random_emoji())

    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.command(name="lhcount")
    async def guess_count(self, ctx) -> Embed:
        """
        The guess_count function is used to display the current amount of guesses in the database.
        It does this by creating a list of all guesses and then counting them.

        :param self: Used to access the class methods and variables.
        :param ctx: Used to pass the context of the command.
        :return: the current amount of guesses in the database.
        """
        if not ctx.channel.guild.id == self.client.main_guild.id:
            # Don't allow guesses messages on servers other than the main server
            return
        await ctx.typing()
        embed = Embed(title="LhGuess Count", color=self.success_color)
        embed.add_field(
            name="Current guess Count:", value=f"{len(self.guess_list)} 🦍", inline=True
        )
        embed.set_footer(text=f"Requested by {ctx.message.author}")
        embed_message = await ctx.send(embed=embed)
        await embed_message.add_reaction(random_emoji())

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(name="lhreport")
    async def run_lh_report(self, ctx) -> Embed:
        """
        The run_lh_report function specifically generates a PDF report of all guesses made by the user.
        The report is generated using the PdfReport class and is stored in a file named after the author of
        the command. The function also creates an embed object that contains a link to download the PDF file.

        :param self: Used to access the class attributes and methods.
        :param ctx: Used to get the message author and channel.
        :return: the report.
        """
        if not ctx.channel.guild.id == self.client.main_guild.id:
            # Don't allow guesses messages on servers other than the main server
            return
        report = PdfReport(
            filename=f"{ctx.message.author}-report.pdf", guesses=self.guess_list
        )
        report.generate()
        share = S3Upload(report.filename)
        share.upload_file()
        embed = Embed(title="LhGuess report is ready", color=self.success_color)
        embed.add_field(name="PDF Link:", value=share.get_url())
        await ctx.typing()
        embed_message = await ctx.send(embed=embed)
        await embed_message.add_reaction(random_emoji())

    @commands.command(name="lhhint", aliases=["hint"])
    async def lh_hints(self, ctx) -> Embed:
        """
        The lh_hints function is used to send a random hint about the meaning of LH.
        It's called by typing !lh_hints in discord chat.

        :param self: Used to access the class attributes.
        :param ctx: Used to access the context of the command.
        :return: a random hint from the hints dictionary.
        """
        if not ctx.channel.guild.id == self.client.main_guild.id:
            # Don't allow guesses messages on servers other than the main server
            return
        embed = Embed(title="Random LH Hint", color=self.success_color)
        random_hint = random.choice(list(self.hints))
        embed.add_field(name="Hint:", value=random_hint, inline=True)
        embed.set_footer(text=f"Requested by {ctx.message.author}")
        await ctx.typing()
        embed_message = await ctx.send(embed=embed)
        await embed_message.add_reaction(random_emoji())

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(name="lhdelete", aliases=["deleteguess"], hidden=True)
    async def lh_delete(self, ctx, *, guess_id) -> Embed:
        """
        The lh_delete function is used to delete a specific guess from the database.
        It takes in a string of the guess id and deletes it from the database. It also
        returns an embed message with confirmation that it was deleted.

        :param self: Used to access the class attributes and methods.
        :param ctx: Used to access the context of where the command was called.
        :param *: Used to take in any number of arguments.
        :param guess_id: Used to specify the ID of the guess that is to be deleted.
        :return: the embed message that is sent to the channel.
        """
        if not ctx.channel.guild.id == self.client.main_guild.id:
            # Don't allow guesses messages on servers other than the main server
            return
        await ctx.typing()
        if not self.client.user_is_superuser(ctx.author):
            embed = Embed(
                title="You do not have permisson to run this command!",
                color=self.error_color,
            )
            embed.set_footer(text=f"Requested by {ctx.message.author}")
            embed_message = await ctx.send(embed=embed)
            await embed_message.add_reaction("🔨")
            return
        guess = await self.collection.find_one({"_id": ObjectId(guess_id)})

        if not guess:
            embed = Embed(
                title=f"Guess with ID: {guess_id} was not found!",
                color=self.error_color,
            )
            embed.set_footer(text=f"Requested by {ctx.message.author}")
            embed_message = await ctx.send(embed=embed)
            await embed_message.add_reaction("🔨")
            return

        if guess:
            embed = Embed(color=self.success_color)
            embed.add_field(
                name="Succesfully Deleted LhGuess:", value=guess_id, inline=True
            )
            embed.set_footer(text=f"Requested by {ctx.message.author}")
            await self.collection.delete_one({"_id": ObjectId(guess_id)})
            embed_message = await ctx.send(embed=embed)
            await embed_message.add_reaction("🔨")
            return


async def setup(client) -> None:
    """
    The setup function is used to register the commands that will be used in the bot.
    This function is run when you load a cog, and it's what makes your commands usable.

    :param client: Used to access the client's resources.
    :return: a dictionary of information about the bot and server.
    """
    await client.add_cog(LhGuess(client))
