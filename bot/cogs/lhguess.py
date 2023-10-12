import random
from typing import Optional

from bson.objectid import ObjectId
from discord import Embed, app_commands, ui, TextStyle, Interaction
from discord.ext import commands, tasks
from utils import checks
from utils.banwords import banned_words
from utils.generate_pdf import PdfReport
from utils.hints import lh_hints
from utils.return_helper import helper
from utils.s3_client import S3Upload


class GuessView(ui.Modal, title="LhGuess"):
    guess = ui.TextInput(
        label="Guess:",
        style=TextStyle.paragraph,
        placeholder="Enter your guess here",
        required=True,
        min_length=1,
        max_length=180,
    )

    def __init__(self):
        self.guess_text = None
        super().__init__(timeout=60)

    async def on_submit(self, interaction: Interaction) -> None:
        self.interaction = interaction
        self.guess_text = str(self.guess)
        self.stop()


class LhGuess(commands.Cog, name="LhGuess"):
    def __init__(self, client: commands.Bot) -> None:
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
        self.guess_list = []
        async for guess in self.collection.find():
            data = helper(guess)
            self.guess_list.append(
                {"guess": data["guess"], "guessedBy": data["guessedBy"]}
            )

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
        self, ctx: commands.Context, guess: Optional[str] = None
    ) -> Embed:
        """
        Take a guess at what LH means.
        """
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
            await ctx.send("That is not a valid guess!", ephemeral=True)
            return
        guessed = await self.collection.count_documents({"lhguess": str(guess).lower()})
        if guessed > 0:
            embed = Embed(
                title="This has already been guessed 🚨",
                description=f"LhGuess: {guess}",
                color=self.error_color,
            )
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
    async def count(self, ctx: commands.Context) -> Embed:
        """
        Get the current guess count.
        """
        embed = Embed(title="LhGuess Count", color=self.success_color)
        embed.add_field(
            name="Current guess Count:", value=f"{len(self.guess_list)} 🦍", inline=True
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(description="Generate a PDF report of all the guesses.")
    @commands.guild_only()
    @app_commands.guild_only()
    async def report(self, ctx: commands.Context) -> Embed:
        """
        Generate a PDF report of all the guesses.
        """
        report = PdfReport(
            filename=f"{ctx.message.author}-report.pdf", guesses=self.guess_list
        )
        report.generate()
        share = S3Upload(report.filename)
        share.upload_file()
        embed = Embed(title="LhGuess report is ready", color=self.success_color)
        embed.add_field(name="PDF Link:", value=share.get_url())
        await ctx.send(embed=embed)

    @commands.hybrid_command(description="Get a random hint.")
    @commands.guild_only()
    @app_commands.guild_only()
    async def hints(self, ctx: commands.Context) -> Embed:
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
    async def delete(self, ctx: commands.Context, guess_id: int) -> Embed:
        """
        Delete a guess from the database.
        """
        guess = await self.collection.find_one({"_id": ObjectId(guess_id)})

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


async def setup(client) -> None:
    await client.add_cog(LhGuess(client))
