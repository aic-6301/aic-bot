import discord
from discord.ext import commands
import os
from os import getenv
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
#bot.remove_command("help")


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
        embed = discord.Embed(title=":x: 失敗 -MissingPermissions", description=f"実行者の必要な権限が無いため実行出来ません。", timestamp=ctx.message.created_at, color=discord.Color.red())
        embed.set_footer(text="お困りの場合は、サーバー管理者をメンションしてください。")
        await ctx.send(embed=embed)
    elif isinstance(error, discord.ext.commands.errors.BotMissingPermissions):
        embed = discord.Embed(title=":x: 失敗 -BotMissingPermissions", description=f"Botの必要な権限が無いため実行出来ません。", timestamp=ctx.message.created_at, color=discord.Color.red())
        embed.set_footer(text="お困りの場合は、サーバー管理者をメンションしてください。")
        await ctx.send(embed=embed)
    elif isinstance(error, discord.ext.commands.errors.CommandNotFound):
        embed = discord.Embed(title=":x: 失敗 -CommandNotFound", description=f"不明なコマンドもしくは現在使用不可能なコマンドです。", timestamp=ctx.message.created_at, color=discord.Color.red())
        embed.set_footer(text="お困りの場合は、サーバー管理者をメンションしてください。")
        await ctx.send(embed=embed)
    elif isinstance(error, discord.ext.commands.errors.MemberNotFound):
        embed = discord.Embed(title=":x: 失敗 -MemberNotFound", description=f"指定されたメンバーが見つかりません。", timestamp=ctx.message.created_at, color=discord.Color.red())
        embed.set_footer(text="お困りの場合は、サーバー管理者をメンションしてください。")
        await ctx.send(embed=embed)
    elif isinstance(error, discord.ext.commands.errors.BadArgument):
        embed = discord.Embed(title=":x: 失敗 -BadArgument", description=f"指定された引数がエラーを起こしているため実行出来ません。", timestamp=ctx.message.created_at, color=discord.Color.red())
        embed.set_footer(text="お困りの場合は、サーバー管理者をメンションしてください。")
        await ctx.send(embed=embed) 
    elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        embed = discord.Embed(title=":x: 失敗 -BadArgument", description=f"指定された引数が足りないため実行出来ません。", timestamp=ctx.message.created_at, color=discord.Color.red())
        embed.set_footer(text="お困りの場合は、サーバー管理者をメンションしてください。")
        await ctx.send(embed=embed) 
    else:
        ch = 996370412239855667
        embed = discord.Embed(title="エラー情報", description="")
        embed.add_field(name="エラー発生サーバー名", value=ctx.guild.name, inline=False)
        embed.add_field(name="エラー発生サーバーID", value=ctx.guild.id, inline=False)
        embed.add_field(name="エラー発生ユーザー名", value=ctx.author.name, inline=False)
        embed.add_field(name="エラー発生ユーザーID", value=ctx.author.id, inline=False)
        embed.add_field(name="エラー発生コマンド", value=ctx.message.content, inline=False)

        t = f"```py\n{''.join(traceback.TracebackException.from_exception(error))}```"
        embed.add_field(name="発生エラー", value=t if len(t < 2048) else f"```py\n{error}\n```", inline=False)

        m = await bot.get_channel(ch).send(embed=embed)
        await ctx.send(discord.Embed(title="エラーが発生しました", description="何らかのエラーが発生しました。ごめんなさい。\nこのエラーについて問い合わせるときは下記のエラーIDも一緒にお知らせください").set_footer(text="エラーid:{m.id}"))
        raise error




# restart
def restart_bot(): 
  os.exec(sys.executable, ['python'] + sys.argv)

@bot.command(name= 'restart')
@commands.is_owner()
async def restart(ctx):
  await ctx.send("再起動中...(数秒で完了します)")
  restart_bot()



#loader
@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")
    embed = discord.Embed(title="load!", description=f'{extension} loaded!', color=0xff00c8)
    await ctx.send(embed=embed)

#unloader
@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    embed = discord.Embed(title="unload!", description=f'{extension} unloaded!', color=0xff00c8)
    await ctx.send(embed=embed)
#reload
@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    bot.reload_extension(f"cogs.{extension}")
    embed = discord.Embed(title='Reload', description=f'{extension} successfully reloaded', color=0xff00c8)
    await ctx.send(embed=embed)


@bot.command()
@commands.is_owner()
async def shutdown(ctx):
  await ctx.send('bye!:wave:')
  print(quit())


# ping
@bot.command()
async def ping(ctx):
    await ctx.send(f'pong!{round(bot.latency*1000)} msです')


#token = getenv('DISCORD_BOT_TOKEN')
bot.run(TOKEN)
