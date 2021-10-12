from discord.ext import commands

## LEVELS ##
#  error
#  warning
#  notice
class MusicCommandError(commands.CommandError):
    __levels = ["notice", "warning", "error"]

    def __init__(self, title: str = "Command Error", description: str = "An error occured.", type: str = __levels[2], *args):
        super().__init__(title, description, type, *args)
        self.__error_details = {
            "title": title,
            "description": description
        }
        self.__error_type = type
    
    @property
    def error(self):
        return self.__levels[2]

    @property
    def warning(self):
        return self.__levels[1]

    @property
    def notice(self):
        return self.__levels[0] 

    @property
    def type(self):
        return self.__error_type

    @property
    def details(self):
        return self.__error_details

    @classmethod
    def NotInAVoiceChannel(self, bot: bool = False):
        description = "I am not in a voice channel." if bot else "You are not in a voice channel."
        return self(description=description)

    @classmethod
    def BotAlreadyInChannel(self):
        return self(description="I am already in a voice channel.")