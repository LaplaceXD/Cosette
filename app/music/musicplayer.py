import asyncio
from async_timeout import timeout
from discord.ext import commands
from app.music.playlist import Playlist
from app.music.musicembed import MusicEmbed

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

    @property
    def is_inactive(self):
        return self.__inactive

    async def play_tracks(self):
        while True:
            self.next.clear()

            if not self.__loop:
                try:
                    async with timeout(180):
                        self.current = await self.playlist.next()
                except asyncio.timeoutError:
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

        self.next.set()
    
    async def stop(self):
        self.playlist.clear()

        if self.voice:
            await self.voice.disconnect()
            self.voice = None

class MusicPlayerError(Exception):
    def __init__(self, *args):
        self.message = args[0] if args else None

    def __str__(self):
        return f"MUSIC PLAYER ERROR: {self.message}" if self.message else f"MUSIC PLAYER ERROR has been raised!"