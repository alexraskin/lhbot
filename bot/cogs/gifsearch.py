import sys
from urllib.parse import quote_plus

import discord
from aiohttp import ContentTypeError
from discord.ext import commands
from sentry_sdk import capture_exception

sys.path.append("../bot")
from config import Settings

conf = Settings()


class Gif(commands.Cog, name="Gif"):
    def __init__(self, client):
        self.client = client

    async def tenor_share_search(self, query: str, gif_id: int) -> bool:
        """
        sends a gif id and search term to the tenor api.. helps with their AI

        read more here https://tenor.com/gifapi/documentation#endpoints-registershare

        :param self: Used to access the bot's state.
        :param query:str: search term from the user
        :param gif_id:int: id of the gif
        :return: a boolean value.
        """
        try:
            async with self.client.session.get(
                f"https://g.tenor.com/v1/registershare?key={conf.tenor_api_key}&id={gif_id}&locale=en_US&q={quote_plus(query)}"
            ) as r:
                if r.status != 200:
                    return False
                else:
                    data = await r.json()
                    if data["status"] == "ok":
                        return True
        except ContentTypeError as e:
            capture_exception(e)
            return False
        except Exception as e:
            capture_exception(e)
            return False

    @commands.command(
        name="gif", aliases=["tenor", "gifsearch", "tenorsearch", "randomgif"]
    )
    async def gif(self, ctx, *, search=None):
        """
        The gif function is used to search for a gif on Tenor using the API.
        It takes in a string as an argument and searches Tenor for that string.
        If there is no string passed to the function, it will return a random gif
        If it finds any results, it will return the first result from Tenor's API.

        :param self: Used to access the bot itself.
        :param ctx: Used to send messages back to the user.
        :param *: Used to grab all the arguments after the command.
        :param search: Used to search for the gifs.
        :return: the gif url.

        :doc-author: Trelent
        """
        q = [search if search else ""]
        try:
            async with self.client.session.get(
                f"https://g.tenor.com/v1/random?key={conf.tenor_api_key}&q={q}&locale=en_US&contentfilter=low&media_filter=basic&ar_range=standard&limit=1"
            ) as r:
                if r.status == 200:
                    data = await r.json()
                    if data["results"]:
                        await self.tenor_share_search(search, data["results"][0]["id"])
                        embed = discord.Embed(
                            title=f'{data["results"][0]["content_description"]}',
                            url=data["results"][0]["url"],
                            color=0x00FF00,
                        )
                        embed.set_image(
                            url=data["results"][0]["media"][0]["gif"]["url"]
                        )
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send("No gifs found")
                else:
                    await ctx.send("No gifs found")
        except ContentTypeError as e:
            capture_exception(e)
            await ctx.send("No gifs found")
        except Exception as e:
            capture_exception(e)
            await ctx.send("No gifs found")


def setup(client):
    """
    The setup function is used to register the commands that will be used in the bot.
    This function is run when you load a cog, and it's what makes your commands usable.

    :param client: Used to access the client's resources.
    :return: a dictionary of information about the bot and server.
    """
    client.add_cog(Gif(client))
