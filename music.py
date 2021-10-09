import discord
from discord.ext import commands, tasks
from youtube import Youtube
from utils import extract_json, convert_to_equiv_digits
import youtube_dl
import time

options = extract_json("options")
msg = extract_json("msg_templates")

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.yt = Youtube()
        
        self.currently_playing = {}
        self.song_started = False
        self.has_joined = False
        self.paused = False
        self.queue = []
        self.rechecks = 0
        self.inactive = False
        
    def cog_unload(self, ctx):
        self.restart()
    
    def reset(self):
        self.currently_playing = {}
        self.song_started = False
        self.has_joined = False
        self.paused = False
        self.queue = []
        self.rechecks = 0
        self.inactive = False 
    
    @commands.command(aliases=["j"])
    async def join(self, ctx):  
        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel!")
        else:
            channel = ctx.author.voice.channel
            await channel.connect() if ctx.voice_client is None else ctx.voice_client.move_to(channel)
            await ctx.guild.get_member(self.client.user.id).edit(mute=False, deafen=True)
            self.check_if_playing.start(ctx)
            
    @commands.command(aliases=["d", "dc"])
    async def disconnect(self, ctx):
        print("Disconnecting!")
        if ctx.voice_client.is_playing(): 
            ctx.voice_client.stop()
        self.check_if_playing.cancel()  
        self.check_songs.cancel()
        self.reset()
        
        await ctx.voice_client.disconnect()

    @tasks.loop(seconds=10)
    async def check_songs(self, ctx):
        if len(self.queue) == 0 and not bool(self.currently_playing) and self.inactive:
            await ctx.send("Nangluod na ang bot.") 
            await self.disconnect(ctx)

    @commands.command(aliases=["p"])
    async def play(self, ctx, *, query=None):
        if ctx.voice_client is None:
            await self.join(ctx)

        if query is None:
            if self.currently_playing:
                await self.resume(ctx)
            else:
                await ctx.send("No track inputted!")
        else:
            url = query if query.startswith("$https") else self.yt.search(query)
            music_data = self.extract_yt_data(url)
            self.queue.insert(len(self.queue), music_data)
            if len(self.queue) >= 0 and bool(self.currently_playing):
                await ctx.send(f"Queued Song#{len(self.queue)} 📜: {url}")
            
    @commands.command(aliases=["s", "sk"])
    async def skip(self, ctx):
        ctx.voice_client.stop()
        if self.paused:
            ctx.voice_client.resume()

        self.paused = False
        self.song_started = False
        self.currently_playing = {} if len(self.queue) == 0 else self.queue.pop(0)
        await self.play_track(ctx)

    @commands.command(aliases=["rm"])
    async def remove(self, ctx, num):
        index = int(num)
        if index > len(self.queue) or index < 1:
            await ctx.send("Oi mate! Wrong number.")
        else:
            removed = self.queue.pop(index - 1)
            await ctx.send(f"Removed from queue:\n{self.yt.msg_format(removed)}")

    # refactor this?
    def extract_yt_data(self, url):
        with youtube_dl.YoutubeDL(options["ydl"]) as ydl:
            res = ydl.extract_info(url, download=False)
            data = self.yt.generate_schema(url, res)

        return data

    @commands.command()
    async def playing(self, ctx):
        if not bool(self.currently_playing):
            msg = "No track currently playing."
        else:
            msg = f"▶️ Currently playing: {self.yt.msg_format(self.currently_playing)}"
    
        await ctx.send(msg)

    @tasks.loop(seconds=5.0)
    async def check_if_playing(self, ctx):
        if not bool(self.currently_playing):
            self.rechecks += 1
        else:
            self.rechecks = 0
            self.inactive = False
            if self.check_songs.is_running:
                self.check_songs.cancel()

        if not ctx.voice_client.is_playing() and not self.paused:
            self.song_started = False
            self.currently_playing = {} if len(self.queue) == 0 else self.queue.pop(0)
            await self.play_track(ctx)
                
    async def play_track(self, ctx):
        if self.song_started:
            print("Music in progress")
            return
        elif not bool(self.currently_playing):
            print(f"{self.rechecks} No songs in queue")
            if self.rechecks == 12:
                print("Disconnecting in one minute.")
                self.check_songs.start(ctx)
                self.inactive = True
            return

        title = self.currently_playing["title"]
        channel = self.currently_playing["channel"]
        duration = time.strftime('%H:%M:%S', time.gmtime(int(self.currently_playing["duration"])))
        download_url = self.currently_playing["download_url"]
        display_url = self.currently_playing["url"]
        likes = self.currently_playing["like_count"]
        dislikes = self.currently_playing["dislike_count"]
        thumbnail = self.currently_playing["thumbnail"]

        source = await discord.FFmpegOpusAudio.from_probe(download_url, **options["ffmpeg"])
        ctx.voice_client.play(source)
        embed = discord.Embed(title=title, url=display_url, color=0xff0059)
        embed.set_author(name="▶️ Now playing!", icon_url="https://cdn.discordapp.com/attachments/797083893014462477/896312760084889600/unknown.png")
        embed.set_thumbnail(url=thumbnail)
        embed.add_field(name="📺 Channel", value=channel)
        embed.add_field(name="🕒 Duration", value=duration, inline=False)
        embed.add_field(name="👍 Likes", value=likes)
        embed.add_field(name="👎 Dislikes", value=dislikes)
        embed.set_footer(text="Made with love by Laplace ❤️")
        await ctx.send(embed=embed)
        self.song_started = True

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
        self.paused = True
        await ctx.send("⏸ Music Stopped.")

    @commands.command()
    async def resume(self, ctx):
        ctx.voice_client.resume()
        self.paused = False
        await ctx.send("▶️ Music Resumed.")

def setup(client):
    client.add_cog(Music(client))
