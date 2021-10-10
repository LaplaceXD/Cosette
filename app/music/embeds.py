from discord import Embed

class Embeds(Embed):
    COLORS =  {
        "MUSIC": 0xff0059,
        "WARNING": 0xfbff2b,
        "NOTICE": 0x00bbff
    }
    BOT_ICON_URL = "https://cdn.discordapp.com/attachments/797083893014462477/896312760084889600/unknown.png"
    FOOTER = "Made with love by Laplacé#0702 ❤️"

    def __create_embed(self, header: str = "", show_footer: bool = True, footer_text: str = FOOTER, icon_url: str = BOT_ICON_URL, **kwargs):
        self.__embed = Embed(**kwargs)
        if header:
            self.__embed.set_author(name=header, icon_url=icon_url)
        if show_footer:
            self.__embed.set_footer(text=footer_text)

    def get_embed(self):
        return self.__embed

    def warning(self, error_type: str, error: Exception):
        params = {
            "header": f"⚠️ {error_type}",
            "icon_url": "",
            "description": str(error),
            "color": self.COLORS["WARNING"],
            "show_footer": False
        }

        self.__create_embed(**params)
        return self
