import asyncio, itertools, random
from app.utils import handle_indexes, convert_to_equiv_emoji_digits
from app.music.music import Music
from app.music.musicembed import MusicEmbed

class Playlist(asyncio.Queue):
    def __getitem__(self, index: int or slice):
        if isinstance(index, slice):
            return list(itertools.islice(self._queue, index.start, index.stop, index.step))
        elif isinstance(index, int):
            idx = handle_indexes(index, int(self.qsize()), PlaylistError)
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
        return self.put(music)

    def remove(self, index: int):
        idx = handle_indexes(index)
        del self._queue[idx]

    def clear(self):
        return self._queue.clear()

    # add pagination
    def create_embed(self):
        if self.qsize() == 0:
            description = "There are currently no music on queue. Add one?"
        else:
            description = "Here are the list of songs that are currently on queue."

        embed = MusicEmbed(description=description).add_header(header="🎶 Music Queue").add_footer()

        for i in range(self.qsize()):
            props = self._queue[i].get("title", "channel", "duration", "url")
            title = props["title"]
            channel = props["channel"]
            duration = props["duration"]["hh:mm:ss"]
            url = props["url"]["page"]
            pos = convert_to_equiv_emoji_digits(i + 1)

            embed.add_field(name=f"{pos} {title}", value=f"`📺 {channel}` | `🕒 {duration}` | [youtube]({url})", inline=False)
        
        return embed

class PlaylistError(Exception):
    def __init__(self, *args):
        self.message = args[0] if args else None

    def __str__(self):
        return f"PLAYLIST ERROR: {self.message}" if self.message else f"PLAYLIST ERROR has been raised!"