import random

import discord
from discord.ext import commands

from database.db import db_client
from utils.banwords import banned_words
from utils.generate_pdf import PdfReport
from utils.return_helper import _helper
from utils.uploader import FileSharer

database = db_client.lhbot

collection = database.get_collection("lhbot_collection")


class LhGuess(commands.Cog, name="lhguess"):
    def __init__(self, client):
        """
        The __init__ function is a special function that Python runs automatically whenever we create a new instance based on the Dog class. The self parameter refers to the newly created object, and we can access attributes and methods of that object as its attributes.
        
        :param self: Used to refer to the class instance itself.
        :param client: Used to access the client's methods and properties.
        :return: the bot object.
        :doc-author: Trelent
        """
        self.bot = client
        self.banned_words_list = banned_words.split("\n")
        self.hints = [
            "It is in English",
            "Made by 10 year old finnish lad",
            "Clever",
            "Masaa can be bribed",
            "It's not long hammer",
        ]

    @commands.command(name="lhguess")
    async def lh_guess(self, ctx, *, guess):
        """
        The lh_guess function is used to add a guess to the database.
        It takes in a string as an argument and adds it to the database.
        The function also returns some information about the guess that was just added.
        
        :param self: Used to access the bot's attributes.
        :param ctx: Used to get the context of the message.
        :param *: Used to pass in unlimited arguments.
        :param guess: Used to store the user's guess.
        :return: a dictionary containing the guess, guessedBy and id of the guess.
        :doc-author: Trelent
        """
        """
        !lhguess <your guess>
        """

        if str(guess).lower() in self.banned_words_list:
            embed = discord.Embed(title="Guess not allowed", color=0xE74C3C)
            embed_message = await ctx.send(embed=embed)
            await embed_message.add_reaction("❌")

        else:

            guesses = []
            async for _guess in collection.find():
                guesses.append(_helper(_guess)["guess"])
            if str(guess).lower() in guesses:
                embed = discord.Embed(
                    title="This has already been guessed 🚨",
                    description=f"LhGuess: {guess}",
                )
                embed_message = await ctx.send(embed=embed)
                await embed_message.add_reaction("👎")
            else:
                guess_dict = {
                    "lhguess": str(guess).lower(),
                    "guessedBy": str(ctx.message.author),
                }
                new_guess = await collection.insert_one(guess_dict)
                return_guess = await collection.find_one({"_id": new_guess.inserted_id})
                pretty_return = _helper(return_guess)
                embed = discord.Embed(color=0x42F56C)
                embed.set_author(name="🛡️ LhGuess added to the Database 🔥")
                embed.add_field(
                    name="LhGuess:", value=pretty_return["guess"], inline=True
                )
                embed.add_field(
                    name="Guessed by:",
                    value=pretty_return["guessedBy"],
                    inline=False)
                embed.add_field(
                    name="Guess ID:", value=pretty_return["id"], inline=False
                )
                embed_message = await ctx.send(embed=embed)
                await embed_message.add_reaction("👍")

    @commands.command(name="lhcount")
    async def guess_count(self, ctx):
        """
        The guess_count function is used to display the current amount of guesses in the database.
        It does this by creating a list of all guesses and then counting them.
        
        :param self: Used to access the class methods and variables.
        :param ctx: Used to pass the context of the command.
        :return: the current amount of guesses in the database.
        :doc-author: Trelent
        """
        """
        current amount of guesses in the database
        """
        guesses = []
        async for _guess in collection.find():
            guesses.append(_helper(_guess)["guess"])
        embed = discord.Embed(title="LhGuess Count", color=0x42F56C)
        embed.add_field(
            name="Current guess Count:",
            value=f"{len(guesses)} 🦍",
            inline=True)
        embed.set_footer(text=f"Requested by {ctx.message.author}")
        embed_message = await ctx.send(embed=embed)
        await embed_message.add_reaction("💚")

    @commands.command(name="lhreport")
    async def run_lh_report(self, ctx):
        """
        The run_lh_report function specifically generates a PDF report of all guesses made by the user.
        The report is generated using the PdfReport class and is stored in a file named after the author of 
        the command. The function also creates an embed object that contains a link to download the PDF file.
        
        :param self: Used to access the class attributes and methods.
        :param ctx: Used to get the message author and channel.
        :return: the report.
        :doc-author: Trelent
        """
        """
        generate LhGuess PDF report
        """
        guess_list = []
        async for _guess in collection.find():
            guess_list.append(_helper(_guess)["guess"])
        report = PdfReport(
            filename=f"{ctx.message.author}-report.pdf", guesses=guess_list
        )
        report.generate()
        share = FileSharer(f"{report.filename}")
        embed = discord.Embed(title="LhGuess report is ready", color=0x42F56C)
        embed.add_field(name="PDF Link:", value=share.share())
        embed_message = await ctx.send(embed=embed)
        await embed_message.add_reaction("✔️")

    @commands.command(name="lhhint")
    async def lh_hints(self, ctx):
        """
        The lh_hints function is used to send a random hint about the meaning of LH.
        It's called by typing !lh_hints in discord chat.
        
        :param self: Used to access the class attributes.
        :param ctx: Used to access the context of the command.
        :return: a random hint from the hints dictionary.
        :doc-author: Trelent
        """
        """
        random hint about the meaning of LH
        """
        embed = discord.Embed(description="LhHints", color=0x42F56C)
        random_hint = random.choice(list(self.hints))
        embed.set_author(name="Random LH Hint")
        embed.add_field(name="Hint:", value=random_hint, inline=False)
        embed.set_footer(text=f"Requested by {ctx.message.author}")
        embed_message = await ctx.send(embed=embed)
        embed_message.add_reaction("✨")


def setup(client):
    """
    The setup function is used to register the commands that will be used in the bot.
    This function is run when you load a cog, and it's what makes your commands usable.
    
    :param client: Used to access the client's resources.
    :return: a dictionary of information about the bot and server.
    :doc-author: Trelent
    """
    client.add_cog(LhGuess(client))
