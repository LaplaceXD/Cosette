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

    def generate_embed(self, header: str, simplified=False, color=0xff0059, icon_url=BOT_ICON_URL):
        title = self.__details["title"]
        display_url = self.__details["url"]["display"]
        thumbnail = self.__details["thumbnail"]

        embed = (Embed(title=title, url=display_url, color=color)
            .set_thumbnail(url=thumbnail)
            .set_footer(text="Made with love by Laplace ❤️"))

        if header:
            embed.set_author(name=header, icon_url=icon_url)
        
        if not simplified:
            channel = self.__details["channel"]
            duration = self.__details["duration"]
            likes = self.__details["like_count"]
            dislikes = self.__details["dislike_count"]

            (embed.add_field(name="📺 Channel", value=channel)
            .add_field(name="🕒 Duration", value=duration, inline=False)
            .add_field(name="👍 Likes", value=likes)
            .add_field(name="👎 Dislikes", value=dislikes))

        return embed

    def get(self, key: str):
        data = self.__details[key]
        if data:
            return data
        else:
            raise MusicError(f"{key.capitalize()} does not exist.")

    def get_details(self, simplified=True):
        if simplified:
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
            return self.__details