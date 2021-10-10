import discord
import youtube_dl
import urllib, re
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
    
    def __init__(self):
        self.__ytdl = youtube_dl.YoutubeDL(self.YTDL_OPTIONS)

    # add schema here

    def get_music(self, query: str):
        url = query if query.startswith("$https") else self.search(query)
        data = self.__ytdl.extract_info(url, download=False)
        data["url"] = {
            "display": url,
            "download": data["formats"][0]["url"]
        }

        source = discord.FFmpegPCMAudio(data["url"]["download"], **self.FFMPEG_OPTIONS)
        return Music(data, source)

    def search(self, query: str):
        query_string = urllib.parse.urlencode({ "search_query": query })
        htm_content = urllib.request.urlopen(
            "http://www.youtube.com/results?" + query_string
        )
        search_results = re.findall("\\/watch\\?v=(.{11})", htm_content.read().decode())

        return "https://www.youtube.com/watch?v=" + search_results[0]


    