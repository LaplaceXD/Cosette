class YoutubeDLSourceError(Exception):
    def __init__(self, *args):
        self.message = args[0] if args else None

    def __str__(self):
        return f"YTDL SOURCE ERROR: {self.message}" if self.message else f"YTDL SOURCE ERROR has been raised!"