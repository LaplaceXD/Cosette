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

    def paginate(self, size: int, page: int):
        if self.qsize() <= size or size == 0:
            return self._queue
        
        start = (page - 1) * size
        end = (page) * size
        self.__page = page
        return self[start:end]

    def create_embed(self, size: int = 0, page: int = 0):
        queue = self.paginate(size, page)
        size = len(queue)
        prev_pages_items = (page - 1) * size
        prev_page = page - 1 if page != 0 else "None"
        next_page = page + 1 if prev_pages_items + size > self.qsize() else "None"

        if size == 0:
            description = "There are currently no music on queue. Add one?"
        else:
            description = "Here are the list of songs that are currently on queue."

        embed = MusicEmbed(description=description).add_header(header="🎶 Music Queue").add_footer()

        for i in range(size):
            props = queue[i].get("title", "channel", "duration", "url", "requester")
            title = props["title"]
            channel = props["channel"]
            duration = props["duration"]["hh:mm:ss"]
            requester = props["requester"]["author"].mention
            url = props["url"]["page"]
            pos = convert_to_equiv_emoji_digits(i + 1 + prev_pages_items)

            embed.add_field(name=f"{pos} {title}", value=f"`📺 {channel}` | `🕒 {duration}` | 🔥 {requester} | [youtube]({url})", inline=False)
        
        embed.add_field(name="⏮️ Prev Page", value=f"{prev_page}")
        embed.add_field(name="Current Page", value=f"{page}")
        embed.add_field(name="Next Page ⏭️", value=f"{next_page}")

        return embed

class PlaylistError(Exception):
    def __init__(self, *args):
        self.message = args[0] if args else None

    def __str__(self):
        return f"PLAYLIST ERROR: {self.message}" if self.message else f"PLAYLIST ERROR has been raised!"