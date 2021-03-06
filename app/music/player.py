import asyncio
from async_timeout import timeout
from discord.ext import commands

from app.utils.emitter import EventEmitter
from app.music.embed import MusicEmbed as Embed
from app.music.playlist import Playlist

class MusicPlayer:
    def __init__(self, bot: commands.Bot, ctx: commands.Context):
        self.__bot = bot
        self.__ctx = ctx

        self.current = None
        self.playlist = Playlist()
        self.voice = None # voice_state
        self.__loop = 0
        self.__loop_count = 0
        self.__inactive = False

        self.__event_controller = asyncio.Event()
        self.__listener = EventEmitter()

        player = bot.loop.create_task(self.play_tracks())
        self.__listener.on("cleanup", lambda: player.cancel())

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
                    self.__bot.loop.create_task(self.off())
                    return
            
            self.voice.play(self.current.source, after=self.play_next_track)
            if self.__loop_count == 0:
                embed = self.current.embed(header="▶️ Now playing!")
                await self.current.requester.channel.send(embed=embed)
                
            await self.__event_controller.wait()

    def play_next_track(self, error=None):
        if error:
            raise MusicPlayerError(str(error))
            
        if not self.__loop:
            self.current = None
            self.__loop_count = 0
        else:
            self.__loop_count += 1

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
        self.__listener.on("cleanup", fn, *args)

    async def off(self):
        if not self.voice:
            raise MusicPlayerError("Is not connected to any voice client!")
        
        await self.voice.disconnect()
        self.__listener.emit("cleanup")

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