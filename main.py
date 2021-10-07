import discord
import os

from discord.ext import commands
import music

cogs = [music]
client = commands.Bot(command_prefix="!", intents = discord.Intents.all())

for cog in cogs:
  cog.setup(client)

TOKEN = os.environ['TOKEN']
client.run(TOKEN)