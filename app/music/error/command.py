from discord.ext import commands

class MusicCommandError(commands.CommandError):
    __levels = ["notice", "warning", "error"]

    def __init__(self, title: str = "Command Error", description: str = "An error occured.", error_type: str = __levels[2], *args):
        super().__init__(title, description, type, *args)
        self.__error_details = {
            "title": title,
            "description": description
        }
        self.__error_type = error_type
    
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
        return self("Voice Channel", description, self.warning)

    @classmethod
    def BotAlreadyInVoiceChannel(self):
        return self("Voice Channel", "I am already in a voice channel.", self.warning)

    @classmethod
    def UnplayableTrack(self):
        return self("🙇 I can't play this music", "Try changing your keywords, or be more specific.", self.notice)

    @classmethod
    def MissingPlayQuery(self):
        return self("🤔 What to play?", "You must add a url or a search item after the command.", self.notice)

    @classmethod
    def NotCurrentlyPlaying(self):
        return self("No Track Currently Playing", "Maybe you can add some songs?", self.notice)

    @classmethod
    def MusicAlreadyPlaying(self):
        return self("Music is already playing", "What do you want me to do?!", self.notice)

    @classmethod
    def MusicAlreadyPaused(self):
        return self("Music is already paused", "What do you want me to do?!", self.notice)

    @classmethod
    def EmptyQueue(self):
        return self("Empty Queue", "There are currently no music on queue. Add one?", self.notice)

    @classmethod
    def OutOfRange(self, item: str):
        return self(f"{item.capitalize()} out of range ", "It's not that big.", self.notice)
