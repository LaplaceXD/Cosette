from discord import Embed

from app.music.schema.embedlevel import LevelsSchema, EmbedLevelsData, DefaultsData

class MusicEmbed(Embed):
    embed_levels = EmbedLevelsData(
        notice=LevelsSchema(0xff0059, ""),
        warning=LevelsSchema(0xfbff2b, "⚠️"),
        error=LevelsSchema(0xff122a, "❗"),
    )
    
    defaults = DefaultsData(
        title="Place your advertisement here!",
        icon_url="https://cdn.discordapp.com/attachments/797083893014462477/897143609374146600/unknown.png",
        description="",
        footer="Made with love by Laplacé ❤️"
    )

    def __init__(self, color: int = embed_levels.notice.color, title: str = defaults.title, **kwargs):
        super().__init__(color=color, title=f"{title}", **kwargs)

    def add_header(self, header: str = "", icon_url: str = defaults.icon_url):
        self.set_author(name=header, icon_url=icon_url)
        return self
    
    def add_footer(self, text: str = defaults.footer):
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
    def warning(self, title: str = defaults.title, **kwargs):
        color = self.embed_levels.warning.color
        emoji = self.embed_levels.warning.emoji

        return self(title=f"{emoji} {title}", color=color, **kwargs)

    @classmethod
    def error(self, title: str = defaults.title, **kwargs):
        color = self.embed_levels.error.color
        emoji = self.embed_levels.error.emoji

        return self(title=f"{emoji} {title}", color=color, **kwargs)