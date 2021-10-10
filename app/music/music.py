from discord import Embed, FFmpegOpusAudio
import time

EMBED_COLOR = 0xff0059
BOT_ICON_URL = "https://cdn.discordapp.com/attachments/797083893014462477/896312760084889600/unknown.png"
class Music:
    def __init__(self, details: dict, audio_source: FFmpegOpusAudio):
        if not bool(details):
            raise MusicError("Details can not be empty.")
        elif not audio_source:
            raise MusicError("Audio source is required.")

        self.__source = audio_source
        self.__details = details

    def source(self):
        return self.__source

    def get(self, *keys):
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

    def create_embed(self, header: str, color: int = EMBED_COLOR, icon_url: str = BOT_ICON_URL, show_tags: bool = False, simplified: bool = False):
        requester = self.__details["requester"]

        embed = (Embed(title=self.__details["title"], url=self.__details["url"]["page"], color=color)
            .set_thumbnail(url=self.__details["thumbnail"])
            .set_footer(text="Made with love by Laplacé#0702 ❤️"))

        if header:
            embed.set_author(name=header, icon_url=icon_url)
        
        if not simplified:
             (embed.add_field(name="📺 Channel", value=self.__details["channel"])
            .add_field(name="🔥 Requested By", value=requester.mention)
            .add_field(name="🕒 Duration", value=self.__details["duration"]["hh:mm:ss"], inline=False)
            .add_field(name="👍 Likes", value=self.__details["stats"]["likes"])
            .add_field(name="👎 Dislikes", value=self.__details["stats"]["dislikes"]))

        if show_tags and len(self.__details["tags"]) != 0:
            tagStr = ""
            for tag in self.__details["tags"]:
                tagStr += f"`{tag}`, " 
            embed.add_field(name="🏷️ Tags", value=tagStr[:-2], inline=False)

        return embed

class MusicError(Exception):
    def __init__(self, *args):
        self.message = args[0] if args else None

    def __str__(self):
        return f"MUSIC ERROR: {self.message}" if self.message else f"MUSIC ERROR has been raised!"