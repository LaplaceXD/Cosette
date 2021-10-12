import discord
import youtube_dl
import urllib, re, time
from discord.ext import commands

from app.music.music import Music

class YoutubeDLSource():
    YTDL_OPTIONS = {
        "format": "bestaudio/best",
        "extractaudio": True,
        "audioformat": "mp3",
        "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
        "restrictfilenames": True,
        "noplaylist": True,
        "nocheckcertificate": True,
        "ignoreerrors": False,
        "logtostderr": False,
        "quiet": True,
        "no_warnings": True,
        "default_search": "auto",
        "source_address": "0.0.0.0",
    }

    FFMPEG_OPTIONS = {
        "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
        "options": "-vn"
    }
    
    __ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

    def get_music(self, query: str, requester: commands.Context):
        if not query:
            raise YoutubeDLSourceError("Query string is required to obtain Music.")

        url = query if query.startswith("$https") else self.search(query)
        data = self.__ytdl.extract_info(url, download=False)
        details = self.__generate_music_schema({ **data, "requester": requester })
        source = discord.FFmpegPCMAudio(details["url"]["download"], **self.FFMPEG_OPTIONS)
        return Music(details, source)

    def __generate_music_schema(self, data: dict):
        if not bool(data):
            raise YoutubeDLSourceError("Data should be supplied to generate music schema.")

        return {
            "title": data["title"], 
            "description": data["description"],
            "duration": {
                "seconds": data["duration"],
                "hh:mm:ss": self.format_duration(int(data["duration"]))
            },
            "channel": data["channel"],
            "thumbnail": data["thumbnail"],
            "url": {
                "page": data["webpage_url"],
                "download": data["formats"][0]["url"]
            },
            "stats": {
                "likes": data["like_count"],
                "dislikes": data["dislike_count"],
            },
            "upload_data": data["upload_date"],
            "uploader": {
                "name": data["uploader"],
                "url": data["uploader_url"]
            },
            "requester": {
                "author": data["requester"].author,
                "channel": data["requester"].channel
            },
            "tags": data["tags"],
        }

    @staticmethod
    def format_duration(seconds: int):
        if not seconds:
            raise YoutubeDLSourceError("The number of seconds is required for formatting duration.")

        return time.strftime('%H:%M:%S', time.gmtime(seconds))

    @staticmethod
    def search(query: str):
        if not query:
            raise YoutubeDLSourceError("Query string is required for searching")

        query_string = urllib.parse.urlencode({ "search_query": query })
        htm_content = urllib.request.urlopen(
            "http://www.youtube.com/results?" + query_string
        )
        search_results = re.findall("\\/watch\\?v=(.{11})", htm_content.read().decode())

        return "https://www.youtube.com/watch?v=" + search_results[0]

class YoutubeDLSourceError(Exception):
    def __init__(self, *args):
        self.message = args[0] if args else None

    def __str__(self):
        return f"YTDL SOURCE ERROR: {self.message}" if self.message else f"YTDL SOURCE ERROR has been raised!"