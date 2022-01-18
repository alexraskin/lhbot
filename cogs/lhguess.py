import json
import os
import sys

import aiofiles
import discord
from discord.ext import commands

from database.db import client
from database.utils.return_helper import _helper
from utils.generate_pdf import PdfReport
from utils.uploader import FileSharer

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

database = client.lhbot

collection = database.get_collection("lhbot_collection")


class LhGuess(commands.Cog, name="lhguess"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="lhguess")
    async def lh_guess(self, ctx, *, guess):
        """
        !lhguess <your guess>
        """
        banned_list = []
        async with aiofiles.open("./cogs/banwords.txt") as banned_words:
            async for line in banned_words:
                banned_list.append(line.strip("\n"))
        if str(guess).lower() in banned_list:
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
                    name="Guessed by:", value=pretty_return["guessedBy"], inline=False
                )
                embed.add_field(
                    name="Guess ID:", value=pretty_return["id"], inline=False
                )
                embed_message = await ctx.send(embed=embed)
                await embed_message.add_reaction("👍")

    @commands.command(name="lhcount")
    async def guess_count(self, ctx):
        """
        current amount of guesses in the database
        """
        guesses = []
        async for _guess in collection.find():
            guesses.append(_helper(_guess)["guess"])
        embed = discord.Embed(color=0x42F56C)
        embed.add_field(name="LhGuess Count", value=f"{len(guesses)} 🦍", inline=True)
        embed.set_footer(text=f"Requested by {ctx.message.author}")
        embed_message = await ctx.send(embed=embed)
        await embed_message.add_reaction("💚")

    @commands.command(name="lhshow")
    async def show_all_guess(self, ctx):
        """
        show all guesses in the database
        """
        guess_list = []
        async for _guess in collection.find():
            guess_list.append(_helper(_guess)["guess"])
        final_list = "\n".join(guess_list)
        embed = discord.Embed(color=0x42F56C)
        embed.add_field(name="All guesses in the database:", value=sorted(final_list))
        embed_message = await ctx.send(embed=embed)
        await embed_message.add_reaction("👀")

    @commands.command(name="lhreport")
    async def run_lh_report(self, ctx):
        guess_list = []
        async for _guess in collection.find():
            guess_list.append(_helper(_guess)["guess"])
        report = PdfReport(filename=f"{ctx.message.author}-report.pdf", guesses=guess_list)
        report.generate()
        share = FileSharer(f"{report.filename}")
        embed = discord.Embed(title="LhGuess report is ready",color=0x42F56C)
        embed.add_field(name="PDF Link:", value=share.share())
        embed_message = await ctx.send(embed=embed)
        await embed_message.add_reaction("✨")

def setup(bot):
    bot.add_cog(LhGuess(bot))
