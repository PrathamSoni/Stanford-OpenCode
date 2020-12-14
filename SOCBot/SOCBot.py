#MLSBot.py
"""
@author: Nikhil Devanathan
This script handles the functionality of SOCBot, a discord bot that monitors and reports the state 
of the Stanford-OpenCode (SOC) project in a discord server or dms. This bot is also part of the SOC 
project. Talk about code-ception.
"""
#Default packages
import os

#Installed packages
import discord
from dotenv import load_dotenv

#The bot secrets are stored in a local .env file for security. No peeking :)
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

#Unimplemented
async def handle_help(message):
    i = 0

#Unimplemented
async def handle_contributors(message):
    i = 0

#Unimplemented
async def handle_readme(message):
    i = 0

#Unimplemented
async def handle_forks(message):
    i = 0

#Unimplemented
async def handle_latest_commit(message):
    i = 0

#Unimplemented
async def handle_issues(message):
    i = 0

#Unimplemented
async def handle_dir(message):
    i = 0

#Unimplemented
async def handle_read(message):
    i = 0

#Unimplemented
async def handle_error(message):
    i = 0

#Dictionary matching keywords with functions
FCTS_DICT = {'help':handle_help,
'contributors':handle_contributors,
'whatis':handle_readme,
'readme':handle_readme,
'forks':handle_forks,
'latest':handle_latest_commit,
'issues':handle_latest_issue,
'dir':handle_dir,
'read':handle_read,
'h':handle_help,
'c':handle_contributors,
'w':handle_readme,
'f':handle_forks,
'l':handle_latest_commit,
'i':handle_latest_issue,
'd':handle_dir,
'r':handle_read,
}

#Fires when the bot connects to a serevr it has joined. Exists as a dev-side tool.
@client.event
async def on_ready():
    for guild in client.guilds:
        print(f'{client.user} has connected to {guild.name}!')

#The bot always listens for messages, but it only responds when a message begins with ?soc
@client.event
async def on_message(message):
    if ('?soc' == message.content[:4].lower()):
        args = message.content.lower().split(' ')
        args[:] = [arg for arg in args if arg != '']
        if FCTS_DICT[args[1]]:
            await FCTS_DICT[args[1]](message)
        else:
            await handle_error(message)

#Gotta save the best bit for last.
client.run(TOKEN)