from asyncio import sleep
import discord
from discord import Message


# https://discord.gg/VSK6vZN5 - сервер с ботом
TOKEN = 'ODM2MjEzNzc1NzMyMTc4OTc0.YIauxA.qIGCX2O6PDgVHhM-PmPd3IPaP8M'


class TimerBot(discord.Client):
    async def on_ready(self):
        print(f'Я подключился к серверу! Готов ставить таймер!')
        for guild in self.guilds:
            print(
                f'{self.user} подключился к чату:\n'
                f'{guild.name}(id: {guild.id})\n')

    async def on_message(self, message: Message):
        if message.author == self.user:
            return
        words = message.content.split()
        try:
            if len(words) != 6:
                raise ValueError

            cmd = words[0]
            one, two = int(words[2]), int(words[4])
            other = ' '.join([words[j] for j in [1, 3, 5]])

            if cmd != 'set_timer' or other != 'in hours minutes':
                raise ValueError

            await message.channel.send(f'The timer should start in {one} hours and {two} minutes.')
            await sleep(3600 * one + 60 * two)
            await message.channel.send('Time X has come!')

        except (IndexError, ValueError):
            await message.channel.send('Я вас не понимаю! Команда должна быть такой:\n\n'
                                       'set_timer in [целое число] hours [целое число] minutes')


client = TimerBot()
client.run(TOKEN)
