# JustinBot.py
"""
@author: Nikhil Devanathan, Justin Weiler
This script handles the functionality of JustinBot, a discord bot that dispenses imprompteau math lessons.
"""
# Default packages
import os

# Installed packages
import discord
from dotenv import load_dotenv

# The bot secrets are stored in a local .env file for security
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

# Fires when the bot connects to a serevr it has joined. Exists as a dev-side tool.
@client.event
async def on_ready():
    for guild in client.guilds:
        print(f'{client.user} has connected to {guild.name}!')

# Function to tell if string is an int because apparently python doesn't have that natively.
def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

# Function to give a multifactorial.
def multifactorial(num, amount):
    ret = 1
    while num > 0:
        ret *= num
        num -= amount
    return ret

# Helper function for detecting a message where a lesson can be learned.
def magic(word):
    i = len(word) - 1
    while i >= 0 and word[i] == '!':
        i -= 1
    i += 1
    if i == 0:
        return ''

    if word.find('!') == i:
        bef = word[:i]
        ret = f'{word} = '
        if is_int(bef) and int(bef) <= 805:
            val = multifactorial(int(bef), len(word) - i)
            ret += str(val)
        else:
            ret += f'{bef}*({bef} - {len(word) - i}){word[i:]}'
        return ret
    else:
        return ''

# Fires whenever there's a message received.
@client.event
async def on_message(message):
    if '!' in message.content and message.author != client.user:
        words = message.content.split(' ')
        words[:] = [word for word in words if word != '' and word != '!']
        for word in words:
            s = magic(word)
            if s != '':
                await message.channel.send(s)

client.run(TOKEN) # Runs bot
