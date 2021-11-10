from discord.ext import commands
from discord import Embed
from app.utils.misc import extract_json
from random import randint
import urllib
import asyncio
import json
import re

msg = extract_json("msg_templates")
names = {
    "266518596283269131": "HANSHIN!"
}

class FunBot(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def morningbot(self, ctx):
        content = urllib.request.urlopen("https://api.quotable.io/random")
        quote = json.load(content)
        quote_content = quote["content"]
        author = quote["author"]
        await ctx.send(f"[__{author}__] **{quote_content}**")

    async def reminder(self, ctx, to, duration, msg):
        dur = int(duration)
        mention_sender = "you" if "me" in to else to
        note = f"I will remind {mention_sender} to **{msg}** in __{dur} seconds__"

        print(re.findall("(\\d)([minutes|seconds|hours])+", duration))

        await ctx.send(note)
        await asyncio.sleep(dur)
        mention_author = f"<@!{ctx.message.author.id}>" if "me" in to else to
        await ctx.send(f"{mention_author}, remember to **{msg}**")

    @commands.command()
    async def remind(self, ctx, to, duration, *, msg):
        await self.reminder(ctx, to, duration, msg)

    @commands.command()
    async def mute(self, ctx, userId):
        guild = ctx.message.guild
        member = guild.get_member(int(userId[3:-1]))
        await member.edit(mute=True, deafen=True)
    
    @commands.command()
    async def unmute(self, ctx, userId):
        guild = ctx.message.guild
        member = guild.get_member(int(userId[3:-1]))
        await member.edit(mute=False, deafen=False)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        
        if "rob <@!336038143063228436>" in message.content:
            await message.send("Why do you call for master <@!336038143063228436>.")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(msg["quotes"][randint(0, 7)])

    @commands.command()
    async def say(self, ctx, *, msg=None):
        print(msg)
        if msg is None:
            await ctx.send("Please teach me how to talk, daddy.")
        else:
            await ctx.message.delete()
            await ctx.send(msg)

    @commands.command(aliases=["f", "F"])
    async def pay_respects(self, ctx):
        await ctx.send("**F**")

    @commands.command()
    async def gudnytbot(self, ctx):
        id = str(ctx.message.author.id)
        if id == "336038143063228436":
            await ctx.send("Praise thy Buot!")
        elif id in names:
            name = names[id]
            await ctx.send(f"FUCK YOU, {name.upper()}!")
        else:
            await ctx.send(f"FUCK YOU {ctx.message.author.nick.upper()}!")
    
    @commands.command(
        name="superidol"
    )
    async def _super_idol(self, ctx):
        embed = Embed(title="Super Idol!").set_image(url="https://cdn.discordapp.com/attachments/797083893014462477/902574709957349436/unknown.png")

        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(FunBot(client))