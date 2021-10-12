import asyncio
from async_timeout import timeout
from discord.ext import commands

from app.music.embed import MusicEmbed
from app.music.playlist import Playlist
from app.music.error.player import MusicPlayerError

class MusicPlayer:
    def __init__(self, bot: commands.Bot, ctx: commands.Context):
        self.bot = bot
        self.__ctx = ctx

        self.current = None
        self.next = asyncio.Event()
        self.playlist = Playlist()

        self.__inactive = False
        self.voice = None # voice_state
        self.__loop = False

        self.player = bot.loop.create_task(self.play_tracks())

    def __del__(self):
        self.player.cancel()

    @property
    def loop(self):
        return self.__loop

    @loop.setter
    def loop(self, value: bool):
        self.__loop = value

    @property
    def is_playing(self):
        return self.voice and self.current

    # refactor this
    def create_current_embed(self, header: str = None, simplified: bool=False, show_tags: bool = False):
        if self.current:
            embed = self.current.create_embed(header=header, simplified=simplified, show_tags=show_tags)
        else:
            embed = MusicEmbed(
                title="No Track Currently Playing",
                description="Maybe you can add some songs?"
            ) 
        
        return embed

    async def play_tracks(self):
        while True:
            self.next.clear()

            if not self.__loop:
                try:
                    async with timeout(180):
                        self.current = await self.playlist.next()
                except asyncio.timeoutError:
                    print("Inactive")
                    self.__inactive = True
                    self.bot.loop.create_task(self.stop())
                    return

            self.voice.play(self.current.source, after=self.play_next_track)
            embed = self.current.create_embed(header="▶️ Now playing!")
            await self.current.channel.send(embed=embed)

            await self.next.wait()

    def play_next_track(self, error=None):
        if error:
            raise MusicPlayerError(str(error))

        self.current = None
        self.next.set()

    def resume(self):
        self.voice.resume()

    def pause(self):
        self.voice.pause()

    def skip(self):
        if self.is_playing:
            self.voice.stop()
        else:
            raise MusicPlayerError("Self.current is None!")
    
    async def stop(self):
        self.playlist.clear()

        if self.__inactive:
            embed = MusicEmbed(title="🔌 Disconnnected due to Inactivity.", description="Nangluod na ko walay kanta.")
        else:
            embed = MusicEmbed(title="Disconnected", description="Ai, ing ana man jud ka. Ge.")
        await self.__ctx.send(embed=embed)

        if self.voice:
            await self.voice.disconnect()
            self.voice = None
            self.current = None
            self.__inactive = False
            self.__loop = False