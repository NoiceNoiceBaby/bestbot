########################################################################################################################
# INCLUDES
########################################################################################################################
import os
import sys
from datetime import date  # for blacklist
import string              # for blacklist
from os import path        # for find
import json                # for conv & game database
import random              # for helix
from random import randint # for roll
import urllib              # for find
from requests import get   # for ip
import discord
from discord.ext import commands

########################################################################################################################
# SETUP
########################################################################################################################
client = commands.Bot(command_prefix = '/')
client.echoLog = {}

GH_LINK     = 'https://github.com/gentutu/bestbot'
ERROR_REPLY = 'Incorrect command usage; see `/help [command]`'

colours = {
    'red'   : 0xAA2222,
    'green' : 0x22AA22,
    'blue'  : 0x224466
}

searchEngines = {
    'google' : 'https://www.google.com/search?q=',
    'yt'     : 'https://www.youtube.com/results?search_query=',
    'ddg'    : 'https://duckduckgo.com/?q=',
    'bing'   : 'https://www.bing.com/search?q=',
    'sp'     : 'https://startpage.com/do/search?q=',
    'wiki'   : 'https://en.wikipedia.org/wiki/Search?search=',
    'reddit' : 'https://www.reddit.com/search/?q=',
    'gh'     : 'https://github.com/search?q=',
    'aw'     : 'https://wiki.archlinux.org/index.php?search=',
    'gw'     : 'https://wiki.gentoo.org/index.php?search=',
    'pcgw'   : 'https://www.pcgamingwiki.com/w/index.php?search=',
    'wdb'    : 'https://www.winehq.org/search?q=',
    'pdb'    : 'https://www.protondb.com/search?q=',
    'ud'     : 'https://www.urbandictionary.com/define.php?term=',
    'mcw'    : 'https://minecraft.gamepedia.com/Special:Search?search=',
    'cheat'  : 'https://cheat.sh/'
}

files = {
    'f_blacklist'    : 'res/blacklist',
    'f_botToken'     : 'res/botToken',
    'f_channelAdmin' : 'res/channelAdmin',
    'f_channelEcho'  : 'res/channelEcho',
    'f_cosmeticRoles': 'res/cosmeticRoles',
    'f_emoteHelix'   : 'res/emoteHelix',
    'f_currencyKey'  : 'res/currencyKey',
    'f_catKey'       : 'res/catKey',
    'f_helixReplies' : 'res/helixReplies',
    'f_gameKeys'     : 'res/gameKeys.json'
}

if os.path.exists(files["f_blacklist"]):
    with open(files["f_blacklist"], 'r') as blacklistFile:
        global BLACKLIST
        BLACKLIST = blacklistFile.read().split()
        BLACKLIST = [element for element in BLACKLIST if element]
else:
    print(f'Error: {files["f_blacklist"]} file missing')
    sys.exit()

if os.path.exists(files["f_botToken"]):
    with open(files["f_botToken"], 'r') as botTokenFile:
        global BOT_TOKEN
        BOT_TOKEN = botTokenFile.read().strip('\n')
else:
    print(f'Error: {files["f_botToken"]} file missing')
    sys.exit()

if os.path.exists(files["f_channelAdmin"]):
    with open(files["f_channelAdmin"], 'r') as channelAdminFile:
        global CHANNEL_ADMIN
        CHANNEL_ADMIN = channelAdminFile.read().strip('\n')
else:
    print(f'Error: {files["f_channelAdmin"]} file missing')
    sys.exit()

if os.path.exists(files["f_channelEcho"]):
    with open(files["f_channelEcho"], 'r') as channelEchoFile:
        global CHANNEL_ECHO
        CHANNEL_ECHO = channelEchoFile.read().strip('\n')
else:
    print(f'Error: {files["f_channelEcho"]} file missing')
    sys.exit()

if os.path.exists(files["f_cosmeticRoles"]):
    with open(files["f_cosmeticRoles"], 'r') as cosmeticRolesFile:
        global COSMETIC_ROLES
        COSMETIC_ROLES = cosmeticRolesFile.read().split('\n')
        COSMETIC_ROLES = [element for element in COSMETIC_ROLES if element]
else:
    print(f'Error: {files["f_cosmeticRoles"]} file missing')
    sys.exit()

if os.path.exists(files["f_emoteHelix"]):
    with open(files["f_emoteHelix"], 'r') as emoteHelixFile:
        global EMOTE_HELIX
        EMOTE_HELIX = emoteHelixFile.read().strip('\n')
else:
    print(f'Error: {files["f_emoteHelix"]} file missing')
    sys.exit()

if os.path.exists(files["f_currencyKey"]):
    import currency
    with open(files["f_currencyKey"], 'r') as currencyKeyFile:
        global CURRENCY_KEY
        CURRENCY_KEY = currencyKeyFile.read().strip('\n') # https://www.currencyconverterapi.com/
else:
    CURRENCY_KEY = None

if os.path.exists(files["f_catKey"]):
    import cat
    with open(files["f_catKey"], 'r') as catKeyFile:
        global CAT_KEY
        CAT_KEY = catKeyFile.read().strip('\n') # https://thecatapi.com/ or https://thedogapi.com/
else:
    CAT_KEY = None

if os.path.exists(files["f_helixReplies"]):
    with open(files["f_helixReplies"], 'r') as helixRepliesFile:
        global HELIX_REPLIES
        HELIX_REPLIES = open(files["f_helixReplies"], 'r').read().split('\n')
        HELIX_REPLIES = [element for element in HELIX_REPLIES if element]
else:
    print(f'Error: {files["f_helixReplies"]} file missing')
    sys.exit()

if os.path.exists(files["f_gameKeys"]):
    pass
else:
    print(f'Error: {files["f_gameKeys"]} file missing')
    sys.exit()

@client.event
async def on_ready():
    print('Bestbot online.')
    await client.change_presence(status = discord.Status.online)

########################################################################################################################
# LOCAL API
########################################################################################################################
async def echoMessage(reason, message, colour):
    echoChannel = client.get_channel(int(CHANNEL_ECHO))

    if message.author.id == client.user.id:
        return

    if message.attachments:
        image = message.attachments[0]
        client.echoLog[message.guild.id] = (image.proxy_url, message.content, message.author, message.channel.name, message.created_at)
    else:
        client.echoLog[message.guild.id] = (message.content,message.author, message.channel.name, message.created_at)

    try:
        image_proxy_url, contents,author, channel_name, time = client.echoLog[message.guild.id]
    except:
        contents,author, channel_name, time = client.echoLog[message.guild.id]

    try:
        embed = discord.Embed(description = contents , color = colour, timestamp = time)
        embed.set_image(url = image_proxy_url)
        embed.set_author(name = f"{author.name}#{author.discriminator}", icon_url = author.avatar_url)
        embed.set_footer(text = f"{reason} in #{channel_name}")
        await echoChannel.send(embed = embed)
    except:
        embed = discord.Embed(description = contents , color = colour, timestamp = time)
        embed.set_author(name = f"{author.name}#{author.discriminator}", icon_url = author.avatar_url)
        embed.set_footer(text = f"{reason} in #{channel_name}")
        await echoChannel.send(embed = embed)

    async for entry in message.guild.audit_logs(action = discord.AuditLogAction.message_delete):
        action = discord.AuditLogAction.message_delete

########################################################################################################################
# MODERATION
########################################################################################################################
@client.command(brief       = 'Shows the host\'s WAN IP', ########################################################### ip
                description = '[admin] Shows the host\'s WAN IP.')
async def ip(context, noarg = None):
    if not context.author.guild_permissions.administrator: # check for user permissions
        await context.send(f'{context.author.mention} Permission denied.')
        return

    if noarg is not None: # check for no arguments
        await context.send(f'{context.author.mention} {ERROR_REPLY}.')
        return

    if int(CHANNEL_ADMIN) == context.channel.id:
        host_wan_ip = get('https://api.ipify.org').text
        embed = discord.Embed(title = "Host WAN IP", description = f'||`{host_wan_ip}`||', color = colours["red"])
        await context.send(embed = embed)
    else:
        await context.send(f'{context.author.mention} Command not available on current channel.')


@client.command(brief       = 'Deletes a specified amount of messages', ########################################## clear
                description = '[admin/mod] Deletes a specified amount of messages. Call with \'confirm\' argument.')
async def clear(context, amount = None, confirm = None, noarg = None):
    if not context.author.guild_permissions.manage_messages: # check for user permissions
        await context.send(f'{context.author.mention} Permission denied.')
        return

    try: # check for correct argument type
        if noarg is None and confirm == 'confirm': # check for no third argument
            amount = int(amount)
            if amount < 1:
                raise Exception()
            elif amount == 1:
                await context.channel.purge(limit = amount + 1)
                await context.send(f'{context.author.mention} cleared the last message.')
            else:
                await context.channel.purge(limit = amount + 1)
                await context.send(f'{context.author.mention} cleared the last {amount} messages.')
        else:
            raise Exception()
    except Exception:
        await context.send(f'{context.author.mention} {ERROR_REPLY}.')

@client.command(brief       = 'Sets the channel\'s slow mode', #################################################### slow
                description = '[admin/mod] Sets the channel\'s slow mode. Use `off` or a valid duration (e.g. `1m`).')
async def slow(context, amount = None, *, reason = None):
    if not context.author.guild_permissions.manage_messages: # check for user permissions
        await context.send(f'{context.author.mention} Permission denied.')
        return

    duration = {
        'off': 0,
        '5s' : 5,
        '10s': 10,
        '15s': 15,
        '30s': 30,
        '1m' : 60,
        '2m' : 120,
        '5m' : 300,
        '10m': 600,
        '15m': 900,
        '30m': 1800,
        '1h' : 3600,
        '2h' : 7200,
        '6h' : 21600
    }

    if amount in duration:
        await context.channel.edit(reason = '/slow command', slowmode_delay = int(duration[amount]))
        if amount == 'off':
            await context.send(f'{context.author.mention} disabled slow mode.')
        else:
            if reason is None:
                await context.send(f'{context.author.mention} enabled {amount} slow mode.')
            else:
                await context.send(f'{context.author.mention} enabled {amount} slow mode with reason `{reason}`.')
    else:
        await context.send(f'{context.author.mention} {ERROR_REPLY}.')

########################################################################################################################
# UTILITIES
########################################################################################################################
@client.command(brief       = 'Links towards the bot\'s source code', ########################################### source
                description = 'Links towards the bot\'s source code.',
                aliases     = ['saucecode', 'sauce'])
async def source(context, noarg = None):
    if noarg is None: # check for no arguments
        embed = discord.Embed(title = "Best Source", description = f"<{GH_LINK}>", color = colours["red"])
        await context.send(embed = embed)
    else:
        await context.send(f'{context.author.mention} {ERROR_REPLY}.')

@client.command(brief       = 'Checks bot status and network quality', ############################################ ping
                description = 'Check  bot status and network quality.',
                aliases     = ['pong'])
async def ping(context, noarg = None):
    if noarg is None: # check for no arguments
        if context.invoked_with == 'pong':
            await context.send(':dagger:')
        else:
            await context.send(f'pong! `{round(client.latency * 1000)}ms`')
    else:
        await context.send(f'{context.author.mention} {ERROR_REPLY}.')

@client.command(brief       = 'Rolls for a random number up to a maximum', ######################################## roll
                description = 'Rolls for a random number up to a maximum.')
async def roll(context, maximum = None, *, terms = None):
    try: # check for correct argument type
        maximum = int(maximum)
        if maximum > 1:
            if terms is None:
                await context.send(f'{context.author.mention} rolled {randint(1, maximum)}.')
            else:
                await context.send(f'{context.author.mention} rolled {randint(1, maximum)} for *{terms}*.')
        else:
            raise Exception()
    except Exception:
        await context.send(f'{context.author.mention} {ERROR_REPLY}.')

@client.command(brief       = 'Tosses a coin', #################################################################### coin
                description = 'Tosses a coin. Accepts terms freely.',
                aliases     = ['toss', 'flip'])
async def coin(context, *, terms = None):
    sides = ['heads', 'tails']

    if terms is None:
        await context.send(f'{context.author.mention} tossed **{random.choice(sides)}**.')
    else:
        await context.send(f'{context.author.mention} tossed **{random.choice(sides)}** for *{terms}*.')

@client.command(brief       = 'Consult the Helix Fossil', ######################################################## helix
                description = 'Consult the Helix Fossil. It shall answer.')
async def helix(context, *, question = None):
    if question is not None: # check for at least 1 argument
        await context.send(f'{context.author.mention} Helix Fossil says: {EMOTE_HELIX} *{random.choice(HELIX_REPLIES)}* {EMOTE_HELIX}')
    else:
        await context.send(f'{context.author.mention} Consult the Fossil. {EMOTE_HELIX}')

@client.command(brief       = 'Performs a web search', ############################################################ find
                description = 'Search a lot of places. Too many to list here. See the source code.')
async def find(context, engine = None, *, query = None):
    engine = engine.lower()
    if engine == 'ph':
        if path.exists('res/no.jpg'):
            picture = discord.File('res/no.jpg')
            await context.send(file=picture)
        else:
            await context.send(f'{context.author.mention} No.')
        return

    if engine not in searchEngines: # check if the requested engine exists
        await context.send(f'{context.author.mention} Unknown search engine.')
        return

    if query is not None: # check for at least 1 search term
        search_input = searchEngines[engine] + urllib.parse.quote(query)
        await context.send(f'{context.author.mention} Your search results: <{search_input}>')
    else:
        await context.send(f'{context.author.mention} What should I search for?')

@client.command(brief       = 'Toggles a role', ################################################################### role
                description = 'Toggles a role. List all options with the `list` argument.')
async def role(context, role_arg = None, noarg = None):
    member = context.author
    if noarg is not None:
        await context.send(f'{context.author.mention} {ERROR_REPLY}.')
        return

    if role_arg == 'list':
        await context.send(f'{context.author.mention} Available roles: `{"`, `".join(COSMETIC_ROLES)}`.')
        return

    if role_arg in COSMETIC_ROLES:
        role_arg = discord.utils.get(member.guild.roles, name = role_arg)
        if role_arg in member.roles:
            await discord.Member.remove_roles(member, role_arg)
            await context.send(f'{context.author.mention} Removed `{role_arg}` role.')
        else:
            await discord.Member.add_roles(member, role_arg)
            await context.send(f'{context.author.mention} Added `{role_arg}` role.')
    elif role_arg is None:
        await context.send(f'{context.author.mention} {ERROR_REPLY}.')
    else:
        await context.send(f'{context.author.mention} Unsupported role.')

@client.command(brief       = 'Converts currency', ################################################################ conv
                description = 'Converts currency. Use the 3-letter currency codes.')
async def conv(context, amount = None, source_curr = None, target_curr = None, noarg = None):
    try: # check for int amount
        amount = float(amount)
        if noarg       is not None or \
           source_curr is     None or \
           target_curr is     None or \
           amount      is     None:
            raise Exception()
    except Exception:
        await context.send(f'{context.author.mention} {ERROR_REPLY}.')
        return

    source_curr = source_curr.upper()
    target_curr = target_curr.upper()

    if not 'currencies.json' in os.listdir('./res'): # retrieve currency data if we don't have it stored.
        await currency.retrieve_currencies(CURRENCY_KEY)

    with open('./res/currencies.json', 'r') as stored_curr: # load list of currencies
        available_curr = json.load(stored_curr)

    if source_curr not in available_curr or \
      target_curr not in available_curr:
        await context.send(f'{context.author.mention} Unknown currency code.')
        return

    if source_curr == target_curr:
        await context.send(f'{context.author.mention} Nothing to convert.')
        return

    exchanged = await currency.currency_convert(CURRENCY_KEY, amount, source_curr, target_curr)
    await context.send(f'{context.author.mention} {amount:.2f} `{source_curr}` ≈ `{target_curr}` {exchanged:.2f}')

@client.command(brief       = 'Sends a random animal picture', ##################################################### pls
                description = 'Sends a random animal picture. Use `cat` or `dog` when requesting.')
async def pls(context, animal = None, noarg = None):
    try:
        if noarg is not None:
            raise Exception()
    except Exception:
        await context.send(f'{context.author.mention} {ERROR_REPLY}.')
        return

    supported_animals = ['cat', 'dog']

    if(animal in supported_animals):
        URL = await cat.get(animal, CAT_KEY, random.choice(['jpg', 'gif']))
        await context.send(f'{URL}')
    else:
        await context.send(f'{context.author.mention} {ERROR_REPLY}.')

@client.command(brief       = 'Allows a user to input a game with its activation code', ######################## addgame
                description = 'Allows a user to input a game with its activation code. arg1 = gameName, arg2 = code.')
async def addgame(context, gameName = None, gameCode = None, noarg = None):
    try:
        if noarg is not None or\
            gameName is None or\
            gameCode is None:
                raise Exception()
    except Exception:
        await context.send(f'{context.author.mention} {ERROR_REPLY}.')
        return
    
    with open(files["f_gameKeys"], "r") as gameKeyFile:
        games = json.load(gameKeyFile)

    games[str(gameName)] = str(gameCode)

    with open(files["f_gameKeys"], "w") as gameKeyFile:
        games = json.dump(games, gameKeyFile)

    await context.send(f"{context.author.mention} game added!")
    await context.channel.purge(limit=2)

@client.command(brief       = 'Allows a user to claim a game', ################################################ claimgame
                description = 'Allows a user to claim a game. The activation code is dm\'d to the user')  
async def claimgame(context, gameName = None, noarg = None):
    try:
        if noarg is not None:
            raise Exception()
    except Exception:
        await context.send(f'{context.author.mention} {ERROR_REPLY}.')
        return

    with open(files["f_gameKeys"], "r") as gameKeyFile:
        games = json.load(gameKeyFile)

    if str(gameName) in games:
        await context.send(f'{context.author.mention} `{gameName}` found! dm\'ing your game code now!')
        await context.author.send(f'key: {games[gameName]}')
        
        with open(files["f_gameKeys"], "r+") as gameKeyFile:
            games = json.load(gameKeyFile)
            games.pop(gameName)
            global TEMP_GAMES
            TEMP_GAMES = games

        with open(files["f_gameKeys"], "w+") as gameKeyFile:
            pass

        with open(files["f_gameKeys"], "r+") as gameKeyFile:
            TEMP_GAMES = json.dump(TEMP_GAMES, gameKeyFile)

    else:
        await context.send(f'{context.author.mention} `{gameName}` not found!')

@client.command(brief       = 'Lists the games a user can claim', ################################################ listgame
                description = 'Lists the games a user can claim.')
async def listgames(context):
    with open(files["f_gameKeys"], "r") as gameKeyFile:
        games = json.load(gameKeyFile)

        gameEmbed = discord.Embed(title="available games:")
        
        for game in games:
            gameEmbed.add_field(name=f"{game}", value=f'type `/claimgame {game}` to claim!')

        await context.send(embed=gameEmbed)

########################################################################################################################
# EVENTS
########################################################################################################################
@client.event ################################################################################################ blacklist
async def on_message(message):
    allowed = True
    current_message = message.content.lower()
    current_message = current_message.replace(" ", "")
    current_message = current_message.translate(str.maketrans('', '', string.punctuation))

    if date.today().weekday() != 2 and ":wednesday:" in current_message:
        await message.delete()
        allowed = False
    else:
        for word in BLACKLIST:
            if word in current_message:
                await message.delete()
                allowed = False

    if allowed:
        await client.process_commands(message)

@client.event ################################################################################################ blacklist
async def on_message_edit(before, after):
    if before.content == after.content:
        return

    await echoMessage('Edited from', before, colours["green"])
    await echoMessage('Edited to'  , after,  colours["blue"])

    for word in BLACKLIST:
        current_message = after.content.lower()
        if word in current_message.replace(" ", ""):
            await after.delete()

@client.event ############################################################################################# deleted echo
async def on_message_delete(message):
    await echoMessage('Deleted', message, colours["red"])

# dis: disabled for now
#@client.event ######################################################################################### unknown command
#async def on_command_error(context, error):
#    if isinstance(error, commands.CommandNotFound):
#        context.content = "/cat"
#        await client.process_commands(context)

########################################################################################################################
# RUN
########################################################################################################################
client.run(BOT_TOKEN)

########################################################################################################################
# END OF FILE
########################################################################################################################
