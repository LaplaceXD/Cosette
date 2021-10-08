from discord.ext import commands
from utils import extract_json
from random import randint

msg = extract_json("msg_templates")
names = {
    "266518596283269131": "HANSHIN!"
}

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return

        if "<@!336038143063228436>" in message.content:
            await message.channel.send("Why do you call for master <@!336038143063228436>.")

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

def setup(client):
    client.add_cog(Fun(client))