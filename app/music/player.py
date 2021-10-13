import asyncio
from functools import partial
from async_timeout import timeout
from discord.ext import commands

from app.music.embed import MusicEmbed as Embed
from app.music.playlist import Playlist

class MusicPlayer:
    def __init__(self, bot: commands.Bot, ctx: commands.Context):
        self.__bot = bot
        self.__ctx = ctx

        self.current = None
        self.playlist = Playlist()
        self.voice = None # voice_state
        self.__loop = False
        self.__inactive = False

        self.__event_controller = asyncio.Event()
        self.__player = bot.loop.create_task(self.play_tracks())
        self.__cleanup_fn = []

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
            self.__event_controller.clear()

            if not self.__loop:
                try:
                    async with timeout(180):
                        self.current = await self.playlist.next()
                except asyncio.TimeoutError:
                    self.__inactive = True
                    self.__bot.loop.create_task(self.stop())
                    return

            self.voice.play(self.current.source, after=self.play_next_track)
            embed = self.current.embed(header="▶️ Now playing!")
            await self.current.channel.send(embed=embed)
            await self.__event_controller.wait()

    def play_next_track(self, error=None):
        if error:
            raise MusicPlayerError(str(error))

        self.current = None
        self.__event_controller.set()

    def resume(self):
        self.voice.resume()

    def pause(self):
        self.voice.pause()

    def skip(self):
        if self.is_playing:
            self.voice.stop()
        else:
            raise MusicPlayerError("Self.current is None!")
    
    def on_cleanup(self, fn=None, *args):
        if type(fn) == "function":
            raise MusicPlayerError("You need to pass a callable function to the argument.")

        partial_fn = partial(fn, *args);
        self.__cleanup.insert(len(self.__cleanup), partial_fn)
        
        return self

    def __execute_cleanup(self):
        self.playlist.clear() # is this required?
        self.__player.cancel() # remove task in loop 
        [fn() for fn in self.__cleanup_fn]

    async def stop(self):
        if not self.voice:
            raise MusicPlayerError("Is not connected to any voice client!")
        
        await self.voice.disconnect()
        self.__execute_cleanup()

        if self.__inactive:
            embed = Embed(title="🔌 Disconnnected Due to Inactivity", description="Nangluod na ko walay kanta.")
        else:
            embed = Embed(title="🔌 Disconnected", description="Ai, ing ana man jud ka. Ge.")

        await self.__ctx.send(embed=embed)

class MusicPlayerError(Exception):
    def __init__(self, *args):
        self.message = args[0] if args else None

    def __str__(self):
        return f"MUSIC PLAYER ERROR: {self.message}" if self.message else f"MUSIC PLAYER ERROR has been raised!"