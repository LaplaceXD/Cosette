from discord import Embed

class MusicEmbed(Embed):
    PROPS = {
        "normal": {
            "color": 0xff0059,
            "emoji": "",
        }, 
        
        "warning": {
            "color": 0xfbff2b,
            "emoji": "⚠️",
        }, 
        "notice": {
            "color": 0x00bbff,
            "emoji": "📢 ",
        }
    }

    BOT_ICON_URL = "https://cdn.discordapp.com/attachments/797083893014462477/896312760084889600/unknown.png"
    FOOTER = "Made with love by Laplacé#0702 ❤️"

    def __init__(self, embed_type: str = "NORMAL", **kwargs):
        if not embed_type in self.PROPS:
            raise MusicEmbedError(f"The Embed type, {embed_type.upper()} was not found.")

        super().__init__(color=self.COLORS.get(embed_type.lower()), **kwargs)

    def add_header(self, header: str = "", icon_url: str = BOT_ICON_URL):
        super().set_author(name=header, icon_url=icon_url)
        return self

class MusicEmbedError(Exception):
    def __init__(self, *args):
        self.message = args[0] if args else None

    def __str__(self):
        return f"MUSIC EMBED ERROR: {self.message}" if self.message else f"MUSIC EMBED ERROR has been raised!"