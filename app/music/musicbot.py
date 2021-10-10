from discord.ext import commands
from math import ceil

from app.music.youtubesource import YoutubeDLSource
from app.music.musicembed import MusicEmbed
from app.music.musicplayer import MusicPlayer

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
            embed = MusicEmbed("WARNING", title="Can't Disconnect", description="I'm not even connected to any voice channel.")
            return await ctx.send(embed=embed)

        await ctx.music_player.stop()

        if ctx.music_player.is_inactive:
            embed = MusicEmbed(title="🔌 Disconnnected due to Inactivity.", description="Nangluod na ko walay kanta.")
        else:
            embed = MusicEmbed("NOTICE", title="Disconnected", description="It was a pleasure to play music for you.")
        await self.__ctx.send(embed=embed)
        await ctx.message.add_reaction("✅")

        del self.music_players[ctx.guild.id]

    @commands.command(
        name="play",
        aliases=["p"],
        description="Plays a track." 
    )
    async def _play(self, ctx: commands.Context, *, query: str):
        if not ctx.music_player.voice:
            await ctx.invoke(self._join)

        async with ctx.typing(): # shows typing in discord
            try:
                music = YoutubeDLSource().get_music(query, ctx)
            except Exception as e:
                await ctx.send(embed=MusicEmbed("WARNING", title="Youtube Download Error", description=str(e)))
            else:
                await ctx.music_player.playlist.add(music)
                
                if ctx.music_player.is_playing:
                    embed = music.create_embed(header=f"📜 [{ctx.music_player.playlist.size()}] Music Queued")
                    await ctx.send(embed=embed)

    @commands.command(name="queue", aliases=["q"], description="Returns the list of songs in queue.")
    async def _queue(self, ctx: commands.Context, page: int = 1):
        max = ceil(ctx.music_player.playlist.size() / 8) # probably refactor this

        if page < 1 or page * 8 > ctx.music_player.playlist.size():
            embed = MusicEmbed("WARNING", title="Page Out of Range", description=f"It's not that big, input a value between 0 and {max}.")
            return await ctx.send(embed=embed) 

        await ctx.send(embed=ctx.music_player.playlist.create_embed(8, page))

    @commands.command(name="current", aliases=["curr"], description="Displays the currently active track.")
    async def _current(self, ctx: commands.Context):
        if ctx.music_player.current is None:
            embed = MusicEmbed("NOTICE", title="No Track Currently Playing", description="Maybe you can add some songs?")
        else:
            embed = ctx.music_player.current.create_embed(header="▶️ Currently Playing", show_tags=True)

        await ctx.send(embed=embed)

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.send(embed=MusicEmbed("WARNING", title="Command Error", description=str(error)))
        
    @_join.before_invoke
    @_play.before_invoke
    async def ensure_voice(self, ctx: commands.Context):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError("Connect to a voice channel first.")

        # if ctx is in a voice_client but it is not the same voice_client as bot
        if ctx.voice_client and ctx.voice_client.channel != ctx.author.voice.channel:
            raise commands.CommandError("I am already in a voice channel.")

def setup(client):
    client.add_cog(MusicBot(client))