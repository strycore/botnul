"""Bot discord de yishan"""

import os
import re
import json
import logging

import random

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import urbandictionary as ud
from quote import QUOTES  # quotes personnelles

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger("discord")
LOGGER.setLevel(logging.INFO)
MESSAGE_LOGGER = logging.getLogger(__name__)
MESSAGE_HANDLER = logging.FileHandler("devnull.log")
MESSAGE_LOGGER.addHandler(MESSAGE_HANDLER)

load_dotenv()
BOT_NAME = "Botnul"
TOKEN = os.getenv("DISCORD_TOKEN")
MAIN_ID = 844786390578233357
CENSORED_SENTENCES = ("ta gueule",)

CENSORED_WORDS = (
    "tg",
    "menfou",
    "ftg",
)


class BotClient(discord.Client):
    """Discord bot client"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        """The Discord client is ready"""
        game = discord.Game("Au nom de la lune, je vais tous vous punir.")
        await self.change_presence(status=discord.Status.online, activity=game)
        # await self.say_yo.start()

    async def on_message(self, message):
        """Handle received messages"""
        bot_commands = {
            "!ping": self.ping,
            "!urban": self.urbandef,
            "!echo": self.echo,
            "!quote": self.show_random_quote,
            "!podcast": self.show_podcast_quote,
            "!yishan": self.show_yishan_quote,
            "!strider": self.show_strider_quote,
            "!pctony": self.show_pctony_quote,
            "!nuggets": self.show_nuggets_quote,
            "!bak": self.backup_channel,
            "yo": self.reply_yo,
        }
        if message.author == self.user:
            return
        MESSAGE_LOGGER.info("%s: %s", message, message.content)
        words = re.findall(r"\w+", message.content)
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
        command = message.content.split()[0].lower()
        if command in bot_commands:
            await bot_commands[command](
                message.channel, message.content[len(command) + 1 :]
            )

    @tasks.loop(hours=24)
    async def say_yo(self):
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
        # embed.set_thumbnail(url="https://share.yishan.io/images/ud.jpg")
        await channel.send(embed=embed)

    async def echo(self, channel, phrase):
        """Repète Jacquot"""
        await channel.send(phrase + " ducon")

    async def show_random_quote(self, channel, _rien):
        """Balance une quote random"""
        quote = random.choice(QUOTES)
        embed = discord.Embed(title="Quote", description=quote, color=0x0392E1)
        # embed.set_thumbnail(url="https://share.yishan.io/images/quote.png")
        await channel.send(embed=embed)

    async def show_podcast_quote(self, channel, _data):
        await self.send_random_line(channel, "podcast.txt", more=3)

    async def show_yishan_quote(self, channel, _data):
        await self.send_random_line(channel, "quotes-yishan.txt", more=0)

    async def show_strider_quote(self, channel, _data):
        await self.send_random_line(channel, "quotes-strider.txt", more=0)

    async def show_pctony_quote(self, channel, _data):
        await self.send_random_line(channel, "quotes-pctony.txt", more=0)

    async def show_nuggets_quote(self, channel, _data):
        await self.send_random_line(channel, "quotes-nuggets.txt", more=0)

    async def send_random_line(self, channel, filename, more=0):
        def random_line(afile, more=0):
            line = next(afile)
            consume_next = False
            for num, aline in enumerate(afile, 2):
                if consume_next:
                    consume_next -= 1
                    line = line + " " + aline
                    continue
                if random.randrange(num):
                    continue
                line = aline
                consume_next = more
            return line

        podcast_file = open(filename)
        await channel.send(random_line(podcast_file, more=more))

    async def retrieve_all_messages(self, channel):
        messages = []
        last_message_id = channel.last_message_id
        current_message = None
        while True:
            if current_message:
                print(current_message.created_at)
            async for message in channel.history(oldest_first=True, limit=100, after=current_message):
                messages.append(self.serialize_message(message))
                current_message = message
                if message.id == last_message_id:
                    return messages

    async def backup_channel(self, channel, _data):
        messages = await self.retrieve_all_messages(channel)
        with open(f"backup-{channel.name}.json", "w") as backup_file:
            json.dump(messages, backup_file, indent=2)

    def serialize_message(self, message):
        return {
            "id": message.id,
            "channel": {
                "id": message.channel.id,
                "name": message.channel.name,
            },
            "author": {
                "id": message.author.id,
                "name": message.author.name,
                "global_name": message.author.global_name
            },
            "content": message.content,
            "created_at": message.created_at.timestamp(),
            "edited_at": message.edited_at.timestamp() if message.edited_at else None,
            "pinned": message.pinned,
            "embeds": self.serialize_embeds(message.embeds),
            "attachments": self.serialize_attachments(message.attachments),
        }

    def serialize_attachments(self, attachments):
        response = []
        for attachment in attachments:
            response.append({
                "id": attachment.id,
                "description": attachment.description,
                "duration": attachment.duration,
                "filename": attachment.filename,
                "url": attachment.url,
                "height": attachment.height,
                "width": attachment.width,
                "size": attachment.size,
            })
        return response

    def serialize_embeds(self, embeds):
        response = []
        for embed in embeds:
            response.append({
                "type": embed.type,
                "title": embed.title,
                "description": embed.description,
                "url": embed.url,
                "timestamp": embed.timestamp.timestamp() if embed.timestamp else None,
            })
        return response


intents = discord.Intents.default()
intents.message_content = True

DISCORD_NUL_BOT = BotClient(intents=intents)
DISCORD_NUL_BOT.run(TOKEN)
