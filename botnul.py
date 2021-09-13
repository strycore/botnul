"""Bot discord de yishan"""
import os
import re
import logging

import random

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import urbandictionary as ud
from quote import QUOTES  # quotes personnelles

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger('discord')
LOGGER.setLevel(logging.INFO)
MESSAGE_LOGGER = logging.getLogger(__name__)
MESSAGE_HANDLER = logging.FileHandler('devnull.log')
MESSAGE_LOGGER.addHandler(MESSAGE_HANDLER)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
MAIN_ID = 449724925725376513
CENSORED_SENTENCES = (
    "ta gueule",
)

CENSORED_WORDS = (
    "tg",
    "menfou",
    "ftg",
)



class BotClient(discord.Client):
    """Discord bot client"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.say_yo.start()

    async def on_ready(self):
        """The Discord client is ready"""
        game = discord.Game("Au nom de la lune, je vais tous vous punir.")
        await self.change_presence(status=discord.Status.online, activity=game)

    async def on_message(self, message):
        """Handle received messages"""
        bot_commands = {
            # "!ping": self.ping,
            # "!urban": self.urbandef,
            # "!echo": self.echo,
            # "!help": self.rtfm,
            # "!rtfm": self.rtfm,
            # "!quote": self.show_random_quote
            # "yo": self.reply_yo
        }
        MESSAGE_LOGGER.info("%s: %s", message, message.content)
        print(message)
        words = re.findall(r'\w+', message.content)
        if not words:
            return
        sentence = message.content.strip().lower()
        if sentence in CENSORED_SENTENCES:
            await message.delete()
            return
        for word in words:
            if word in CENSORED_WORDS:
                await message.delete()
                return
        command = message.content.split()[0]
        if command in bot_commands:
            await bot_commands[command](message.channel, message.content[len(command) + 1:])

    @tasks.loop(hours=24) # task runs every 60 seconds
    async def say_yo(self):
        """Wait until the bot logs in"""
        channel = self.get_channel(MAIN_ID)
        await channel.send("yo")

    @say_yo.before_loop
    async def before_say_yo(self):
        """Wait until the bot logs in"""
        await self.wait_until_ready()

    async def reply_yo(self, channel, _payload):
        """Reply with 'yo'"""
        await channel.send("yo")

    async def ping(self, channel, _payload):
        """Sends pong"""
        await channel.send("pong")

    async def urbandef(self, channel, term):
        """Cherche une def sur Urban"""
        response = ud.define(term)
        if not response:
            await channel.send("Ça existe pas ta merde.")
            return
        response = response[0]
        response.definition = response.definition.replace("[", "**")
        response.definition = response.definition.replace("]", "**")
        response.example = response.example.replace("[", "**")
        response.example = response.example.replace("]", "**")
        embed = discord.Embed(title=term, color=0x0392E1)
        if len(response.definition) > 1000:
            concat = response.definition[:995] + "\n**[...]**"
        else:
            concat = response.definition

        embed.add_field(name="**definition** :\n", value=concat, inline=False)
        embed.add_field(name="**example** :\n", value=response.example)
        embed.set_thumbnail(url="https://share.yishan.io/images/ud.jpg")
        await channel.send(embed=embed)

    async def echo(self, channel, phrase):
        """Repète Jacquot"""
        await channel.send(phrase + " ducon")

    async def show_random_quote(self, channel, _rien):
        """Balance une quote random"""
        quote = random.choice(QUOTES)
        embed = discord.Embed(title="Quote", description=quote, color=0x0392E1)
        embed.set_thumbnail(url="https://share.yishan.io/images/quote.png")
        await channel.send(embed=embed)

    async def rtfm(self, channel, _payload):
        """Fuck you"""
        await channel.send("RTFM!")


DISCORD_NUL_BOT = BotClient()
DISCORD_NUL_BOT.run(TOKEN)
