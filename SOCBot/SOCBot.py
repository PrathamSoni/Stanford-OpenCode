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

#SOCBot help text
HELP_TEXT ="""Hi, I'm SOCBot, the discord interface for Stanford-OpenCode (SOC)!
Use `?soc [command]` commands to talk to me.
Commands:
`help`, `h` - brings up this text
`contributors`, `c` - list current SOC contributors
`readme`, `whatis`, `w` - bring up the current SOC README
`forks`, `f` - list the number of forks, and the people who have forked
`latest`, `l` - shows the latest commit to the main SOC repository
`issues`, `i` - displays the number of open issues
`view`, `v` - lists the files and folders in the current directory (by default the directory of the main SOC repo)
`change`, `cd` - changes the current directory being viewed
'read', 'r' - reads a file into discord
Remember, I won't respond to commands that don't *start with* `?soc`"""

#The bot secrets are stored in a local .env file for security. No peeking :)
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

#Handles sending a message with a brief guide on bot usage
async def handle_help(message):
    await message.channel.send(HELP_TEXT)

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
async def handle_view(message):
    i = 0

#Unimplemented
async def handle_change_directory(message):
    i = 0

#Unimplemented
async def handle_read(message):
    i = 0

#Dictionary matching keywords with functions
FCTS_DICT = {'help':handle_help,
'contributors':handle_contributors,
'whatis':handle_readme,
'readme':handle_readme,
'forks':handle_forks,
'latest':handle_latest_commit,
'issues':handle_latest_issue,
'view':handle_view,
'change':handle_change_directory,
'read':handle_read,
'h':handle_help,
'c':handle_contributors,
'w':handle_readme,
'f':handle_forks,
'l':handle_latest_commit,
'i':handle_latest_issue,
'v':handle_view,
'cd':handle_change_directory,
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
            await message.channel.send('Unknown command: ' + args[1] + '. Try `?soc help` to see valid commands.')

#Gotta save the best bit for last.
client.run(TOKEN)