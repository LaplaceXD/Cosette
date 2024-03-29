from discord.ext import commands

from app.music.source.youtube import YoutubeDLSource
from app.music.embed import MusicEmbed as Embed
from app.music.player import MusicPlayer as Player
from app.music.error.command import MusicCommandError as Error

class MusicBot(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.music_players = {}

    def get_music_player(self, ctx: commands.Context):
        music_player = self.music_players.get(ctx.guild.id)
        if not music_player:
            music_player = Player(self.client, ctx)
            music_player.on_cleanup(lambda: self.music_players.pop(ctx.guild.id))
            self.music_players[ctx.guild.id] = music_player
        
        return music_player

    def cog_unload(self):
        for music_player in self.music_players.values():
            self.client.loop.create_task(music_player.off())

    # this is growing start refactoring
    async def cog_before_invoke(self, ctx: commands.Context):
        ctx.music_player = self.get_music_player(ctx)

        if not ctx.author.voice or not ctx.author.voice.channel:
            raise Error.NotInAVoiceChannel()

        if hasattr(ctx.voice_client, "voice"):
            if ctx.voice_client.voice != ctx.author.voice.channel:
                raise Error.BotAlreadyInChannel()

        if not ctx.music_player.voice and not ctx.command.name in ["join", "play"]:
            raise Error.NotInAVoiceChannel(bot=True)

        if not ctx.music_player.is_playing and ctx.command.name in ["resume", "pause", "current", "skip", "loop"]:
            raise Error.NotCurrentlyPlaying()

        if ctx.music_player.playlist.size == 0 and ctx.command.name in ["queue", "remove", "shuffle"]:
           raise Error.EmptyQueue()

        if ctx.command.name in ["play", "skip"]:
            ctx.music_player.loop = False

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if hasattr(error, "type") and error.type == Error.notice:
            embed = Embed(**error.details)
        elif hasattr(error, "type") and error.type == Error.warning:
            embed = Embed.warning(**error.details)
        else:
            embed = Embed.error(title="Unexpected Error", description=str(error))

        await ctx.send(embed=embed)

    @commands.command(
        name="join", 
        description="Lets the bot join the current voice channel", 
        aliases=["j", "ali"], 
        invoke_without_subcommand=True
    )
    async def _join(self, ctx: commands.Context):
        channel = ctx.author.voice.channel

        if ctx.music_player.voice:
            await ctx.music_player.voice.move_to(channel)
        else:
            ctx.music_player.voice = await channel.connect()

        await (ctx.guild
            .get_member(self.client.user.id)
            .edit(mute=False, deafen=True)) # deafen the bot on enter
    
    @commands.command(
        name="disconnect",
        aliases=["d", "leave", "layas"],
        description="Music bot leaves the current channel."
    )
    async def _disconnect(self, ctx: commands.Context):
        await ctx.music_player.off()
        await ctx.message.add_reaction("🖕")

    @commands.command(
        name="play",
        aliases=["p", "tukargud"],
        description="Plays a track." 
    )
    async def _play(self, ctx: commands.Context, *, query: str = None):
        if not ctx.music_player.voice:
            await ctx.invoke(self._join)
        
        if not query:
            raise Error.MissingPlayQuery()

        async with ctx.typing():
            try:
                music = YoutubeDLSource.get_music(query, ctx)
            except Exception as e:
                print(f"YOUTUBE DL ERROR: {str(e)}")
                raise Error.UnplayableTrack()
            else:
                await ctx.music_player.playlist.add(music)
                if ctx.music_player.is_playing:
                    embed = music.embed(header=f"📜 [{ctx.music_player.playlist.size}] Music Queued")
                    await ctx.send(embed=embed)
    
    @commands.command(
        name="current",
        aliases=["curr", "np", "now", "playing", "unsani"],
        description="Displays the currently active track."
    )
    async def _current(self, ctx: commands.Context):
        embed = ctx.music_player.current.embed(header="▶️ Currently Playing", show_tags=True)
        await ctx.send(embed=embed)

    @commands.command(
        name="loop",
        aliases=["repeat"],
        description="Loops the current track."
    )
    async def _loop(self, ctx: commands.Context):
        ctx.music_player.loop =  not ctx.music_player.loop

        header = "🔄 Currently Looping" if ctx.music_player.loop else "⏹️ Stopped Looping"
        embed = ctx.music_player.current.embed(header=header, simplified=True)
        await ctx.send(embed=embed)
        await ctx.message.add_reaction("🔄" if ctx.music_player.loop else "⏹️")

    @commands.command(
        name="resume",
        description="Resumes the currently playing track."
    )
    async def _resume(self, ctx: commands.Context):
        if ctx.voice_client.is_playing():
            raise Error.MusicAlready("Playing")

        ctx.music_player.resume()
        embed = ctx.music_player.current.embed(header="▶️ Music Resumed", simplified=True)
        await ctx.send(embed=embed)
        await ctx.message.add_reaction("▶️")

    @commands.command(
        name="pause",
        description="Pauses the currently playing track."
    )
    async def _pause(self, ctx: commands.Context):
        if not ctx.voice_client.is_playing():
            raise Error.MusicAlready("Paused")

        ctx.music_player.pause()
        embed = ctx.music_player.current.embed(header="⏸ Music Paused", simplified=True)
        await ctx.send(embed=embed)
        await ctx.message.add_reaction("⏸")

    @commands.command(
        name="queue",
        aliases=["q", "unsaysoundtrip"],
        description="Returns the list of songs in queue."
    )
    async def _queue(self, ctx: commands.Context, page: int = 1):
        playlist = ctx.music_player.playlist
        pagination_size = 8

        if page < 1 or (page - 1) * pagination_size > playlist.size:
            raise Error.OutOfRange("Page")
        
        embed = playlist.paginate(pagination_size, page).embed()
        await ctx.send(embed=embed)

    @commands.command(
        name="skip",
        aliases=["s", "skipnauy"],
        description="Skips the currently playing track."
    )
    async def _skip(self, ctx: commands.Context):
        ctx.music_player.skip()
        embed = ctx.music_player.current.embed(header="⏭ Skipped", simplified=True)
        await ctx.send(embed=embed)

    @commands.command(
        name="remove",
        aliases=["rm", "tangtangagud"],
        description="Removes a music with the given index from the queue."
    )
    async def _remove(self, ctx: commands.Context, idx: int = -1):
        size = ctx.music_player.playlist.size

        if idx < 1 or idx > size:
            raise Error.OutOfRange("Music Number")

        removed = ctx.music_player.playlist.remove(idx - 1)
        embed = removed.embed(header="❌ Removed From Queue", simplified=True)
        await ctx.send(embed=embed)

    @commands.command(
        name="shuffle",
        aliases=["mixmixmix"],
        desciption="Shuffles the queue."
    )
    async def _shuffle(self, ctx: commands.Context):
        ctx.music_player.playlist.shuffle()
        embed = Embed(title="🔀 Queue Shuffled", description="Now, which is which?!")
        await ctx.send(embed=embed)
        await ctx.message.add_reaction("🔀")

def setup(client):
    client.add_cog(MusicBot(client))