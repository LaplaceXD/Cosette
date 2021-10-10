from discord import Embed
from discord.ext import commands, tasks
from app.utils import extract_json, convert_to_equiv_digits
from app.music.youtubesource import YoutubeDLSource

from app.music.embeds import Embeds
from app.music.musicplayer import MusicPlayer

msg = extract_json("msg_templates")
bot_properties = extract_json("properties")
EMBED_WARNING_COLOR = int(bot_properties["COLORS"]["WARNING"], 16)
FOOTER_TEXT = bot_properties["FOOTER"]

class MusicBot(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.music_players = {}

    def get_music_player(self, ctx: commands.Context):
        music_player = self.music_players.get(ctx.guild.id)
        if not music_player:
            music_player = MusicPlayer(self.client, ctx)
            self.music_players[ctx.guild.id] = music_player
        
        return music_player

    def cog_unload(self):
        for music_player in self.music_players.values():
            self.client.loop.create_task(music_player.stop())

    async def cog_before_invoke(self, ctx: commands.Context):
        ctx.music_player = self.get_music_player(ctx)

    @commands.command(
        name="join", 
        description="Lets the bot join the current voice channel", 
        aliases=["j"], 
        invoke_without_subcommand=True
    )
    async def _join(self, ctx: commands.Context):
        channel = ctx.author.voice.channel
        if ctx.music_player.voice:
            await ctx.music_player.voice.move_to(channel)
            return

        ctx.music_player.voice = await channel.connect()
        await ctx.guild.get_member(self.client.user.id).edit(mute=False, deafen=True) # deafen the bot on enter
    
    @commands.command(
        name="disconnect",
        aliases=["d"],
        description="Music bot leaves the current channel."
    )
    async def _disconnect(self, ctx: commands.Context):
        if not ctx.music_player.voice:
            # change to notice embed
            return await ctx.send('Not connected to any voice channel.')

        await ctx.voice_state.stop()
        del self.voice_states[ctx.guild.id]

    @commands.command(
        name="play",
        aliases=["p"],
        description="Plays a track" 
    )
    async def _play(self, ctx: commands.Context, *, query: str):
        if not ctx.music_player.voice:
            await ctx.invoke(self._join)

        async with ctx.typing(): # shows typing in discord
            try:
                music = YoutubeDLSource().get_music(query, ctx)
            except Exception as e:
                await Embeds().simple("Youtube Download Error", e, "WARNING").send_embed(ctx)
            else:
                await ctx.music_player.playlist.add(music)
                
                if ctx.music_player.is_playing:
                    embed = music.create_embed(header=f"📜 [{ctx.music_player.playlist.size()}] Music Queued")
                    await ctx.send(embed=embed)

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await Embeds().simple("Command Error", error, "WARNING").send_embed(ctx)
        
    @_join.before_invoke
    @_play.before_invoke
    async def ensure_voice(self, ctx: commands.Context):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError("Connect to a voice channel first.")

        # if ctx is in a voice_client but it is not the same voice_client as bot
        if ctx.voice_client and ctx.voice_client.channel != ctx.author.voice.channel:
            raise commands.CommandError("I am already in a voice channel.")

# # Currently Legacy Code
# class MusicBot(commands.Cog):
#     def __init__(self, client):
#         self.client = client
#         self.yt = Youtube()
        
#         self.ytdl = YoutubeDLSource()
#         self.current_music = {}
#         self.song_started = False
#         self.has_joined = False
#         self.paused = False
#         self.queue = []
#         self.rechecks = 0
#         self.inactive = False

#     def cog_unload(self, ctx):
#         self.restart()
    
#     def reset(self):
#         self.current_music = {}
#         self.song_started = False
#         self.has_joined = False
#         self.paused = False
#         self.queue = []
#         self.rechecks = 0
#         self.inactive = False

#     @commands.command(aliases=["r"])
#     async def restart(self, ctx):
#         self.reset()
#         await ctx.send("Restarting.")
#         exit(1)
    
#     @commands.command(aliases=["j"])
#     async def join(self, ctx):  
#         if ctx.author.voice is None:
#             await ctx.send("You're not in a voice channel!")
#         else:
#             channel = ctx.author.voice.channel
#             await channel.connect() if ctx.voice_client is None else ctx.voice_client.move_to(channel)
#             self.voice = ctx.voice_client
#             await ctx.guild.get_member(self.client.user.id).edit(mute=False, deafen=True)
#             self.check_if_playing.start(ctx)

#     @commands.command()
#     async def printjson(self, ctx):
#         print(self.current_music.get_details(simplified=False))
     
#     @commands.command(aliases=["d", "dc"])
#     async def disconnect(self, ctx):
#         print("Disconnecting!")
#         if ctx.voice_client.is_playing(): 
#             ctx.voice_client.stop()
#         self.check_if_playing.cancel()  
#         self.check_songs.cancel()
#         self.reset()

#         await ctx.voice_client.disconnect()

#     @tasks.loop(minutes=5.0)
#     async def check_songs(self, ctx):
#         if len(self.queue) == 0 and not bool(self.current_music) and self.inactive:
#             await ctx.send("Nangluod na ang bot.") 
#             await self.disconnect(ctx)

#     @commands.command(aliases=["p"])
#     async def play(self, ctx, *, query=None):
#         if ctx.voice_client is None:
#             await self.join(ctx)

#         if query is None:
#             if self.current_music:
#                 await self.resume(ctx)
#             else:
#                 await ctx.send("No track inputted!")
#         else:
#             music = self.ytdl.get_music(query, ctx)
#             self.queue.insert(len(self.queue), music)
#             if len(self.queue) >= 0 and bool(self.current_music):
#                 embed = music.create_embed(header=f"📜 [{len(self.queue)}] Music Queued")
#                 await ctx.send(embed=embed)

#     @tasks.loop(seconds=5.0)
#     async def check_if_playing(self, ctx):
#         if not bool(self.current_music):
#             self.rechecks += 1
#         else:
#             self.rechecks = 0
#             self.inactive = False
#             if self.check_songs.is_running:
#                 self.check_songs.cancel()

#         if not ctx.voice_client.is_playing() and not self.paused:
#             self.song_started = False
#             self.current_music = {} if len(self.queue) == 0 else self.queue.pop(0)
#             await self.play_track(ctx)
                
#     async def play_track(self, ctx):
#         if self.song_started:
#             print("Music in progress")
#             return
#         elif not bool(self.current_music):
#             print(f"{self.rechecks} No songs in queue")
#             if self.rechecks == 12:
#                 print("Disconnecting in one minute.")
#                 self.check_songs.start(ctx)
#                 self.inactive = True
#             return

#         source = self.current_music.source
#         ctx.voice_client.play(source)
#         embed = self.current_music.create_embed(header="▶️ Now playing!")
#         await self.current_music.channel.send(embed=embed)
#         self.song_started = True
            
#     @commands.command(aliases=["s", "sk"])
#     async def skip(self, ctx):
#         ctx.voice_client.stop()
#         if self.paused:
#             ctx.voice_client.resume()

#         self.paused = False
#         self.song_started = False
#         self.current_music = {} if len(self.queue) == 0 else self.queue.pop(0)
#         await self.play_track(ctx)

#     @commands.command(aliases=["rm"])
#     async def remove(self, ctx, num):
#         index = int(num)
#         if index > len(self.queue) or index < 1:
#             embed = Embed(title="Oi mate! Wrong number.")
#         else:
#             removed = self.queue.pop(index - 1)
#             embed =  removed.create_embed(header="😢 Removed From Queue", simplified=True)

#         await ctx.send(embed=embed)

#     @commands.command()
#     async def playing(self, ctx):
#         if not bool(self.current_music):
#             embed = Embed(title="No track currently playing.", color=0xff0059)
#         else:
#             embed = self.current_music.create_embed(header="▶️ Currently Playing", show_tags=True)
    
#         await ctx.send(embed=embed)

#     @commands.command(aliases=["l", "q", "queue"])
#     async def list(self, ctx):
#         if len(self.queue) == 0:
#             queue_list = "No tracks in queue."
#         else:
#             queue_list = ""
#             for i in range(len(self.queue)):
#                 formatted = self.yt.msg_format(self.queue[i])
#                 emojiNum = convert_to_equiv_digits(msg["digits"], i + 1)
#                 queue_list += emojiNum + " " + formatted + "\n"

#         await ctx.send(queue_list)

#     @commands.command(aliases=["stop"])
#     async def pause(self, ctx):
#         ctx.voice_client.pause()
#         self.paused = True
#         await ctx.send("⏸ Music Stopped.")

#     @commands.command()
#     async def resume(self, ctx):
#         ctx.voice_client.resume()
#         self.paused = False
#         await ctx.send("▶️ Music Resumed.")

def setup(client):
    client.add_cog(MusicBot(client))