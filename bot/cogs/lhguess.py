from __future__ import annotations

import random
from datetime import datetime
from typing import Optional, TYPE_CHECKING

from bson.objectid import ObjectId
from discord import Embed, app_commands, ui, TextStyle, Interaction, File
from discord.ext import commands
from async_lru import alru_cache
from utils import checks
from utils.banwords import banned_words
from utils.generate_csv import MongoDataProcessor
from utils.hints import lh_hints
from utils.return_helper import helper

if TYPE_CHECKING:
    from ..bot import LhBot


class GuessView(ui.Modal):
    guess = ui.TextInput(
        label="Guess:",
        style=TextStyle.paragraph,
        placeholder="Enter your guess here",
        required=True,
        min_length=1,
        max_length=180,
    )

    def __init__(self) -> None:
        self.guess_text = None
        super().__init__(timeout=60)

    async def on_submit(self, interaction: Interaction) -> None:
        self.interaction = interaction
        self.guess_text = str(self.guess)
        self.stop()


class LhGuess(commands.Cog):
    def __init__(self, client: LhBot) -> None:
        self.client: LhBot = client
        self.banned_words_list = banned_words.split("\n")
        self.hints = lh_hints.split("\n")
        self.error_color = 0xE74C3C
        self.success_color = 0x42F56C
        self.guess_list = []
        self.database = self.client.db_client.lhbot
        self.collection = self.database.get_collection("lhbot_collection")

    @alru_cache(maxsize=32)
    async def load_collection_list(self) -> list:
        async for guess in self.collection.find():
            data = helper(guess)
            self.guess_list.append(
                {"guess": data["guess"], "guessedBy": data["guessedBy"]}
            )
        return self.guess_list

    def check(self, guess: str) -> bool:
        if not str(guess).lower().startswith("l"):
            return False
        if str(guess).lower() in self.banned_words_list:
            return False
        return True

    @commands.hybrid_command()
    @commands.guild_only()
    @app_commands.guild_only()
    @app_commands.describe(guess="Take a guess at what LH means")
    async def lhguess(
        self, ctx: commands.Context, *, guess: Optional[str] = None
    ) -> None:
        """
        Take a guess at what LH means.
        """
        if ctx.guild.id != self.client.config.main_guild:
            await ctx.send("This command can only be used in Cloudy's Discord.")
            return
        if guess is None:
            if ctx.interaction is None:
                await ctx.send("Please provide a guess!")
                return
            else:
                modal = GuessView()
                await ctx.interaction.response.send_modal(modal)
                await modal.wait()
                guess = modal.guess_text
                ctx.interaction = modal.interaction
        if self.check(guess) is False:
            embed = Embed()
            embed.title = "That is not a valid guess 🚨"
            embed.description = (
                "You must start your guess with `L` and it cannot be a banned word."
            )
            embed.color = self.error_color
            embed.timestamp = ctx.message.created_at
            await ctx.send(embed=embed)
            return
        guessed = await self.collection.count_documents({"lhguess": str(guess).lower()})
        if guessed > 0:
            guessed_by = await self.collection.find_one({"lhguess": str(guess).lower()})
            pretty_guessed_by = helper(guessed_by)
            embed = Embed(
                title="This has already been guessed 🚨",
                description=f"LhGuess: {guess}",
                color=self.error_color,
            )
            embed.add_field(
                name="Guessed by:", value=pretty_guessed_by["guessedBy"], inline=True
            )
            embed.add_field(
                name="Guess ID:", value=pretty_guessed_by["id"], inline=True
            )
            embed.timestamp = ctx.message.created_at
            await ctx.send(embed=embed)
            return
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
            await ctx.send(embed=embed)

    @commands.hybrid_command(description="Get the current guess count.")
    @commands.guild_only()
    @app_commands.guild_only()
    async def lhcount(self, ctx: commands.Context):
        """
        Get the current guess count.
        """
        embed = Embed(title="LhGuess Count", color=self.success_color)
        count = await self.load_collection_list()
        embed.add_field(
            name="Current guess Count:", value=f"{len(count)} 🦍", inline=True
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(description="Generate a CSV report of all the guesses.")
    @commands.guild_only()
    @app_commands.guild_only()
    async def lhreport(self, ctx: commands.Context):
        """
        Generate a CSV report of all the guesses.
        """
        if ctx.guild.id != self.client.config.main_guild:
            await ctx.send("This command can only be used in Cloudy's Discord.")
            return
        now = datetime.now()
        file_name_friendly_date = now.strftime("%Y-%m-%d_%H-%M-%S")
        report = MongoDataProcessor(await self.load_collection_list())
        report.export_to_csv(f"lhguess_report_{file_name_friendly_date}.csv")
        await ctx.send(file=File(report.file_path))

    @commands.hybrid_command(description="Get a random hint.")
    @commands.guild_only()
    @app_commands.guild_only()
    async def lhhints(self, ctx: commands.Context):
        """
        Get a random hint.
        """
        embed = Embed(title="Random LH Hint", color=self.success_color)
        random_hint = random.choice(list(self.hints))
        embed.add_field(name="Hint:", value=random_hint, inline=True)

        await ctx.send(embed=embed)

    @commands.hybrid_command()
    @checks.is_mod()
    @commands.guild_only()
    @app_commands.guild_only()
    @app_commands.describe(guess_id="Delete a guess from the database")
    async def lhdelete(self, ctx: commands.Context, guess_id: int):
        """
        Delete a guess from the database.
        """
        if ctx.guild.id != self.client.config.main_guild:
            await ctx.send("This command can only be used in Cloudy's Discord.")
            return
        guess = await self.collection.find_one({"_id": ObjectId(guess_id)})  # type: ignore

        if not guess:
            raise commands.BadArgument("Could not find a guess with that ID!")
        if guess:
            embed = Embed(color=self.success_color, timestamp=ctx.message.created_at)
            embed.add_field(
                name="Succesfully Deleted LhGuess:", value=guess_id, inline=True
            )
            await self.collection.delete_one({"_id": ObjectId(guess_id)})
            embed_message = await ctx.send(embed=embed)
            return

    @commands.hybrid_command()
    @commands.guild_only()
    @app_commands.guild_only()
    async def lhlatest(self, ctx: commands.Context):
        """
        Get the 5 latest guesses.
        """
        # if ctx.guild.id != self.client.config.main_guild:
        #     await ctx.send("This command can only be used in Cloudy's Discord.")
        #     return
        embed = Embed(title="Latest LhGuesses", color=self.success_color)
        guess_list = await self.load_collection_list()
        for guess in guess_list[-5:]:
            embed.add_field(
                name=f"LhGuess: {guess['guess']}",
                value=f"Guessed by: {guess['guessedBy']}",
                inline=False,
            )
        await ctx.send(embed=embed)


async def setup(client: LhBot) -> None:
    await client.add_cog(LhGuess(client))
