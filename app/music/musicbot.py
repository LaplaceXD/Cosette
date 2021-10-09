from discord.ext import commands, tasks
import youtube_dl
from app.utils import extract_json, convert_to_equiv_digits
from app.music.youtube import Youtube
from app.music.music import Music
from app.music.playlist import Playlist

options = extract_json("options")
msg = extract_json("msg_templates")

class MusicBot(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.yt = Youtube()
        
        # self.playlist = Playlist()
        self.current_music = {}
        self.song_started = False
        self.has_joined = False
        self.paused = False
        self.queue = []
        self.rechecks = 0
        self.inactive = False

    def cog_unload(self, ctx):
        self.restart()
    
    def reset(self):
        self.current_music = {}
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
            self.voice = ctx.voice_client
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
        if len(self.queue) == 0 and not bool(self.current_music) and self.inactive:
            await ctx.send("Nangluod na ang bot.") 
            await self.disconnect(ctx)

    @commands.command(aliases=["p"])
    async def play(self, ctx, *, query=None):
        if ctx.voice_client is None:
            await self.join(ctx)

        if query is None:
            if self.current_music:
                await self.resume(ctx)
            else:
                await ctx.send("No track inputted!")
        else:
            url = query if query.startswith("$https") else self.yt.search(query)
            music = self.extract_yt_data(url)
            self.queue.insert(len(self.queue), music)
            if len(self.queue) >= 0 and bool(self.current_music):
                embed = self.current_music.create_embed(header=f"📜 [{len(self.queue)}] Music Queued")
                await ctx.send(embed=embed)

    @tasks.loop(seconds=5.0)
    async def check_if_playing(self, ctx):
        if not bool(self.current_music):
            self.rechecks += 1
        else:
            self.rechecks = 0
            self.inactive = False
            if self.check_songs.is_running:
                self.check_songs.cancel()

        if not ctx.voice_client.is_playing() and not self.paused:
            self.song_started = False
            self.current_music = {} if len(self.queue) == 0 else self.queue.pop(0)
            await self.play_track(ctx)
                
    async def play_track(self, ctx):
        if self.song_started:
            print("Music in progress")
            return
        elif not bool(self.current_music):
            print(f"{self.rechecks} No songs in queue")
            if self.rechecks == 12:
                print("Disconnecting in one minute.")
                self.check_songs.start(ctx)
                self.inactive = True
            return

        source = await self.current_music.get_audio(options["ffmpeg"])
        ctx.voice_client.play(source)
        embed = self.current_music.create_embed(header="▶️ Now playing!")
        await ctx.send(embed=embed)
        self.song_started = True
            
    @commands.command(aliases=["s", "sk"])
    async def skip(self, ctx):
        ctx.voice_client.stop()
        if self.paused:
            ctx.voice_client.resume()

        self.paused = False
        self.song_started = False
        self.current_music = {} if len(self.queue) == 0 else self.queue.pop(0)
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
            res["url"] = {
                "display": url,
                "download": res["formats"][0]["url"]
            }
        
        return Music(res)

    @commands.command()
    async def playing(self, ctx):
        if not bool(self.current_music):
            msg = "No track currently playing."
        else:
            msg = f"▶️ Currently playing: {self.yt.msg_format(self.current_music)}"
    
        await ctx.send(msg)

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
    client.add_cog(MusicBot(client))
