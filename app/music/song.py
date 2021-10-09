from discord import Embed

class MusicError(Exception):
    def __init__(self, *args):
        self.message = args[0] if args else None

    def __str__(self):
        return f"MUSIC ERROR: {self.message}" if self.message else f"MUSIC ERROR has been raised!"


BOT_ICON_URL = "https://cdn.discordapp.com/attachments/797083893014462477/896312760084889600/unknown.png"

class Music:
    def __init__(self, details: object):
        self.__details = details

    def generate_embed(self, color=0xff0059, icon_url=BOT_ICON_URL):
        title = self.__details["title"]
        display_url = self.__details["url"]["display"]
        thumbnail = self.__details["thumbnail"]
        channel = self.__details["channel"]
        duration = self.__details["duration"]
        likes = self.__details["like_count"]
        dislikes = self.__details["dislike_count"]

        return (Embed(title=title, url=display_url, color=color)
            .set_author(name="▶️ Now playing!", icon_url=icon_url)
            .set_thumbnail(url=thumbnail)
            .add_field(name="📺 Channel", value=channel)
            .add_field(name="🕒 Duration", value=duration, inline=False)
            .add_field(name="👍 Likes", value=likes)
            .add_field(name="👎 Dislikes", value=dislikes)
            .set_footer(text="Made with love by Laplace ❤️"))
    
    def get_details(self, format="simplified"):
        if format == "verbose":
            return self.__details
        elif format == "simplified":
            return {
                "title": self.__details["title"], 
                "channel": self.__details["channel"],
                "duration": self.__details["duration"],
                "thumbnail": self.__details["thumbnail"]
                "url": {
                    "display": self.__details["display_url"],
                    "download": self.__details["download_url"] # ["formats"][0]["url"]
                },
                "likes": self.__details["like_count"],
                "dislikes": self.__details["dislike_count"],
            }
        else:
            raise MusicError("Invalid Argument Exception in Music.get_details method.")