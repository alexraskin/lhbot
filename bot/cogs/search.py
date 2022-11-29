from discord.ext import commands
from duckduckgo_search import ddg
from sentry_sdk import capture_exception


class Search(commands.Cog, name="Search"):
    def __init__(self, client: commands.Bot):
        """
        General commands
        :param self: Used to refer to the object itself.
        :param client: Used to pass the client object to the class.
        :return: the object of the class.
        """
        self.client = client

    @staticmethod
    def get_ddg(keywords, region="us-en", safesearch="On", max_results=1):
        return ddg(
            keywords, region=region, safesearch=safesearch, max_results=max_results
        )

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.hybrid_command(
        name="search",
        aliases=["lmgtfy", "duck", "duckduckgo", "google"],
        description="Search something on DuckDuckGo",
    )
    async def search(self, ctx: commands.Context, query: str = None):
        """
        The search function searches the web for the user's query.
        :param ctx: Used to get the context of where the command was called.
        :param query: Used to store the user's query.
        :return: a link to the search results.
        """

        if ctx.interaction:
            if query is None:
                await ctx.send("Please provide a search query.")
                return

        if query is None:
            await ctx.send("Please provide a search query.")
            return

        await ctx.typing()

        message = await ctx.send("Searching DuckDuckGo...")

        try:
            search_results = self.get_ddg(query)
        except Exception as error:
            self.client.logger.error(f"Error in search: {error}")
            capture_exception(error)
            await message.edit("Something went wrong while searching DuckDuckGo.")
            return

        await message.edit(
            content=f"Search results for *{query}*:"
            + f"\n**Title**: {search_results[0]['title']}"
            + f"\n**Link**: {search_results[0]['href']}"
            + f"\n**Text**: {search_results[0]['body']}"
        )


async def setup(client):
    """
    The setup function is used to add the cog to the client.
    :param client: Used to pass the client object to the class.
    :return: None.
    """
    await client.add_cog(Search(client))
