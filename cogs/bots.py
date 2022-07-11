from inspect import BoundArguments
from json import tool
from typing_extensions import Self
import discord
from discord.ext import commands
import os
import traceback
import asyncio
import datetime
import sys

@commands.command()
async def help(self,ctx):
    embed = discord.Embed(title=f"help",timestamp=ctx.message.created_at,color=discord.Colour.purple(),inline=False)
    embed.set.thumbnail(url=ctx.guild.icon.url)
    #embed.add_field(vaule=f"このbotのプレフィックスは「{}」です。コマンドの前につけてください")
    embed.add_field(name="help",value=f"このコマンドです。\nbotのコマンドについて書かれています、",inline=False)
    embed.add_field(name="serverinfo",value=f"サーバー情報が取得できます。",inline=False)
    embed.add_field(name="tenki",value="天気が取得できます",inline=False)
    embed.set_footer(text=f"実行者：{ctx.author} ",icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
  

@commands.command(name= 'stop')
@commands.is_owner()
async def stop(ctx):
    await ctx.send("bye!:wave:")
    print(sys.exit())




# restart
def restart_bot(): 
  os.execv(sys.executable, ['python'] + sys.argv)

@commands.command(name= 'restart')
@commands.is_owner()
async def restart(self, ctx):
  await ctx.send("再起動中...(数秒で完了します)")
  restart_bot()


\
#loader
@commands.command()
@commands.is_owner()
async def load(self, ctx, extension):
    self.bot.load_extension(f"cogs.{extension}")
    embed = discord.Embed(title="load!", description=f'{extension} loaded!', color=0xff00c8)
    await ctx.send(embed=embed)

#unloader
@commands.command()
@commands.is_owner()
async def unload(self, ctx, extension):
    self.bot.unload_extension(f"cogs.{extension}")
    embed = discord.Embed(title="unload!", description=f'{extension} unloaded!', color=0xff00c8)
    await ctx.send(embed=embed)
#reload
@commands.command()
@commands.is_owner()
async def reload(self, ctx, extension):
    self.bot.reload_extension(f"cogs.{extension}")
    embed = discord.Embed(title='Reload', description=f'{extension} successfully reloaded', color=0xff00c8)
    await ctx.send(embed=embed)


@commands.command()
@commands.is_owner()
async def shutdown(self, ctx):
  await ctx.send('bye!:wave:')
  print(quit())

def setup(bot):
  bot.add_cog(tool(bot))