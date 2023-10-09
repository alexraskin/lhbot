import random

from bson.objectid import ObjectId
from discord import Embed, app_commands
from discord.ext import commands, tasks
from utils.banwords import banned_words
from utils.generate_pdf import PdfReport
from utils.hints import lh_hints
from utils.return_helper import helper
from utils.s3_client import S3Upload


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

    @commands.hybrid_group(description="LhGuess Commands", without_command=True)
    @commands.guild_only()
    @app_commands.guild_only()
    async def lh(self, ctx: commands.Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @lh.command()
    @commands.guild_only()
    @app_commands.guild_only()
    @app_commands.describe(guess="Take a guess at what LH means")
    async def guess(self, ctx: commands.Context, guess: str) -> Embed:
        """
        Take a guess at what LH means.
        """
        if not ctx.channel.guild.id == self.client.main_guild.id:
            return

        if not str(guess).lower().startswith("l"):
            embed = Embed(title="Guess not allowed!", color=self.error_color)
            
            embed_message = await ctx.send(embed=embed)
            await embed_message.add_reaction("❌")
            return

        if str(guess).lower() in self.banned_words_list:
            embed = Embed(title="Guess not allowed!", color=self.error_color)
            
            embed_message = await ctx.send(embed=embed)
            await embed_message.add_reaction("❌")
            return

        guessed = await self.collection.count_documents({"lhguess": str(guess).lower()})
        if guessed > 0:
            embed = Embed(
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

    @lh.command()
    @commands.guild_only()
    @app_commands.guild_only()
    async def count(self, ctx: commands.Context) -> Embed:
        """
        Get the current guess count.
        """
        if not ctx.channel.guild.id == self.client.main_guild.id:
            return
        
        embed = Embed(title="LhGuess Count", color=self.success_color)
        embed.add_field(
            name="Current guess Count:", value=f"{len(self.guess_list)} 🦍", inline=True
        )
        await ctx.send(embed=embed)

    @lh.command()
    @commands.guild_only()
    @app_commands.guild_only()
    async def report(self, ctx) -> Embed:
        """
        Generate a PDF report of all the guesses.
        """
        if not ctx.channel.guild.id == self.client.main_guild.id:
            return
        report = PdfReport(
            filename=f"{ctx.message.author}-report.pdf", guesses=self.guess_list
        )
        report.generate()
        share = S3Upload(report.filename)
        share.upload_file()
        embed = Embed(title="LhGuess report is ready", color=self.success_color)
        embed.add_field(name="PDF Link:", value=share.get_url())
        await ctx.send(embed=embed)

    @lh.command()
    @commands.guild_only()
    @app_commands.guild_only()
    async def hints(self, ctx: commands.Context) -> Embed:
        """
        Get a random hint.
        """
        if not ctx.channel.guild.id == self.client.main_guild.id:
            return
        embed = Embed(title="Random LH Hint", color=self.success_color)
        random_hint = random.choice(list(self.hints))
        embed.add_field(name="Hint:", value=random_hint, inline=True)
        
        await ctx.send(embed=embed)

    @lh.command()
    @commands.guild_only()
    @app_commands.guild_only()
    @app_commands.describe(guess_id="Delete a guess from the database")
    async def delete(self, ctx: commands.Context, guess_id: int) -> Embed:
        """
        Delete a guess from the database.
        """
        if not ctx.channel.guild.id == self.client.main_guild.id:
            return
        
        if not self.client.user_is_superuser(ctx.author):
            embed = Embed(
                title="You do not have permisson to run this command!",
                color=self.error_color,
                timestamp=ctx.message.created_at,
            )
            embed_message = await ctx.send(embed=embed)
            await embed_message.add_reaction("🔨")
            return
        guess = await self.collection.find_one({"_id": ObjectId(guess_id)})

        if not guess:
            embed = Embed(
                title=f"Guess with ID: {guess_id} was not found!",
                color=self.error_color,
                timestamp=ctx.message.created_at,
            )
            embed_message = await ctx.send(embed=embed)
            await embed_message.add_reaction("🔨")
            return

        if guess:
            embed = Embed(color=self.success_color, timestamp=ctx.message.created_at)
            embed.add_field(
                name="Succesfully Deleted LhGuess:", value=guess_id, inline=True
            )
            await self.collection.delete_one({"_id": ObjectId(guess_id)})
            embed_message = await ctx.send(embed=embed)
            await embed_message.add_reaction("🔨")
            return


async def setup(client) -> None:
    await client.add_cog(LhGuess(client))
