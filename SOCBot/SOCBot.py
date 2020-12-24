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
Use `?soc [command]` commands to talk to me. All commands are *case sensitive*.
Commands:
`help`, `h` - brings up this text
`contributors`, `c` - list current SOC contributors
`readme`, `r` - bring up the current SOC README
`forks`, `f` - list the number of forks, and the people who have forked
`latest`, `l` - shows the latest commit to the main SOC repository
`issues`, `i` - displays the number of open issues
`list [path]`, `ls [path]` - lists the files and folders at the path within the repository. \
A blank path or '/' for path will correspond to main directory of the repository. Folders are \
listed in bolded font. If the path is invalid, my response will say so. Use '/' not '\\' in the path.
`view [path]`, `v [path]` - reads a file into discord. Reuqires the path to the file within the repo.
"""

#These can be chanegd to adapt the code to any github repo
REPO_NAME = "Stanford-OpenCode"
URL = "https://github.com/PrathamSoni/Stanford-OpenCode"
BRANCH = 'main'

#Dict linking extensions to supported formats for discord code blocks
SUPPORTED_FORMATS = {
'.sh':'bash',
'.coffee':'coffeescript',
'.c':'cpp',
'.cpp':'cpp',
'.cxx':'cpp',
'.cc':'cpp',
'.C':'cpp',
'.c++':'cpp',
'.h':'cpp',
'.hh':'cpp',
'.H':'cpp',
'.hpp':'cpp',
'.hxx':'cpp',
'.h++':'cpp',
'.cs':'cs',
'.csx':'cs',
'.css':'css',
'.ini':'ini',
'.json':'json',
'.md':'md',
'.ml':'ml',
'.pl':'prolog',
'.py':'py',
'.tex':'tex',
'.xl':'xl',
'.xml':'xml',
}

#The bot secrets are stored in a local .env file for security
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
        reply += '\n' + clean(name.get_text())
    await message.channel.send(reply)

#Replies with the contents of the repository README, formatted simply
async def handle_readme(message):
    readme = fetch_html(URL).find('article', class_="markdown-body entry-content container-lg")
    reply = "README: \n"
    for element in list(readme.children):
        if (element.name == 'h1'):
            reply += '**%s**\n' % clean(element.get_text())
        elif (element.name == 'h2'):
            reply += '\n**%s**\n' % clean(element.get_text())
        elif (element.name == 'p'):
            reply += '%s\n' % clean(element.get_text())
    await message.channel.send(reply)

#Outputs the number of forks of the repository and the users who have forks of this repository
async def handle_forks(message):
    html = fetch_html(URL+"/network/members")
    count = html.find_all('a', class_="social-count")[2]
    forks = html.find_all('div', class_='repo')
    reply = "%s users have forked this repository:\nMain - " % digitize(count.get_text())
    for fork in forks:
        forkers = fork.find_all('a', attrs={'data-hovercard-type':'user'})
        for forker in forkers:
            if forker.get_text() != '':
                reply += clean(forker.get_text()) + '\n'
    await message.channel.send(reply)

#Displays the number of commits on the repository and shares the latest commit
async def handle_latest_commit(message):
    html = fetch_html(URL)
    count = list(html.find('a', class_="pl-3 pr-3 py-3 p-md-0 mt-n3 mb-n3 mr-n3 m-md-0 link-gray-dark no-underline no-wrap").children)[3]
    commit = list(html.find('div', class_="css-truncate css-truncate-overflow text-gray").children)[3]
    reply = "There have been %s commits to %s so far.\n The latest commit is:\n" % (digitize(count.get_text()), REPO_NAME)
    reply += commit.get_text().replace('\n','') + '\n'
    author = html.find('a', class_="commit-author user-mention")
    date = html.find('relative-time', class_="no-wrap")
    reply += "by %s, %s." % (author.get_text(), date.get_text())
    await message.channel.send(clean(reply))
    

#Replies with the number of open and closed issues, and gives the time openned of the latest open issue
async def handle_issues(message):
    html = fetch_html(URL+"/issues")
    open_label = html.find('a', class_="btn-link selected", attrs={'data-ga-click':'Issues, Table state, Open'})
    closed_label = html.find('a', class_="btn-link", attrs={'data-ga-click':'Issues, Table state, Closed'})
    reply = "There are %s open issues and %s closed issues. \n" % (digitize(open_label.get_text()), digitize(closed_label.get_text()))
    if int(digitize(open_label.get_text())) > 0:
        latest = html.find('relative-time', class_="no-wrap")
        reply += "The latest issue was opened %s." % clean(latest.get_text())
    await message.channel.send(reply)

#Lists files and folders in a given valid subdirectory of the repository
async def handle_list(message):
    tail = ''
    valid = True
    reply = ''
    args = message.content.split(' ')
    args[:] = [arg for arg in args if arg != '']
    if (len(args) > 2 and args[2] != '/'):
        tail = '/tree/%s/%s/' % (BRANCH, args[2].strip('/'))
    html = fetch_html(URL+tail)
    rows = html.find_all('div', attrs={'role':'row'})
    rows[:] = [row for row in rows if 'Box-row' in row['class']]
    if rows:
        reply = clean('Directory: /%s/%s\n' % (REPO_NAME, tail.replace('/tree/'+BRANCH+'/', '')))
        for row in rows:
            header = row.find('div', attrs={'role':'rowheader'})
            icon = row.find('svg', attrs={'role':"img"})
            if len(reply) > 1700:
                await message.channel.send(reply)
                reply = ''
            if icon and 'File' in icon['aria-label']:
                reply += clean(header.get_text().replace('\n','') + '\n')
            elif icon:
                reply += '**%s**\n' % clean(header.get_text().replace('\n',''))
    else:
        reply = 'Invalid directory'
    await message.channel.send(reply)

#Reads a file from the repository into discord
async def handle_view(message):
    reply = ''
    args = message.content.split(' ')
    args[:] = [arg for arg in args if arg != '']
    if (len(args) > 2):
        tail = '/blob/%s/%s' % (BRANCH, args[2].strip('/'))
        doctype = ''
        if tail[tail.rfind('.'):] in SUPPORTED_FORMATS:
            doctype = SUPPORTED_FORMATS[tail[tail.rfind('.'):]] + '\n'
        html = fetch_html(URL+tail)
        lines = html.find_all('td', class_='blob-code blob-code-inner js-file-line')
        if lines:
            reply = clean(tail[tail.rfind('/')+1:]) + ':\n```' + doctype
            for line in lines:
                if len(reply) > 1700:
                    reply += '```'
                    await message.channel.send(reply)
                    reply = '```' + doctype
                reply += line.get_text().replace('\n','').replace('`','\\`')+'\n'
            reply += '```'
        else:
            reply = 'Empty/invalid file or path'
    else:
        reply = 'Need filename or path argument'
    await message.channel.send(reply)

#Dictionary matching keywords with functions
FCTS_DICT = {'help':handle_help,
'contributors':handle_contributors,
'readme':handle_readme,
'forks':handle_forks,
'latest':handle_latest_commit,
'issues':handle_issues,
'list':handle_list,
'view':handle_view,
'h':handle_help,
'c':handle_contributors,
'r':handle_readme,
'f':handle_forks,
'l':handle_latest_commit,
'i':handle_issues,
'ls':handle_list,
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

#Puts an escape char before discord markdown symbols, this is to avoid unwanted discord formatting
def clean(text):
    cleaned = ''
    for char in text:
        if char in '`_*~>\\':
            cleaned += '\\' + char
        else:
            cleaned += char
    return cleaned

#Fires when the bot connects to a serevr it has joined. Exists as a dev-side tool.
@client.event
async def on_ready():
    init_webdriver()
    for guild in client.guilds:
        print(f'{client.user} has connected to {guild.name}!')

#The bot always listens for messages, but it only responds when a message begins with ?soc
@client.event
async def on_message(message):
    if ('?soc' == message.content[:4]):
        args = message.content.split(' ')
        args[:] = [arg for arg in args if arg != '']
        if args[1] in FCTS_DICT:
            await FCTS_DICT[args[1]](message)
        else:
            await message.channel.send('Unknown command: ' + args[1] + '. Try `?soc help` to see valid commands.')

client.run(TOKEN) #Runs bot