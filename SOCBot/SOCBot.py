#SOCBot.py
"""
@author: Nikhil Devanathan
This script handles the functionality of SOCBot, a discord bot that monitors and reports the state 
of the Stanford-OpenCode (SOC) project in a discord server or dms. This bot is also part of the SOC 
project. Talk about code-ception.
"""
#Default packages
import os
from time import sleep

#Installed packages
import discord
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#SOCBot help text
HELP_TEXT ="""Hi, I'm SOCBot, the discord interface for Stanford-OpenCode (SOC)!
Use `?soc [command]` commands to talk to me.
Commands:
`help`, `h` - brings up this text
`contributors`, `c` - list current SOC contributors
`readme`, `r` - bring up the current SOC README
`forks`, `f` - list the number of forks, and the people who have forked
`latest`, `l` - shows the latest commit to the main SOC repository
`issues`, `i` - displays the number of open issues
`list`, `ls` - lists the files and folders in the current directory (by default the directory of the main SOC repo)
`change`, `cd` - changes the current directory being viewed
`view`, `v` - reads a file into discord
Remember, I won't respond to commands that don't *start with* `?soc`"""

REPO_NAME = "Stanford-OpenCode"
URL = "https://github.com/PrathamSoni/Stanford-OpenCode"
url_tail = ""

#The bot secrets are stored in a local .env file for security. No peeking :)
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

#Handles sending a message with a brief guide on bot usage
async def handle_help(message):
    await message.channel.send(HELP_TEXT)

#Outputs the number and list of current SOC contributors
async def handle_contributors(message):
    #the first found element is a blank template
    contributors = fetch_html(URL + '/graphs/contributors').find_all('h3', class_="border-bottom p-2 lh-condensed")[1:]
    reply = "There are currently %d %s contributors:" % (len(contributors), REPO_NAME)
    for contributor in contributors:
        name = list(contributor.children)[5]
        reply += '\n' + name.get_text()
    await message.channel.send(reply)

#Replies with the contents of the repository README, formatted simply
async def handle_readme(message):
    readme = fetch_html(URL).find('article', class_="markdown-body entry-content container-lg")
    reply = "README: \n"
    for element in list(readme.children):
        if (element.name == 'h1'):
            reply += '**%s**\n' % element.get_text()
        elif (element.name == 'h2'):
            reply += '\n**%s**\n' % element.get_text()
        elif (element.name == 'p'):
            reply += '%s\n' % element.get_text()
    await message.channel.send(reply)

#Outputs the number of forks of the repository and the users who have forks of this repository
async def handle_forks(message):
    html = fetch_html(URL+"/network/members")
    count = html.find_all('a', class_="social-count")[2]
    forkers = html.find_all('a', class_=False, attrs={'data-hovercard-type':'user'})
    reply = "%s users have forked this repository:\n Main - " % digitize(count.get_text())
    for forker in forkers:
        reply += forker.get_text() + '\n'
    await message.channel.send(reply)

#Unimplemented
async def handle_latest_commit(message):
    i = 0

#Replies with the number of open and closed issues, and gives the time openned of the latest open issue
async def handle_issues(message):
    html = fetch_html(URL+"/issues")
    open_label = html.find('a', class_="btn-link selected", attrs={'data-ga-click':'Issues, Table state, Open'})
    closed_label = html.find('a', class_="btn-link", attrs={'data-ga-click':'Issues, Table state, Closed'})
    reply = "There are %s open issues and %s closed issues. \n" % (digitize(open_label.get_text()), digitize(closed_label.get_text()))
    if int(digitize(open_label.get_text())) > 0:
        latest = html.find('relative-time', class_="no-wrap")
        reply += "The latest issue was opened %s." % latest.get_text()
    await message.channel.send(reply)

#Unimplemented
async def handle_list(message):
    i = 0

#Unimplemented
async def handle_change_directory(message):
    i = 0

#Unimplemented
async def handle_view(message):
    i = 0

#Dictionary matching keywords with functions
FCTS_DICT = {'help':handle_help,
'contributors':handle_contributors,
'readme':handle_readme,
'forks':handle_forks,
'latest':handle_latest_commit,
'issues':handle_issues,
'list':handle_list,
'change':handle_change_directory,
'view':handle_view,
'h':handle_help,
'c':handle_contributors,
'r':handle_readme,
'f':handle_forks,
'l':handle_latest_commit,
'i':handle_issues,
'ls':handle_list,
'cd':handle_change_directory,
'v':handle_view,
}

#Initializes the headless selenium chrome webdriver
def init_webdriver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    global driver
    driver = webdriver.Chrome(options=options)

#Returns the parsed html of a given website
def fetch_html(url):
    driver.get(url)
    sleep(3.1) #load time
    return BeautifulSoup(driver.page_source, 'html.parser')

#Returns a string of the numeric charcters in a given string
def digitize(text):
    digitized = ''
    for char in text:
        if char in '1234567890':
            digitized += char
    return digitized

#Fires when the bot connects to a serevr it has joined. Exists as a dev-side tool.
@client.event
async def on_ready():
    init_webdriver()
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

client.run(TOKEN) #Runs bot