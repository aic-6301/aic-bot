import discord
from discord.ext import commands
from googletrans import Translator


class Trans(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

translator = Translator()

@commands.command()
async def trans(message):
    # botの発言には反応しない
    if message.author.bot:
        return

    # メッセージの言語判別
    lang = translator.detect(message.content).lang

    # 言語が日本語だったら
    if lang == "ja":
        trans_text = translator.translate(message.content, src = lang, dest = "en").text
        await message.channel.send(trans_text)

    # 言語が英語だったら
    elif lang == "en":
        trans_text = translator.translate(message.content, src = lang, dest = "ja").text
        await message.channel.send(trans_text)

def setup(bot):
    bot.add_cog(Trans(bot))