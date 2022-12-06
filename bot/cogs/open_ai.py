import openai

from discord.ext import commands


class OpenAI(commands.Cog, name="Openai"):
    """
    """

    def __init__(self, client: commands.Bot):
        """
        """
        self.client = client
        self.ai = openai
        openai.api_key = self.client.config.openai_api_key

    @commands.hybrid_command(
      name="openai-text",
      description="Generates text using OpenAI's GPT-3 API.",
      aliases=["openai-gpt3", "openai-gpt-3", "openai-gpt"]
      )
    async def openai_text(self, ctx: commands.Context, prompt: str = None):
        """
        """
        if prompt is None:
          await ctx.send("Please provide a prompt.")
        try:
          response = self.ai.Completion.create(
              engine="davinci",
              prompt=prompt,
              temperature=0.9,
              max_tokens=150,
              top_p=1,
              frequency_penalty=0,
              presence_penalty=0.6,
              stop=["\n", " Human:", " AI:"]
          )
        except Exception as e:
          self.client.logger.error(e)
          await ctx.send("An error occurred during the request. Please try again later.")

        if len(response.choices[0].text) > 2000:
            await ctx.send("The response was too long to send.")
        else:
          await ctx.send(response.choices[0].text)

    @commands.hybrid_command(
      name="openai-image",
      description="Generates an image using OpenAI's GPT-3 API.",
      aliases=["openai-gpt3-image", "openai-gpt-3-image", "openai-gpt-image"]
      )
    async def openai_image(self, ctx: commands.Context, prompt: str = None):
      if prompt is None:
        await ctx.send("Please provide a prompt.")
      try:
        response = self.ai.Image.create(
          prompt=prompt,
          n=1,
          size="1024x1024"
          )
      except Exception as e:
        self.client.logger.error(e)
        await ctx.send("An error occurred during the request. Please try again later.")
      await ctx.send(response['data'][0]['url'])


async def setup(client: commands.Bot):
    """
    """
    await client.add_cog(OpenAI(client))
