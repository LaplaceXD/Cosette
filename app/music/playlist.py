import asyncio
from app.music.music import Music

class Playlist(asyncio.Queue):
    async def next(self):
        return await self.get()

    def add(self, music: Music):
        return self.put_nowait(music)

    def clear(self):
        for _ in range(self.qsize()):
            self.get_nowait()
            self.task_done()