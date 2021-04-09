import discord
from discord.ext import commands
import logging
import sys

bot = commands.Bot(command_prefix='|')
logging.basicConfig(level=logging.INFO)

#Removed searchcog and musiccog becuase dependencies issues
modules = ["cogs.admincog", "cogs.topiccog", "cogs.categorycog", "cogs.debatecog", "cogs.misccog", "cogs.complaintscog", "cogs.memecog", "cogs.currencycog", "cogs.inventorycog", "cogs.nominationcog", "cogs.searchcog"] #, "cogs.helpcog", "cogs.musiccog"]

for ext in modules:
    bot.load_extension(ext)

f = open(sys.argv[1], "r")
for line in f:
    if line[0] == "#":
        continue
    elif "TOKEN" in line:
        TOKEN = line.split("=")[-1].strip()

@bot.event
async def on_ready():
    logging.info(f'Logged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    sys.stdout.write(f'Logged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    sys.stdout.flush()
    await bot.change_presence()

bot.run(TOKEN, bot=True, reconnect=True)

