# stallman.py
# Bot discord de yishan

import os
import discord

from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')
client = discord.Client()

@client.event
async def on_ready():
    game = discord.Game('Attends que Yιѕнαи le code')
    await client.change_presence(status=discord.Status.online,activity=game)

    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} est connecté sur le discord suivant : \n'
        f'{guild.name}(id: {guild.id})\n'
    )

@bot.command(name='ping', help='réponds au ping')
async def ping(ctx):
    test_ping = 'pong'

    response = (test_ping)
    await ctx.send(response)

client.run(TOKEN)
bot.run(TOKEN)
