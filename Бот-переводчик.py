from discord.ext import commands
from deep_translator import GoogleTranslator


# https://discord.gg/VSK6vZN5 - сервер с ботом
TOKEN = 'ODM2MjEzNzc1NzMyMTc4OTc0.YIauxA.qIGCX2O6PDgVHhM-PmPd3IPaP8M'


class Gramotey(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.langs = {}

    @commands.command(name='help_bot')
    async def help(self, ctx):
        await ctx.send('!set_lang [язык-язык] - устанавливает начальный язык и язык перевода.'
                       'Каждый язык является сокращением\n'
                       '!text [текст который нужно перевести] - команда перевода заданного текста')

    @commands.command(name='set_lang')
    async def set_lang(self, ctx: commands.Context, langs=None):
        if langs is None:
            await ctx.send('Я вас не понимаю! Для справки введите !help')
            return
        try:
            one, two = langs.split('-')
            if one not in supported_langs.values() or two not in supported_langs.values():
                await ctx.send('Неверный язык или языки! Повторите команду')
                return
            self.langs[(ctx.guild, ctx.channel)] = (one, two)
            await ctx.send('Язык успешно сменён')
        except Exception:
            await ctx.send('Ошибка в команде! Повторите команду')
            return

    @commands.command(name='text')
    async def translate(self, ctx: commands.Context, line=None):
        if line is None:
            await ctx.send('Я вас не понимаю! Для справки введите !help')
            return
        lang_pair = self.langs[(ctx.guild, ctx.channel)] =\
            self.langs.get((ctx.guild, ctx.channel), ('en', 'ru'))
        one, two = lang_pair
        text = GoogleTranslator(source=one, target=two).translate(line)
        await ctx.send(text)


supported_langs = GoogleTranslator.get_supported_languages(True)
bot = commands.Bot(command_prefix='!')
bot.add_cog(Gramotey(bot))
bot.run(TOKEN)