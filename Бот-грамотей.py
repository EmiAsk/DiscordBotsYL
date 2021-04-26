from discord.ext import commands
from pymorphy2 import MorphAnalyzer


# https://discord.gg/VSK6vZN5 - сервер с ботом
TOKEN = 'ODM2MjEzNzc1NzMyMTc4OTc0.YIauxA.qIGCX2O6PDgVHhM-PmPd3IPaP8M'


class Gramotey(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help_bot')
    async def help(self, ctx):
        await ctx.send('!numerals [слово] [число] - согласовывает число со словом\n'
                       '!alive [слово] - определяет живое ли существительное или нет\n'
                       '!noun [падеж: nomn, gent, datv, accs, ablt, loct] [число: single,'
                       'plural] -\n'
                       'склоняет существительное по падежу и числу\n!inf [слово]\n'
                       '- выводит слово в начальной форме\n!morph [слово] - производит'
                       'морфологический анализ слова')

    @commands.command(name='numerals')
    async def numerals(self, ctx, word=None, num=None):
        if word is None or num is None or not num.isdigit():
            await ctx.send('Я вас не понимаю! Для справки введите !help')
            return
        word = morph.parse(word)[0]
        if word.tag.POS != 'NOUN':
            await ctx.send('Слово не существительное!')
            return
        await ctx.send(f'{num} {word.make_agree_with_number(int(num)).word}')

    @commands.command(name='alive')
    async def alive(self, ctx, word=None):
        if word is None:
            await ctx.send('Я вас не понимаю! Для справки введите !help')
            return
        word = morph.parse(word)[0]
        if word.tag.POS != 'NOUN':
            await ctx.send('Слово не существительное!')
            return

        msg = morph.parse('живой')[1].inflect({word.tag.number, word.tag.gender}).word
        if 'inan' in word.tag:
            msg = 'не' + msg
        await ctx.send(f'{word.word} {msg}')

    @commands.command(name='noun')
    async def noun(self, ctx, word=None, case=None, number=None):
        if word is None or case is None or number is None:
            await ctx.send('Я вас не понимаю! Для справки введите !help')
            return
        if case not in 'nomn, gent, datv, accs, ablt, loct'.split(', '):
            await ctx.send('Падежа не существует! ')
            return
        elif number not in ['sing', 'plur']:
            await ctx.send('Числа не существует (sing, plur)!')
            return

        word = morph.parse(word)[0]
        msg = word.inflect({case, number}).word
        await ctx.send(msg)

    @commands.command(name='inf')
    async def inf(self, ctx, word=None):
        if word is None:
            await ctx.send('Я вас не понимаю! Для справки введите !help')
            return

        word = morph.parse(word)[0].normal_form
        await ctx.send(word)

    @commands.command(name='morph')
    async def morph(self, ctx, word=None):
        if word is None:
            await ctx.send('Я вас не понимаю! Для справки введите !help')
            return

        word = morph.parse(word)[0]
        msg = f'Слово: {word.word}\nЧасть речи: {word.tag.POS}\nПадеж: {word.tag.case}\n' \
              f'Число: {word.tag.number}\nРод: ' \
              f'{word.tag.gender}\nОдушевленное или нет: ' \
              f'{word.tag.animacy}\nВремя: {word.tag.tense}'
        await ctx.send(msg)


morph = MorphAnalyzer()

bot = commands.Bot(command_prefix='!')
bot.add_cog(Gramotey(bot))
bot.run(TOKEN)