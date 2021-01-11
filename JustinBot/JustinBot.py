#JustinBot.py
"""
@author: Nikhil Devanathan
This script handles the functionality of JustinBot, a discord bot that dispenses imprompteau math lessons.
"""
#Default packages
import os

#Installed packages
import discord
from dotenv import load_dotenv

#The bot secrets are stored in a local .env file for security
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

#Fires when the bot connects to a serevr it has joined. Exists as a dev-side tool.
@client.event
async def on_ready():
    for guild in client.guilds:
        print(f'{client.user} has connected to {guild.name}!')

#The bot always listens for messages, but it only responds when a message begins with ?soc
@client.event
async def on_message(message):
    if '!' in message.content and message.author != client.user:
        words = message.content.split(' ')
        words[:] = [word for word in words if word != '' and word != '!']
        for word in words:
            if word[-1] == '!':
                await message.channel.send('%s = %s * (%s - 1)!' % (word, word[:-1], word[:-1]))

client.run(TOKEN) #Runs bot