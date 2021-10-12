from discord import Embed

class MusicEmbed(Embed):
    __props = {
        "notice": {
            "color": 0xff0059,
            "emoji": "",
        }, 
        "warning": {
            "color": 0xfbff2b,
            "emoji": "⚠️",
        }, 
        "error": {
            "color": 0xff122a,
            "emoji": "❗",
        }
    }

    __default_title = "Place your advertisement here!"
    __bot_icon_url = "https://cdn.discordapp.com/attachments/797083893014462477/897143609374146600/unknown.png"
    __footer = "Made with love by Laplacé ❤️"

    def __init__(self, color: int = __props["notice"]["color"], title: str = __default_title, **kwargs):
        super().__init__(color=color, title=f"{title}", **kwargs)

    def add_header(self, header: str = "", icon_url: str = __bot_icon_url):
        self.set_author(name=header, icon_url=icon_url)
        return self
    
    def add___footer(self):
        self.set___footer(text=self.__footer)
        return self

    def add_fields(self, fields: dict = {}, block: list or bool = False):
        for field in fields:
            self.add_field(
                name=field,
                value=fields[field],

                # checks whether the block is bool if it is then every field is 
                # displayed as block or inline, else if it is a list then the ones in
                # the list would be displayed as block
                inline=not field in block if isinstance(block, list) else block
            )
        return self

    def add_tags(self, tags, **kwargs):
        tagStr = ""
        for tag in tags:
            tagStr += f"`{tag}`, "
        self.add_field(value=tagStr[:-2], **kwargs)
        return self

    @classmethod
    def warning(self, title: str = __default_title, **kwargs):
        color = self.__props["warning"]["color"]
        emoji = self.__props["warning"]["emoji"]

        return self(title=f"{emoji} {title}", color=color, **kwargs)

    @classmethod
    def error(self, title: str = __default_title, **kwargs):
        color = self.__props["error"]["color"]
        emoji = self.__props["error"]["emoji"]

        return self(title=f"{emoji} {title}", color=color, **kwargs)