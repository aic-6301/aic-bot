from copy import error
from decimal import ExtendedContext
from distutils import extension
from tkinter import E
import discord
from discord.ext import commands
import os
import traceback
import sys
import datetime


BACKUP_CHANNEL_ID = 995463878257430558
DEFAULT_PREFIX = 'a!'
TOKEN = 'token'

def _change_command_prefix(bot: commands.Bot, msg: discord.Message):
    if str(msg.guild.id) in prefix_dict.keys():
        return prefix_dict[str(msg.guild.id)]
    else:
        return DEFAULT_PREFIX

online_ch = 995966254512885840
bot = commands.Bot(command_prefix=_change_command_prefix, activity=discord.Activity(name='Aicybot', type=discord.ActivityType.playing), status="idle")
bot.remove_command("help")

INITIAL_EXTENSIONS = ["cogs.tenki", "cogs.bot"]

async def greet():
    channel = bot.get_channel(online_ch)
    embed = discord.Embed(title='起動通知', description='起動したよ！！！', footer=f'現在の時刻：{datetime}')
    await channel.send(embed=embed)
 
# ready
@bot.event
async def on_ready():

    global backup_ch
    global prefix_dict

    backup_ch = await bot.fetch_channel(BACKUP_CHANNEL_ID)
    prefix_dict = {}

    async for m in backup_ch.history():
        splited = m.content.split(' ', 1)
        prefix_dict[splited[0]] = splited[1]
    await greet()
print(f"{bot.user} で起動したよ")


for fn in os.listdir("./cogs"):
    if fn.endswith(".py"):
        bot.load_extension(f"cogs.{fn[:-3]}")


@bot.command(aliases=['cp'])
async def change_prefix(ctx, new_prefix: str = None):
    guild_id = str(ctx.guild.id)
    if new_prefix == None:
        if guild_id in prefix_dict.keys():
            old_prefix = prefix_dict[guild_id]
            async for m in backup_ch.history():
                if m.content.startswith(guild_id):
                    await m.delete()
            prefix_dict.pop(guild_id)
            await ctx.send(embed=discord.Embed(title='このサーバーのプレフィックスがリセットされたよ！', description=f'{old_prefix} -> default({DEFAULT_PREFIX})',))
            return
        else:
            return

    if guild_id in prefix_dict.keys():
        async for m in backup_ch.history():
            if m.content.startswith(guild_id):
                await m.edit(content=f'{guild_id} {new_prefix}')
                break
        old_prefix = prefix_dict[guild_id]
        prefix_dict.pop(guild_id)
        prefix_dict[guild_id] = new_prefix
        await ctx.send(embed=discord.Embed(title='このサーバーのプレフィックスが変更されたよ！', description=f'{old_prefix} -> {prefix_dict[guild_id]}\nこの機能はBeta版です'))
        return

    else:
        await backup_ch.send(f'{guild_id} {new_prefix}')
        prefix_dict[guild_id] = new_prefix
        await ctx.send(embed=discord.Embed(title='このサーバーのプレフィックスが変更されたよ！', description=f'default({DEFAULT_PREFIX}) -> {prefix_dict[guild_id]}'))
        return





# えらー
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        embed = discord.Embed(title=":x: 失敗 -MissingPermissions", description=f"実行者の必要な権限が無いため実行出来ません。", timestamp=ctx.message.created_at, color=discord.Colour.red())
        embed.set_footer(text="お困りの場合は、サーバー管理者をメンションしてください。")
        await ctx.send(embed=embed)
    elif isinstance(error, discord.ext.commands.errors.BotMissingPermissions):
        embed = discord.Embed(title=":x: 失敗 -BotMissingPermissions", description=f"Botの必要な権限が無いため実行出来ません。", timestamp=ctx.message.created_at, color=discord.Colour.red())
        embed.set_footer(text="お困りの場合は、サーバー管理者をメンションしてください。")
        await ctx.send(embed=embed)
    elif isinstance(error, discord.ext.commands.errors.CommandNotFound):
        embed = discord.Embed(title=":x: 失敗 -CommandNotFound", description=f"不明なコマンドもしくは現在使用不可能なコマンドです。", timestamp=ctx.message.created_at, color=discord.Colour.red())
        embed.set_footer(text="お困りの場合は、サーバー管理者をメンションしてください。")
        await ctx.send(embed=embed)
    elif isinstance(error, discord.ext.commands.errors.MemberNotFound):
        embed = discord.Embed(title=":x: 失敗 -MemberNotFound", description=f"指定されたメンバーが見つかりません。", timestamp=ctx.message.created_at, color=discord.Colour.red())
        embed.set_footer(text="お困りの場合は、サーバー管理者をメンションしてください。")
        await ctx.send(embed=embed)
    elif isinstance(error, discord.ext.commands.errors.BadArgument):
        embed = discord.Embed(title=":x: 失敗 -BadArgument", description=f"指定された引数がエラーを起こしているため実行出来ません。", timestamp=ctx.message.created_at, color=discord.Colour.red())
        embed.set_footer(text="お困りの場合は、サーバー管理者をメンションしてください。")
        await ctx.send(embed=embed) 
    elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        embed = discord.Embed(title=":x: 失敗 -BadArgument", description=f"指定された引数が足りないため実行出来ません。", timestamp=ctx.message.created_at, color=discord.Colour.red())
        embed.set_footer(text="お困りの場合は、サーバー管理者をメンションしてください。")
        await ctx.send(embed=embed) 
    else:
        error
        embed = discord.Embed(title=":x: 失敗 -BadArgument", description=f"不明なエラーが発生しました。", timestamp=ctx.message.created_at, color=discord.Colour.red())
        embed.set_footer(text="お困りの場合は、サーバー管理者をメンションしてください。")
        await ctx.send(embed=embed) 
        raise error




#serverinfo
@bot.command()
async def serverinfo(ctx):
    guild = 984807772333932594
    roles =[role for role in guild.role]
    text_channels = [text_channels for text_channels in guild.text_channels]
    #embedのないよう
    embed = discord.Embed(title=f"サーバー情報 - {guild.name}",timestamp=ctx.message.created_at,color=discord.Colour.purple(),inline=False)
    embed.set.thumbnail(url=ctx.guild.icon.url)
    embed.add_field(name="サーバー名",value=f"{guild.name}",inline=False)
    embed.add_field(name="サーバー地域",value=f"{ctx.guild.region}",inline=False)
    embed.add_field(name="サーバー設立日",value=f"{guild.created.at}",inline=False)
    embed.add_field(name="サーバーオーナー",value=f"{guild.owner}",inline=False)
    embed.add_field(name="チャンネル数",value=f"{len(text_channels)}",inline=False)
    embed.add_field(name="ロール数",value=f"{guild.role}",inline=False)
    embed.add_field(name="サーバーブースト数",value=guild.premium_subscription_count,inline=False)
    embed.add_field(name="メンバー数",value=guild.member_count,inline=False)
    embed.set_footer(text=f"実行者：{ctx.author} ",icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
# 天気読み込み
# ./cogs/tenli.pyにかくよてい
# ping
@bot.command()
async def ping(ctx):
    await ctx.send(f'pong!{round(bot.latency*1000)} msです')


# token = getenv('DISCORD_BOT_TOKEN')
bot.run('OTczOTI4NzkzMTU0NjYyNDEw.GjWaR2.YJrhAsrSjM_I8-O9Xot5Ws4kejhFzCJWThA3Sg')
