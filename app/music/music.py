from discord import FFmpegOpusAudio

from app.music.embed import MusicEmbed
from app.music.error.music import MusicError

class Music:
    def __init__(self, details: dict, audio_source: FFmpegOpusAudio):
        if not bool(details):
            raise MusicError("Details can not be empty.")
        elif not audio_source:
            raise MusicError("Audio source is required.")

        self.__source = audio_source
        self.__details = details

    def __str__(self):        
        title = self.__details["title"]
        channel = self.__details["channel"]
        duration = self.__details["duration"]["hh:mm:ss"]
        requester = self.__details["requester"]["author"].mention
        url = self.__details["url"]["page"]

        return f"{title} | `📺 {channel}` | `🕒 {duration}` | 🔥 {requester} | [youtube]({url})"

    @property
    def source(self):
        return self.__source

    @property
    def channel(self):
        return self.__details["requester"]["channel"]

    def get(self, *keys: str):
        data = {}
        for key in keys:
            if key:
                data[key] = self.__details[key]
            else:
                raise MusicError(f"{key.capitalize()} does not exist.")
        
        return data

    def get_details(self, simplified: bool = True):
        fields = ["title", "channel", "duration", "thumbnail", "url", "likes", "dislikes"]
        return self.get(*fields) if simplified else self.__details

    def embed(self, header: str, show_tags: bool = False, simplified: bool = False):
        requester = self.__details["requester"]["author"]

        embed = (MusicEmbed(title=self.__details["title"], url=self.__details["url"]["page"])
            .add_header(header=header)
            .set_thumbnail(url=self.__details["thumbnail"])
            .add_footer())
        
        if not simplified:
            channel = self.__details["channel"]
            channel_url = self.__details["uploader"]["url"]
            embed.add_fields({
                "📺 Channel": f"[{channel}]({channel_url})",
                "🔥 Requested By": requester.mention,
                "🕒 Duration": self.__details["duration"]["hh:mm:ss"],
                "👍 Likes": self.__details["stats"]["likes"],
                "👎 Dislikes": self.__details["stats"]["dislikes"]
            }, block=["🕒 Duration"])

        if show_tags and len(self.__details["tags"]) != 0:
            embed.add_tags(self.__details["tags"], name="🏷️ Tags", inline=False)

        return embed