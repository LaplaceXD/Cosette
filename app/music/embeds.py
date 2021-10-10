from discord import Embed
from discord.ext import commands

class Embeds(Embed):
    COLORS = {
        "NORMAL": 0xff0059,
        "WARNING": 0xfbff2b,
        "NOTICE": 0x00bbff
    }
    EMOJIS = {
        "WARNING": "⚠️ ",
        "NOTICE": "📢 ",
        "NORMAL": ""
    }

    BOT_ICON_URL = "https://cdn.discordapp.com/attachments/797083893014462477/896312760084889600/unknown.png"
    FOOTER = "Made with love by Laplacé#0702 ❤️"

    def __create_embed(self, header: str = "", show_footer: bool = True, footer_text: str = FOOTER, icon_url: str = BOT_ICON_URL, **kwargs):
        self.__embed = Embed(**kwargs)
        if header:
            self.__embed.set_author(name=header, icon_url=icon_url)
        if show_footer:
            self.__embed.set_footer(text=footer_text)

    def send_embed(self, ctx: commands.Context, **kwargs):
        return ctx.send(embed=self.__embed, **kwargs)

    def get_embed(self):
        return self.__embed

    def simple(self, header: str, msg: str, embed_type: str = "NORMAL"):
        emoji = self.EMOJIS.get(embed_type)
        color = self.COLORS.get(embed_type)

        params = {
            "header": f"{emoji}{header}",
            "icon_url": "",
            "description": msg,
            "color": color,
            "show_footer": False
        }

        self.__create_embed(**params)
        return self