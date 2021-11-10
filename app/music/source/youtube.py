import youtube_dl
import urllib, re
import os
from discord.ext import commands

from app.music.music import Music

class YoutubeDLSource():
    __ytdl_options__ = {
        "format": "bestaudio/best",
        "extractaudio": True,
        "audioformat": "mp3",
        "outtmpl": "%(id)s-%(title)s.%(ext)s",
        "restrictfilenames": True,
        "noplaylist": True,
        "nocheckcertificate": True,
        "ignoreerrors": False,
        "logtostderr": False,
        "quiet": True,
        "verbose": True,
        "no_warnings": True,
        "default_search": "auto",
        "source_address": "0.0.0.0",
        "cookiefile": os.getcwd() + "/cache/cookies.txt"
    }
    
    __ytdl__ = youtube_dl.YoutubeDL(__ytdl_options__)

    @classmethod
    def get_music(self, query: str, ctx: commands.Context):
        if not query:
            raise YoutubeDLSourceError("Query string is required to obtain Music.")

        url = query if query.startswith("https") else self.search(query)
        data = self.__ytdl__.extract_info(url, download=False)
        return Music.generate_schema(**data, ctx=ctx)

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