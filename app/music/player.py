import asyncio
from async_timeout import timeout
from discord.ext import commands

from app.music.embed import MusicEmbed
from app.music.playlist import Playlist

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

    @property
    def loop(self):
        return self.__loop

    @loop.setter
    def loop(self, value: bool):
        self.__loop = value

    @property
    def is_playing(self):
        return self.voice and self.current

    async def play_tracks(self):
        while True:
            self.next.clear()

            if not self.__loop:
                try:
                    async with timeout(180):
                        self.current = await self.playlist.next()
                except asyncio.TimeoutError:
                    self.__inactive = True
                    self.bot.loop.create_task(self.stop())
                    return

            self.voice.play(self.current.source, after=self.play_next_track)
            embed = self.current.embed(header="▶️ Now playing!")
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
        if not self.voice:
            raise MusicPlayerError("Is not connected to any voice client!")
        
        self.songs.clear()
        self.player.cancel() # remove task in loop 
        await self.voice.disconnect()

        if self.__inactive:
            embed = MusicEmbed(title="🔌 Disconnnected due to Inactivity.", description="Nangluod na ko walay kanta.")
        else:
            embed = MusicEmbed(title="Disconnected", description="Ai, ing ana man jud ka. Ge.")
        await self.__ctx.send(embed=embed)
            

class MusicPlayerError(Exception):
    def __init__(self, *args):
        self.message = args[0] if args else None

    def __str__(self):
        return f"MUSIC PLAYER ERROR: {self.message}" if self.message else f"MUSIC PLAYER ERROR has been raised!"