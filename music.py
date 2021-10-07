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

        self.currently_playing = None
        self.has_music = False
        self.queue = []
        
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(msg["quotes"][randint(0, 7)])

    def restart(self):
        self.currently_playing = None
        self.has_music = False
        self.queue = []

    @commands.command(aliases=["j"])
    async def join(self, ctx):  
        self.restart()

        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel!")
        else:
            if ctx.voice_client is None:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.voice_client.move_to(ctx.author.voice.channel)

    @commands.command(aliases=["d", "dc"])
    async def disconnect(self, ctx):
        await ctx.voice_client.stop()
        await ctx.voice_client.disconnect()
        self.restart()

    @commands.command(aliases=["p"])
    async def play(self, ctx, *, query=None):
        await self.join(ctx)
        if ctx.voice_client is None:
            return

        if query is None:
            if ctx.is_playing:
                await ctx.send("No track inputted!")
            else:
                await self.resume(ctx)
        else:
            url = query if query.startswith("$https") else self.yt.search(query)
            music_data = self.extract_yt_data(url)
            self.queue.insert(len(self.queue), music_data)
            if len(self.queue) <= 1 and not self.has_music:
                self.currently_playing = self.queue.pop(0)
                await self.play_track(ctx)
            else:
                await ctx.send(f"Queued Song#{len(self.queue)} 📜: {url}")

    @commands.command(aliases=["s", "sk"])
    async def skip(self, ctx):
        ctx.voice_client.stop()
        self.has_music = False
        self.currently_playing = None if len(self.queue) == 0 else self.queue.pop(0)
        await self.play_track(ctx)

    # refactor this?
    def extract_yt_data(self, url):
        with youtube_dl.YoutubeDL(options["ydl"]) as ydl:
            res = ydl.extract_info(url, download=False)
            data = self.yt.generate_schema(url, res)

        return data

    @commands.command()
    async def playing(self, ctx):
        if self.has_music:
            msg = f"▶️ Currently playing: {self.yt.msg_format(self.currently_playing)}"
        else:
            msg = "No track currently playing."
    
        await ctx.send(msg)

    async def play_track(self, ctx):
        download_url = self.currently_playing["download_url"]
        display_url = self.currently_playing["url"]
        
        source = await discord.FFmpegOpusAudio.from_probe(download_url, **options["ffmpeg"])
        print(source)
        ctx.voice_client.play(source)
        self.has_music = True
        await ctx.send(f"▶️ Now playing: {display_url}")

    @commands.command(aliases=["l", "q", "queue"])
    async def list(self, ctx):
        if len(self.queue) == 0:
            queue_list = "No tracks in queue."
        else:
            queue_list = ""
            for i in range(len(self.queue)):
                formatted = self.yt.msg_format(self.queue[i])
                emojiNum = convert_to_equiv_digits(msg["digits"], i + 1)
                queue_list += emojiNum + " " + formatted + "\n"

        await ctx.send(queue_list)

    @commands.command(aliases=["stop"])
    async def pause(self, ctx):
        ctx.voice_client.pause()
        await ctx.send("⏸ Music Stopped.")

    @commands.command()
    async def resume(self, ctx):
        ctx.voice_client.resume()
        await ctx.send("▶️ Music Resumed.")

def setup(client):
    client.add_cog(Music(client))
