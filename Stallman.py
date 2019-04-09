import asyncio
import json
import random
import sys
import time
from urllib.parse import quote as urlquote
from urllib.request import urlopen

import discord
import requests
import urbandictionary as ud
from bs4 import BeautifulSoup

client = discord.Client()

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

# Hello

    elif message.content == "!hello":
        await client.send_message(message.channel, "Hello!")

# UrbanDictionary
      
    elif message.content == "!urban":
        UD_DEFID_URL = 'https://api.urbandictionary.com/v0/define?defid='
        UD_DEFINE_URL = 'https://api.urbandictionary.com/v0/define?term='
        UD_RANDOM_URL = 'https://api.urbandictionary.com/v0/random'
        class UrbanDefinition(object):
            def __init__(self, word, definition, example, upvotes, downvotes):
                self.word = word
                self.definition = definition
                self.example = example
                self.upvotes = upvotes
                self.downvotes = downvotes

            def __str__(self):
                return '%s: %s%s (%d, %d)' % (
                        self.word,
                        self.definition[:50],
                        '...' if len(self.definition) > 50 else '',
                        self.upvotes,
                        self.downvotes
                    )

        def _get_urban_json(url):
            f = urlopen(url)
            data = json.loads(f.read().decode('utf-8'))
            f.close()
            return data

        def _parse_urban_json(json, check_result=True):
            result = []
            if json is None or any(e in json for e in ('error', 'errors')):
                raise ValueError('UD: Invalid input for Urban Dictionary API')
            if check_result and ('list' not in json or len(json['list']) == 0):
                return result
            for definition in json['list']:
                d = UrbanDefinition(
                        definition['word'], 
                        definition['definition'],
                        definition['example'],
                        int(definition['thumbs_up']),
                        int(definition['thumbs_down'])
                    )
                result.append(d)
            return result

        '''def define(term):
            """Search for term/phrase and return list of UrbanDefinition objects.
            Keyword arguments:
            term -- term or phrase to search for (str)
            """
            json = _get_urban_json(UD_DEFINE_URL + urlquote(term))
            return _parse_urban_json(json)

        def defineID(defid):
            """Search for UD's definition ID and return list of UrbanDefinition objects.
            Keyword arguments:
            defid -- definition ID to search for (int or str)
            """
            json = _get_urban_json(UD_DEFID_URL + urlquote(str(defid)))
            return _parse_urban_json(json)

        def random():
            """Return random definitions as a list of UrbanDefinition objects."""
            json = _get_urban_json(UD_RANDOM_URL)
        return _parse_urban_json(json, check_result=False)'''
        
# ID
client.run("NTQzNDQ5Nzk3NDc5MTA0NTEy.XKeXJA.ZkhDIMixUjuJMG2VvWskRSOeK-Q")
