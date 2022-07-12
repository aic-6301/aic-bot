import discord
from discord.ext import commands


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

@commands.command()
async def user(self, ctx, member : discord.Member):
    embed = discord.Embed(title=f'{member}の詳細', description='詳細だよ', color=discord.Color.orange())
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name='名前', value=f'**{member.display_name}#{member.discriminator}**')
    embed.add_field(name='あなたはBot?', value=member.bot)
    embed.add_field(name='ID', value=member.id)
    embed.add_field(name='作成時間', value=member.created_at)
    embed.add_field(name='サーバーに参加した時間', value=member.joined_at)
    await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Info(bot))