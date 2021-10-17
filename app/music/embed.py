from discord import Embed

from dataclasses import dataclass
from app.music.schema.embedlevel import EmbedLevelScehma

@dataclass(frozen=True)
class EmbedData:
    notice: EmbedLevelScehma = EmbedLevelScehma(0xff0059, "")
    warning: EmbedLevelScehma = EmbedLevelScehma(0xfbff2b, "⚠️")
    erro: EmbedLevelScehma = EmbedLevelScehma(0xff122a, "❗")

class MusicEmbed(Embed):
    __embed_levels__ = EmbedData()
    __title__="Place your advertisement here!",
    __icon_url__="https://cdn.discordapp.com/attachments/797083893014462477/897143609374146600/unknown.png",
    __footer__="Made with love by Laplacé ❤️"

    def __init__(self, color: int = __embed_levels__.notice.color, title: str = __title__, **kwargs):
        super().__init__(color=color, title=f"{title}", **kwargs)

    def add_header(self, header: str = "", icon_url: str = __icon_url__):
        self.set_author(name=header, icon_url=icon_url)
        return self
    
    def add_footer(self, text: str = __footer__):
        self.set_footer(text=text)
        return self

    def add_fields(self, fields: dict = {}, inline: list = []):
        for field in fields:
            self.add_field(
                name=field,
                value=fields[field],

                # checks whether the block is bool if it is then every field is 
                # displayed as block or inline, else if it is a list then the ones in
                # the list would be displayed as block
                inline=not field in inline
            )
        return self

    def add_tags(self, tags, **kwargs):
        tagStr = ""
        for tag in tags:
            tagStr += f"`{tag}`, "
        self.add_field(value=tagStr[:-2], **kwargs)
        return self

    @classmethod
    def warning(self, title: str = __title__, **kwargs):
        color = self.__embed_levels__.warning.color
        emoji = self.__embed_levels__.warning.emoji

        return self(title=f"{emoji} {title}", color=color, **kwargs)

    @classmethod
    def error(self, title: str = __title__, **kwargs):
        color = self.__embed_levels__.error.color
        emoji = self.__embed_levels__.error.emoji

        return self(title=f"{emoji} {title}", color=color, **kwargs)