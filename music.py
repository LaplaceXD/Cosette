import discord
from discord.ext import commands
from utils import search, extract_youtube_data, format_youtube_data
import youtube_dl
from random import randint

class music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.paused = False
        self.queue = []
        self.FFMPEG_OPTIONS = {
            "before_options":
            "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            "options": "-vn"
        }
        self.YDL_OPTIONS = {"format": "bestaudio"}
        self.DIGITS_EMOJI = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣","9️⃣"]
        self.QUOTES = [
            "I think I have taken a liking to you. Won't you be my darling?",
            "I like the look in your eyes. It makes my heart race. You are now my darling!",
            "Wow, your taste makes my heart race. It bites and lingers... The taste of danger. You are now my darling!",
            "Once we die, we'll only be a statistic. It won't matter what we were called.",
            "Don't worry, we'll always be together. Until the day we die.",
            "The weak ones die, big deal.",
            "If you have anything you wanna say, you better spit it out while you can. Because you're all going to die sooner or later.",
            "It's been a long time since I last saw a human cry.",
        ]

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(self.QUOTES[randint(0, 7)])

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
    async def add(self, ctx, *, searchStr=None):
        await self.join(ctx)

        if self.paused and searchStr is None:
            await self.resume(ctx)
        else:
            url =  searchStr if searchStr.startswith("$https") else search(searchStr)
            music_data = {}
            with youtube_dl.YoutubeDL(self.YDL_OPTIONS) as ydl:
                data = ydl.extract_info(url, download=False)
                music_data = extract_youtube_data(url, data)
            
            queue_length = len(self.queue)
            self.queue.insert(queue_length, music_data)
            if queue_length > 0:
                await ctx.send(f"Queued Song#{queue_length}📜: {url}")
            else:
                await self.play_queue(ctx)

    async def play_queue(self, ctx):
        vc = ctx.voice_client

        for music_data in self.queue:
            url = music_data["download_url"]
            source = await discord.FFmpegOpusAudio.from_probe(url, **self.FFMPEG_OPTIONS)
            yt_url = music_data["url"]
            await ctx.send(f"Now playing ▶️: {yt_url}")
            vc.play(source)

    @commands.command(aliases=["l", "q", "queue"])
    async def list(self, ctx):
        queue_list = ""
        for i in range(len(self.queue)):
            formatted = format_youtube_data(self.queue[i])
            emojiNum = "".join([self.DIGITS_EMOJI[int(num)] for num in str(i)])
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
    client.add_cog(music(client))
