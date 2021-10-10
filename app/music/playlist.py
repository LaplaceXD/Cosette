import asyncio, itertools, random
from app.utils import handle_indexes
from app.music.music import Music

class Playlist(asyncio.Queue):
    def __getitem__(self, index: int or slice):
        if isinstance(index, slice):
            return list(itertools.islice(self._queue, index.start, index.stop, index.step))
        elif isinstance(index, int):
            idx = handle_indexes(index, self.qsize(), PlaylistError)
            return self._queue[idx]
        else:
            raise PlaylistError("Index type should be of type int or slice.")

    def __iter__(self):
        return self._queue.__iter__()

    def size(self):
        return self.qsize()

    def next(self):
        return self.get()

    def shuffle(self):
        random.shuffle(self._queue)

    def add(self, music: Music):
        return self.put_nowait(music)

    def remove(self, index: int):
        idx = handle_indexes(index)
        del self._queue[idx]

    def clear(self):
        return self._queue.clear()

class PlaylistError(Exception):
    def __init__(self, *args):
        self.message = args[0] if args else None

    def __str__(self):
        return f"PLAYLIST ERROR: {self.message}" if self.message else f"PLAYLIST ERROR has been raised!"