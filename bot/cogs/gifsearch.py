from typing import Union

from aiohttp import ContentTypeError
from discord import Embed
from discord.ext import commands
from sentry_sdk import capture_exception


class Gif(commands.Cog, name="Gif"):
    def __init__(self, client) -> None:
        self.client = client
        self.base_url = "https://api.giphy.com/v1/"

    async def get_random_giphy_user_id(self) -> Union[str, bool]:
        """
        The get_random_giphy_user_id function is used to get a random user ID from the Giphy API.
        It returns either a string or False, depending on whether it was able to retrieve an ID or not.

        :param self: Used to access the class attributes.
        :return: a random user id from the Giphy API.
        """
        try:
            async with self.client.session.get(
                f"{self.base_url}randomid?api_key={self.client.config.giphy_api_key}"
            ) as response:
                if response.status != 200:
                    self.client.logger.error(
                        "Giphy API returned a non-200 status code."
                    )
                    return False
                else:
                    data = await response.json()
                    return str(data["data"]["random_id"])
        except ContentTypeError as e:
            capture_exception(e)
            self.client.logger.error(f"Error in get_random_giphy_user_id: {e}")
            return False
        except Exception as e:
            self.client.logger.error(f"Error in get_random_giphy_user_id: {e}")
            capture_exception(e)
            return False

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(
        name="gif", aliases=["gifsearch", "randomgif"], description="Search for a gif"
    )
    async def get_random_gif(self, ctx, search: str = None) -> Embed:
        """
        The get_random_gif function is a helper function that retrieves a random gif from the Giphy API.
        It takes in an optional search parameter which will be used to filter the results of the query.
        The get_random_gif function returns an embed object containing a link to the image and its source.

        :param self: Used to access variables that belongs to the class.
        :param ctx: Used to get the context of where the command was called.
        :param *: Used to pass in a list of arguments to the function.
        :param search="": Used to search for a specific keyword.
        :return: a random gif from the giphy api.
        """
        try:
            if search is None:
                url = f"{self.base_url}gifs/trending?api_key={self.client.config.giphy_api_key}&limit=1&offset=0&rating=g&lang=en&random_id={await self.get_random_giphy_user_id()}"
            else:
                url = f"{self.base_url}gifs/search?api_key={self.client.config.giphy_api_key}&q={search}&limit=1&offset=0&rating=g&lang=en&random_id={await self.get_random_giphy_user_id()}"
                async with self.client.session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        if len(data["data"]) == 0:
                            embed = Embed(title="No GIF found!", color=0xFF0000)
                            embed.set_image(
                                url="https://media.giphy.com/media/VbnUQpnihPSIgIXuZv/giphy-downsized.gif"
                            )
                            return await ctx.send(embed=embed)
                        embed = Embed(
                            url=data["data"][0]["images"]["downsized_large"]["url"],
                            color=0x00FF00,
                        )
                        embed.set_image(
                            url=data["data"][0]["images"]["downsized_large"]["url"]
                        )
                        embed.set_footer(text="Powered By GIPHY")
                        await ctx.send(embed=embed)
                    else:
                        self.client.logger.error(
                            f"Error in get_random_gif Status: {response.status}"
                        )
                        await ctx.send("No GIF found")
        except Exception as error:
            self.client.logger.error(f"Error in get_random_gif: {error}")
            capture_exception(error)
            await ctx.send("No GIF found")


async def setup(client):
    """
    The setup function is used to register the commands that will be used in the bot.
    This function is run when you load a cog, and it's what makes your commands usable.

    :param client: Used to access the client's resources.
    :return: a dictionary of information about the bot and server.
    """
    await client.add_cog(Gif(client))
