    # stallman.py
    # Bot discord de yishan

import os
import discord
import urllib
import json 
import urbandictionary as ud

from dotenv import load_dotenv
from discord.ext import commands

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

''' test
@bot.command(name='urban2', help='Urban Dictionary')
async def urbandef2(ctx, term: str): # term est forcément un string ici
	result = await ud.define(term)
    
	# C'est ici que je dois interpreter les résultat pour les afficher correctement
	output = ''
	for r in result: #on cherche pas sur un élément du tableau, mais sur le tableau en entier
		output += ''.join(r.definition)
        
	await ctx.send(output)
'''

@bot.command(name='echo', help='Répète Jacot')
async def echo(ctx, phrase): # phrase est ici la variable qui recevra les mots à répeter
		# maintenant on renvoir la phrase, c'est le bot qui cause...
    await ctx.send(phrase)


@bot.command(name='square', help='Calcule le carré d\'un nombre')
async def square(ctx, number: int):
    result = number * number
    await ctx.send('le résultat est {}'.format(result))

bot.run(TOKEN)