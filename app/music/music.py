from discord import Embed, FFmpegOpusAudio
from app.utils import extract_json

bot_properties = extract_json("properties")
EMBED_COLOR = int(bot_properties["COLORS"]["MUSIC"], 16)
BOT_ICON_URL = bot_properties["BOT_ICON_URL"]
FOOTER_TEXT = bot_properties["FOOTER"]

class Music:
    def __init__(self, details: dict, audio_source: FFmpegOpusAudio):
        if not bool(details):
            raise MusicError("Details can not be empty.")
        elif not audio_source:
            raise MusicError("Audio source is required.")

        self.__source = audio_source
        self.__details = details

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

    def create_embed(self, header: str, color: int = EMBED_COLOR, icon_url: str = BOT_ICON_URL, show_tags: bool = False, simplified: bool = False):
        requester = self.__details["requester"]["author"]

        embed = (Embed(title=self.__details["title"], url=self.__details["url"]["page"], color=color)
            .set_thumbnail(url=self.__details["thumbnail"])
            .set_footer(text=FOOTER_TEXT))

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