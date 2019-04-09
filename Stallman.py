import time
import discord
import asyncio
import urbandictionary as ud
import sys
import json
import requests
from bs4 import BeautifulSoup

client = discord.Client()

@client.event

# Mise en route
async def on_ready():
    print("Logged in as:", client.user.name)
    print("ID:", client.user.id)

# Ping 
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    elif message.content == "!ping":
        timePing = time.monotonic()
        pinger = await client.send_message(message.channel, ":ping_pong: **Pong !**")
        ping = '%.2f' % ( 1000 * (time.monotonic() - timePing))
        await client.edit_message(pinger, ":ping_pong: **Pong !**\n `Latence : " + ping + " ms`" )

# UrbanDictionary


# ID
client.run("NTQzNDQ5Nzk3NDc5MTA0NTEy.XKeXJA.ZkhDIMixUjuJMG2VvWskRSOeK-Q")