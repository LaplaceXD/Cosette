import discord
from discord.ext import commands
from youtube import Youtube
from random import randint
from utils import extract_json, convert_to_equiv_digits
import youtube_dl

options = extract_json("options")
msg = extract_json("msg_templates")

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.yt = Youtube()
        self.paused = False
        self.queue = []
        
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(msg["quotes"][randint(0, 7)])

    @commands.command(aliases=["j"])
    async def join(self, ctx):  
        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel!")
        else:
            if ctx.voice_client is None:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.voice_client.move_to(ctx.author.voice.channel)

    @commands.command(aliases=["d", "dc"])
    async def disconnect(self, ctx):
        self.paused = False
        self.queue = []
        await ctx.voice_client.disconnect()

    @commands.command(aliases=["p", "play"])
    async def add(self, ctx, *, query=None):
        await self.join(ctx)
        if ctx.voice_client is None:
            return

        if query is None:
            if self.paused:
                await self.resume(ctx)
            else:
                await ctx.send("No track inputted!")
                return
        else:
            url = query if query.startswith("$https") else self.yt.search(query)
            music_data = self.extract_yt_data(url)
            queue_length = len(self.queue)
            self.queue.insert(queue_length, music_data)
            if queue_length > 0:
                await ctx.send(f"Queued Song#{queue_length}📜: {url}")
            else:
                await self.play_queue(ctx)
    
    async def extract_yt_data(self, url):
        with youtube_dl.YoutubeDL(options["ydl"]) as ydl:
            res = ydl.extract_info(url, download=False)
            data = self.yt.generate_schema(url, res)

        return data

    async def play_queue(self, ctx):
        for music_data in self.queue:
            url = music_data["download_url"]
            source = await discord.FFmpegOpusAudio.from_probe(url, **options["ffmpeg"])
            yt_url = music_data["url"]
            await ctx.send(f"Now playing ▶️: {yt_url}")
            ctx.voice_client.play(source)

    @commands.command(aliases=["l", "q", "queue"])
    async def list(self, ctx):
        queue_list = ""
        for i in range(len(self.queue)):
            formatted = self.yt.msg_format(self.queue[i])
            emojiNum = convert_to_equiv_digits(msg["digits"], i)
            queue_list += emojiNum + " " + formatted + "\n"

        await ctx.send(queue_list)

    @commands.command(aliases=["s", "stop"])
    async def pause(self, ctx):
        self.paused = True
        ctx.voice_client.pause()
        await ctx.send("Music Paused ⏸")

    @commands.command()
    async def resume(self, ctx):
        self.paused = False
        ctx.voice_client.resume()
        await ctx.send("Music Resumed ▶️")

def setup(client):
    client.add_cog(Music(client))
