import asyncio, itertools, random, math

from app.utils.misc import convert_to_equiv_emoji_digits
from app.music.music import Music
from app.music.embed import MusicEmbed
      
class Playlist(asyncio.Queue):
    def __init__(self, music_list: list=[], **kwargs):
        super().__init__(**kwargs)
        self.__page_queue = music_list # creates own list if its a pagination
        self.__pagination_details = {"prev_page": "None", "next_page": "None", "start_at": 0, "curr_page": 1}

    def __getitem__(self, index: int or slice):
        queue = self.__page_queue or self._queue
        if isinstance(index, slice):
            item = Playlist(list(itertools.islice(queue, index.start, index.stop, index.step)))
        elif isinstance(index, int):
            idx = PlaylistError.check_index(index, self.size)
            item = queue[idx]
        else:
            raise PlaylistError("Index type should be of type int or slice.")

        return item

    @property
    def pagination_details(self):
        return self.__pagination_details

    @pagination_details.setter
    def pagination_details(self, value: dict = {}):
        if not value:
            raise PlaylistError("Pagination details must be set!")
        self.__pagination_details = value

    @property
    def size(self):
        return len(self.__page_queue or self._queue)

    def next(self):
        return self.get()

    def shuffle(self):
        random.shuffle(self._queue)

    def add(self, music: Music):
        return self.put(music)

    def remove(self, index: int):
        idx = PlaylistError.check_index(index, self.size)

        music = self._queue[idx]
        del self._queue[idx]
        return music

    def clear(self):
        return self._queue.clear()

    def paginate(self, size: int = 0, page: int = 1):
        queue = self
        if size < 0:
            raise PlaylistError("Size of pagination can not be negative.")
        
        max_page = 1 if self.size <= size or size == 0 else math.ceil(self.size / size)
        if page > max_page or page < 1:
            raise PlaylistError("Page out of range.")
        else:
            start = (page - 1) * size
            stop = page * size
            
            queue = self[start:stop]
            queue.pagination_details = {
                "prev_page": page - 1 if page > 1 else "None",
                "next_page": page + 1 if stop + size <= self.size else "None",
                "start_at": start,
                "curr_page": page,
            }

        return queue
    
    def embed(self):
        if self.size == 0:
            raise PlaylistError("Did you mean to create an empty embed for playlist instead?")
        
        embed = (MusicEmbed(title="", description="Here are the list of songs that are currently on queue.")
            .add_header(header="🎶 Music Queue")
            .add_footer())
        
        # add music queued fields
        for i in range(self.size):
            music = str(self[i])
            details = music.split("|")

            title = str(details[0]).strip()
            desc = "|".join(details[1:]).strip()
            music_number = convert_to_equiv_emoji_digits(self.__pagination_details["start_at"] + i + 1)
            
            embed.add_field(name=f"{music_number} {title}", value=desc, inline=False)

        embed.add_fields({
            "⏮️ Prev Page": self.__pagination_details["prev_page"],
            "Current Page": self.__pagination_details["curr_page"],
            "Next Page ⏭️": self.__pagination_details["next_page"]
        })

        return embed

class PlaylistError(Exception):
    def __init__(self, *args):
        self.message = args[0] if args else None

    def __str__(self):
        return f"PLAYLIST ERROR: {self.message}" if self.message else f"PLAYLIST ERROR has been raised!"

    @classmethod
    def check_index(self, index: int, length: int = 0):
        if index < 0:
            index += length
        if index >= length or index < 0:
            raise self("Index out of range!")

        return index