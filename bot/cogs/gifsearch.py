import json
import random
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
        self.base_url = "https://g.tenor.com/v1/"

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
                f"{self.base_url}registershare?key={conf.tenor_api_key}&id={gif_id}&locale=en_US&q={quote_plus(query)}"
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
        It takes in a string as an argument and a return a random gif from the Tenor API.

        :param self: Used to access variables that belongs to the class.
        :param ctx: Used to access the bot's commands and send messages.
        :param *: Used to pass in unlimited amount of arguments.
        :param search=None: Used to pass the search term to the function.
        :return: the url of the gif, which is then used to embed it in the message.
        """
        gif_list = []
        query = [search if search else ""]
        try:
            async with self.client.session.get(
                f"{self.base_url}search?key={conf.tenor_api_key}&q={query}&media_filter=basic&contentfilter=low&locale=en_US&ar_range=standard&limit=30"
            ) as r:
                if r.status == 200:
                    data = await r.content.read()
                    payload = json.loads(data)
                    for media in payload["results"]:
                        url = media["media"][0]["gif"]["url"]
                        id = media["id"]
                        title = media["content_description"]
                        gif_list.append(
                            {
                                "url": url,
                                "id": id,
                                "title": title,
                            }
                        )
                    r_gif = random.choice(gif_list)
                    await self.tenor_share_search(search, r_gif["id"])
                    embed = discord.Embed(
                        title=r_gif["title"],
                        url=r_gif["url"],
                        color=0x00FF00,
                    )
                    embed.set_image(url=r_gif["url"])
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("No GIF found")
        except ContentTypeError as e:
            capture_exception(e)
            await ctx.send("No GIF found")
        except Exception as e:
            capture_exception(e)
            await ctx.send("No GIF found")


def setup(client):
    """
    The setup function is used to register the commands that will be used in the bot.
    This function is run when you load a cog, and it's what makes your commands usable.

    :param client: Used to access the client's resources.
    :return: a dictionary of information about the bot and server.
    """
    client.add_cog(Gif(client))
