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

    BOT_ICON_URL = "https://cdn.discordapp.com/attachments/797083893014462477/897143609374146600/unknown.png"
    FOOTER = "Made with love by Laplacé#0702 ❤️"

    def __init__(self, embed_type: str = "NORMAL", title: str = "", **kwargs):
        if not embed_type.lower() in self.PROPS:
            raise MusicEmbedError(f"The Embed type, {embed_type.upper()} was not found.")

        props = self.PROPS.get(embed_type.lower())
        color = props.get("color")
        emoji = props.get("emoji")
        super().__init__(color=color, title=f"{emoji}{title}", **kwargs)

    def add_header(self, header: str = "", icon_url: str = BOT_ICON_URL):
        super().set_author(name=header, icon_url=icon_url)
        return self
    
    def add_footer(self):
        super().set_footer(text=self.FOOTER)
        return self

    def add_tags(self, tags, **kwargs):
        tagStr = ""
        for tag in tags:
            tagStr += f"`{tag}`, "
        super().add_field(value=tagStr[:-2], **kwargs)
        return self

class MusicEmbedError(Exception):
    def __init__(self, *args):
        self.message = args[0] if args else None

    def __str__(self):
        return f"MUSIC EMBED ERROR: {self.message}" if self.message else f"MUSIC EMBED ERROR has been raised!"