import discord, asyncio
from discord.ext import commands

# define client
client = commands.Bot(command_prefix = "!", help_command=None)

# utility for creating acronyms from strings
def acronym(str):
    return "".join(l[0] for l in str.split())

# utility for replacing a string according to a dictionary
def string_dict_replace(str, dict):
    str.split()
    new_str = []
    for char in str:
        if char in dict:
            char = dict[char]
        new_str.append(char)
    new_str = "".join(new_str)
    return new_str

def get_value_with_quotes(str):
    str = str.split('"')
    return str[1]

# open config file and split into list of lines
file = open("listenbot.conf","r").read()[:-1].replace(" ", "").split("\n")

# initialize dictionary for configuration settings
config = {}

for line in file:
    # remove comments and blank lines
    if line != "":
        if "#" not in line:
            # seperate command from value and put into dictionary
            line = line.split("=")
            config[line[0]] = line[1]

# assign values into dictionary
token = config['token']
mute_type = config["mute_type"]
format = config["format"]
channels = config["channels"].split(",")

# start the bot
@client.event
async def on_ready():
    print("Starting")

    # set bot presence to "Watching You"
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="You"))

@client.event
async def on_message(ctx):

    # create acronym
    guild_acronym = acronym(ctx.guild.name)

    # check for valid channel either removing blacklist or searching for whitelist
    whitelist = mute_type == "whitelist" and ctx.channel.name in channels
    blacklist = mute_type == "blacklist" and ctx.channel.name not in channels

    if whitelist or blacklist:
        # create dictionary for dictionary replace utility
        format_dict = {
        'u' : ctx.author.name,
        'c' : ctx.channel.name,
        'g' : ctx.guild.name,
        'a' : acronym(ctx.guild.name),
        '.' : ' '}
        text = string_dict_replace(format, format_dict)

        # add the content to the end of the format prompt
        text += ctx.clean_content

        # add attachments to the end of the content
        for attachment in ctx.attachments:
            text += str(attachment)

        # finally print the text for the host to see
        print(text)

client.run(token)
