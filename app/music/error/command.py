from discord.ext import commands

class MusicCommandError(commands.CommandError):
    @classmethod
    def NotInAVoiceChannel(self):
        return self("Command Error", "You are not in a voice channel.", "warning")