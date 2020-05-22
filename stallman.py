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
    game = discord.Game('un pingouin qui fait du ski.')
    await bot.change_presence(status=discord.Status.online,activity=game)

    for guild in bot.guilds:
        if guild.name == GUILD:
            print(
            f'{bot.user} est connecté sur le discord suivant : \n'
            f'{guild.name}(id: {guild.id})\n'
        )

@bot.command(name='ping', help='réponds au ping')
async def ping(ctx):
    test_ping = 'pong'

    response = (test_ping)
    await ctx.send(response)

# UD

@bot.command(name='urban', help='Urban Dictionary')
async def urbandef(ctx, term):
    r = ud.define(term)[0]
    r.definition = r.definition.replace('[','**')
    r.definition = r.definition.replace(']','**')
    r.example = r.example.replace('[','**')
    r.example = r.example.replace(']','**')
    embed = discord.Embed(title=term, color=0x0392e1)
    if len(r.definition) > 1000 :
        concat = r.definition[:995] + "\n**[...]**"
    else:
        concat = r.definition

    embed.add_field(name = '**definition** :\n', value = concat, inline=False)
    embed.add_field(name = '**example** :\n', value = r.example)
    embed.set_thumbnail(url="https://share.yishan.io/images/ud.jpg")
    await ctx.send(embed = embed)
    print(r)

# echo

@bot.command(name='echo', help='Répète Jacot')
async def echo(ctx, phrase):
    await ctx.send(phrase)

# Square

@bot.command(name='square', help='Calcule le carré d\'un nombre')
async def square(ctx, number: int):
    result = number * number
    await ctx.send('le résultat est {}'.format(result))

# Quotes

@bot.command(name='quote', help='Choisi et affiche au hazard une citation du chan')
async def show_random_quote(ctx):
    quote = random.choice(list_quotes)
    embed=discord.Embed(title="Quote", description=quote, color=0x0392e1)
    embed.set_thumbnail(url="https://share.yishan.io/images/quote.png")
    await ctx.send(embed = embed)


bot.run(TOKEN)
