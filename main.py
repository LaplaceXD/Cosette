import discord
from discord.ext import commands
import os

import music
import fun

cogs = [music, fun]
client = commands.Bot(command_prefix="!", intents = discord.Intents.all())

for cog in cogs:
  cog.setup(client)

TOKEN = os.environ['TOKEN']
client.run(TOKEN)