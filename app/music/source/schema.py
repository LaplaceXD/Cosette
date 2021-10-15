import time
from discord import FFmpegOpusAudio

class MusicSchema:
    FFMPEG_OPTIONS = {
        "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
        "options": "-vn"
    }

    def __init__(self, **kwargs):
        self.__title = kwargs.get("title")
        self.__description = kwargs.get("description")
        self.__duration = {
            "seconds": kwargs.get("duration") or 0,
            "hh:mm:ss": self.format_duration(int(kwargs.get("duration") or 0))
        }
        self.__channel = kwargs.get("channel")
        self.__thumbnail = kwargs.get("thumbnail")
        self.__url = {
            "page": kwargs.get("webpage_url"),
            "download": kwargs.get("formats")[0].get("url")
        }
        self.__stats = {
            "likes": kwargs.get("like_count") or 0,
            "dislikes": kwargs.get("dislike_count") or 0,
        }
        self.__upload_date = kwargs.get("upload_date")
        self.__uploader = {
            "name": kwargs.get("uploader"),
            "url": kwargs.get("uploader_url")
        }
        self.__requester = kwargs.get("requester")
        self.__tags = kwargs.get("tags") or []
        self.__source = self.create_codec_probe(kwargs.get("formats")[0].get("url"))

    @property
    def title(self):
        return self.__title

    @property
    def description(self):
        return self.__description
        
    @property
    def duration(self):
        return self.__duration

    @property
    def channel(self):
        return self.__channel

    @property
    def thumbnail(self):
        return self.__thumbnail

    @property
    def url(self):
        return self.__url

    @property
    def stats(self):
        return self.__stats

    @property
    def upload_date(self):
        return self.__upload_date

    @property
    def uploader(self):
        return self.__uploader

    @property
    def requester(self):
        return self.__requester

    @property
    def tags(self):
        return self.__tags

    @staticmethod
    def create_codec_probe(url: str):
        if not url:
            raise MusicSchema.MissingArgument("url")
        elif not url.startswith("http") or not url.startswith("https")
            raise MusicSchema("Invalid Url!")

        return FFmpegOpusAudio.from_probe(kwargs.get("source"), **self.FFMPEG_OPTIONS)

    @staticmethod
    def format_duration(seconds: int):
        if not seconds:
            raise MusicSchema.MissingArgument("seconds")

        return time.strftime('%H:%M:%S', time.gmtime(seconds))

class MusicSchema(Exception):
    def __init__(self, *args):
        self.message = args[0] if args else None

    def __str__(self):
        return f"MUSIC SCHEMA ERROR: {self.message}" if self.message else f"MUSIC SCHEMA ERROR has been raised!"

    @classmethod
    def MissingArgument(self, arg: str = ""):
        return self(f"{arg.capitalize()} is missing.")
