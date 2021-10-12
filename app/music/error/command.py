from discord.ext import commands

## LEVELS ##
#  error
#  warning
#  notice
class MusicCommandError(commands.CommandError):
    def __init__(self, title: str = "Command Error", description: str = "An error occured.", type: str = "warning", *args):
        super().__init__(title, description, type, *args)
        self.__error_details = {
            "title": title,
            "description": description
        }
        self.__error_type = type

    @property
    def type(self):
        return self.__error_type

    @property
    def details(self):
        return self.__error_details

    @classmethod
    def NotInAVoiceChannel(self):
        return self("Command Error", "You are not in a voice channel.")