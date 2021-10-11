from discord.ext import commands

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

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.send(embed=MusicEmbed("WARNING", title="Command Error", description=str(error)))

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
            return

        ctx.music_player.voice = await channel.connect()
        await ctx.guild.get_member(self.client.user.id).edit(mute=False, deafen=True) # deafen the bot on enter
    
    @commands.command(
        name="disconnect",
        aliases=["d", "leave", "layas"],
        description="Music bot leaves the current channel."
    )
    async def _disconnect(self, ctx: commands.Context):
        if not ctx.music_player.voice:
            embed = MusicEmbed("WARNING", title="Can't Disconnect", description="I'm not even connected to any voice channel.")
            return await ctx.send(embed=embed)

        await ctx.music_player.stop()
        await ctx.message.add_reaction("✅")

        del self.music_players[ctx.guild.id]

    @commands.command(
        name="play",
        aliases=["p", "tukargud"],
        description="Plays a track." 
    )
    async def _play(self, ctx: commands.Context, *, query: str):
        if not ctx.music_player.voice:
            await ctx.invoke(self._join)

        async with ctx.typing(): # shows typing in discord
            try:
                music = YoutubeDLSource().get_music(query, ctx)
            except Exception as e:
                print(f"YOUTUBE DL ERROR: {str(e)}")
                embed = MusicEmbed(title="🙇 An Error Occured Queueing This Music", description="Try changing your keywords, or be more specific.")
                await ctx.send(embed=embed)
            else:
                await ctx.music_player.playlist.add(music)
                
                if ctx.music_player.is_playing:
                    embed = music.create_embed(header=f"📜 [{ctx.music_player.playlist.size()}] Music Queued")
                    await ctx.send(embed=embed)

    @commands.command(name="queue", aliases=["q", "unsaysoundtrip"], description="Returns the list of songs in queue.")
    async def _queue(self, ctx: commands.Context, page: int = 1):
        playlist = ctx.music_player.playlist

        print(playlist.size())
        if playlist.size() != 0 and (page < 1 or page * 2 > playlist.size()):
            embed = MusicEmbed("WARNING", title="Page Out of Range", description=f"It's not that big.")
            return await ctx.send(embed=embed) 

        await ctx.send(embed=playlist.paginate(2, page).create_embed())

    @commands.command(name="current", aliases=["curr", "unsani"], description="Displays the currently active track.")
    async def _current(self, ctx: commands.Context):
        if ctx.music_player.current is None:
            embed = MusicEmbed("NOTICE", title="No Track Currently Playing", description="Maybe you can add some songs?")
        else:
            embed = ctx.music_player.current.create_embed(header="▶️ Currently Playing", show_tags=True)

        await ctx.send(embed=embed)

    @commands.command(name="skip", aliases=["s", "skipnauy"], description="Skips the currently playing track.")
    async def _skip(self, ctx: commands.Context):
        if not ctx.music_player.is_playing:
            embed = MusicEmbed("NOTICE", title="No Track Currently Playing", description="Maybe you can add some songs?")
        else:
            ctx.music_player.skip()
            embed = ctx.music_player.current.create_embed(header="⏭ Skipped", simplified=True)
        await ctx.send(embed=embed)

    @commands.command(name="remove", aliases=["rm", "tangtangagud"], description="Removes a music with the given index from the queue.")
    async def _remove(self, ctx: commands.Context, idx: int = -1):
        max = ctx.music_player.playlist.size()
        if max == 0:
            embed = ctx.music_player.playlist.create_embed()
            return await ctx.send(embed=embed) 
        elif idx < 1 or idx > max:
            embed = MusicEmbed(title="Music Number out of Range", description=f"It's not that big.")
            return await ctx.send(embed=embed) 

        removed = ctx.music_player.playlist.remove(idx - 1)
        embed = removed.create_embed(header="❌ Removed From Queue", simplified=True)
        await ctx.send(embed=embed)

    @commands.command(name="shuffle", aliases=["mixmixmix"], desciption="Shuffles the queue.")
    async def _shuffle(self, ctx: commands.Context):
        if ctx.music_player.playlist.size() == 0:
            return await ctx.send(embed=ctx.music_player.playlist.create_embed())
        
        ctx.music_player.playlist.shuffle()
        await ctx.send(embed=MusicEmbed(title="🔀 Queue Shuffled", description="Now, which is which?!"))
        await ctx.message.add_reaction("🔀")
        
    @_join.before_invoke
    @_play.before_invoke
    async def ensure_voice(self, ctx: commands.Context):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError("Connect to a voice channel first.")

        # if ctx is in a voice_client but it is not the same voice_client as bot
        if hasattr(ctx.voice_client, "voice"):
            if ctx.voice_client.voice != ctx.author.voice.channel:
                raise commands.CommandError("I am already in a voice channel.")

    # Fix tomorrow
    # @_disconnect.before_invoke
    # @_skip.before_invoke
    # @_current.before_invoke
    # @_queue.before_invoke
    # @_remove.before_invoke
    # async def ensure_music_player(self, ctx: commands.Context):
    #     if not hasattr(ctx, "music_player") or not ctx.music_player.voice:
    #         raise commands.CommandError("I am not in a voice channel.")

def setup(client):
    client.add_cog(MusicBot(client))