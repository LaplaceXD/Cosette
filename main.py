import discord
import os
from discord.ext import commands

from app.keep_alive import keep_alive
from app.music import musicbot
from app.fun import funbot

cogs = [musicbot, funbot]
client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

for cog in cogs:
    cog.setup(client)

keep_alive()
TOKEN = os.environ['TOKEN']
client.run(TOKEN)
