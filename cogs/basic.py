import discord
from discord.ext import commands


class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        await ctx.send("こんにちは")


def setup(bot):
    bot.add_cog(Basic(bot))

    