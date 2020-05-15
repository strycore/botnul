# stallman.py
# Bot discord de yishan

import os
import discord
import urllib
import json 
import urbandictionary as ud
import random

from dotenv import load_dotenv
from discord.ext import commands
from quote import list_quotes # quotes personnelles

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    game = discord.Game('niquer le système.')
    await bot.change_presence(status=discord.Status.online,activity=game)

    for guild in bot.guilds:
        if guild.name == GUILD:
            break

        print(
            f'{bot.user} est connecté sur le discord suivant : \n'
            f'{guild.name}(id: {guild.id})\n'
        )

@bot.command(name='ping', help='réponds au ping')
async def ping(ctx):
    test_ping = 'pong'

    response = (test_ping)
    await ctx.send(response)


@bot.command(name='urban', help='Urban Dictionary')
async def urbandef(ctx, term: str):
    result = ud.define(term)
# C'est ici que tu vas interpreter les résultat pour les afficher corectement
    for r in result:
        await ctx.send(r.definition)
        print(r)

# test
@bot.command(name='urban2', help='Urban Dictionary')
async def urbandef2(ctx, term: str): 
    result = ud.random()
    for r in result:
        print(r)
        await ctx.send(r.definition)


@bot.command(name='echo', help='Répète Jacot')
async def echo(ctx, phrase): # phrase est ici la variable qui recevra les mots à répeter
		# maintenant on renvoir la phrase, c'est le bot qui cause...
    await ctx.send(phrase)


@bot.command(name='square', help='Calcule le carré d\'un nombre')
async def square(ctx, number: int):
    result = number * number
    await ctx.send('le résultat est {}'.format(result))

# Quotes

@bot.command(name='quote', help='Choisi et affiche au hazard une citation du chan')
async def show_random_quote(ctx):
    quote = random.choice(list_quotes)
    embed=discord.Embed(title="Quote", color=0x2b2a59)
    embed.set_thumbnail(url="https://share.yishan.io/images/troll_memes_bullshits/elliot.jpg")
    embed.add_field(name='_', value=quote)
    print(embed)
    await ctx.send(embed = embed)

    


bot.run(TOKEN)
