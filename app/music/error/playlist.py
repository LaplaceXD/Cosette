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