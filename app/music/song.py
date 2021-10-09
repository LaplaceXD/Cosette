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

    def get(self, *keys):
        data = {}
        for key in keys:
            if data:
                data[key] = self.__details[key]
            else:
                raise MusicError(f"{key.capitalize()} does not exist.")
        
        return data

    def get_details(self, simplified=True):
        fields = ["title", "channel", "duration", "thumbnail", "url", "like_count", "dislike_count"]
        return self.get(fields) if simplified else self.__details

    def generate_embed(self, header: str, simplified=False, color=0xff0059, icon_url=BOT_ICON_URL):
        fields = ["title", "url", "thumbnail", "channel", "like_count", "dislike_count"]
        embed_data = self.get(fields)

        embed = (Embed(title=embed_data.title, url=embed_data.display_url, color=color)
            .set_thumbnail(url=embed_data.thumbnail)
            .set_footer(text="Made with love by Laplace ❤️"))

        if header:
            embed.set_author(name=header, icon_url=icon_url)
        
        if not simplified:
             (embed.add_field(name="📺 Channel", value=embed_data.channel)
            .add_field(name="🕒 Duration", value=embed_data.duration, inline=False)
            .add_field(name="👍 Likes", value=embed_data.like_count)
            .add_field(name="👎 Dislikes", value=embed_data.dislike_count))

        return embed