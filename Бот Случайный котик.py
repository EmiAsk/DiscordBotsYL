from requests import get
import discord
from discord import Message


# https://discord.gg/VSK6vZN5 - сервер с ботом
TOKEN = 'ODM2MjEzNzc1NzMyMTc4OTc0.YIauxA.qIGCX2O6PDgVHhM-PmPd3IPaP8M'


class CatsAndDogs(discord.Client):
    async def on_ready(self):
        print(f'Я подключился к серверу! Готов показать котика или пёсика!')

    async def on_message(self, message: Message):
        if message.author != self.user:
            if 'кот' in message.content.lower():
                picture = get('https://api.thecatapi.com/v1/images/search').json()[0]['url']
                await message.channel.send(picture)
            elif 'соба' in message.content.lower() or 'пёс' in message.content.lower():
                picture = get('https://dog.ceo/api/breeds/image/random').json()['message']
                await message.channel.send(picture)


client = CatsAndDogs()
client.run(TOKEN)
