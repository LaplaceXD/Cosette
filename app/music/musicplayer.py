import asyncio
from asyncio_timeout import timeout
from discord.ext import commands
from app.music.playlist import Playlist

class MusicPlayer:
    def __init__(self, bot: commands.Bot, ctx: commands.Context):
        self.bot = bot
        self.__ctx = ctx

        self.current = None
        self.next = asyncio.Event()
        self.playlist = Playlist()

        self.__voice = None # voice_state
        self.__playing = False

        self.player = bot.loop.create_task(self.play_tracks())

    def __del__(self):
        self.player.cancel()

    async def play_tracks(self):
        while True:
            self.next.clear()

            if not self.__playing:
                try:
                    async with timeout(180):
                        self.current = self.playlist.next()
                except asyncio.timeoutError:
                    self.bot.loop.create_task(self.stop())
                    return

        self.__voice.play(self.current.source, after=self.play_next_track)
        await self.ctx.channel.send(embed=self.current.create_embed(header="▶️ Now playing!"))

        await self.next.wait()

    def play_next_track(self, error=None):
        if error:
            raise MusicPlayerError(str(error))

        self.next.set()

class MusicPlayerError(Exception):
    def __init__(self, *args):
        self.message = args[0] if args else None

    def __str__(self):
        return f"MUSIC PLAYER ERROR: {self.message}" if self.message else f"MUSIC PLAYER ERROR has been raised!"