from distutils.log import info
from wsgiref.simple_server import server_version
import discord
from discord.ext import commands


@commands.command()
async def serverinfo(self,ctx):
    guild = ctx.message.guild
    roles =[role for role in guild.role]
    text_channels = [text_channels for text_channels in guild.text_channels]
    #embedのないよう
    embed = discord.Embed(title=f"サーバー情報 - {guild.name}",timestamp=ctx.message.created_at,color=discord.Colour.purple(),inline=False)
    embed.set.thumbnail(url=ctx.guild.icon.url)
    embed.add_field(name="サーバー名",value=f"{guild.name}",inline=False)
    embed.add_field(name="サーバー地域",value=f"{ctx.guild.region}",inline=False)
    embed.add_field(name="サーバー設立日",value=guild.created.at,inline=False)
    embed.add_field(name="サーバーオーナー",value=guild.owner,inline=False)
    embed.add_field(name="チャンネル数",value=f"{len(text_channels)}",inline=False)
    embed.add_field(name="ロール数",value=f"{len(roles)}",inline=False)
    embed.add_field(name="サーバーブースト数",value=guild.premium_subscription_count,inline=False)
    embed.add_field(name="メンバー数",value=guild.member_count,inline=False)
    embed.set_footer(text=f"実行者：{ctx.author} ",icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
    

async def setup(bot):
  await bot.add_cog(info(bot))