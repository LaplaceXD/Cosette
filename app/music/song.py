class MusicError(Exception):
    def __init__(self, *args):
        self.message = args[0] if args else None

    def __str__(self):
        return f"MUSIC ERROR: {self.message}" if self.message else f"MUSIC ERROR has been raised!"


class Music:
    def __init__(self, details, url):
        self.__details = details
        self.__url
    
    def get_details(self, format="simplified"):
        if format == "verbose":
            return self.__details
        elif format == "simplified":
            return {
                "title": self.__details["title"], 
                "duration": self.__details["duration"],
                "url": self.__details["url"],
                "download_url": self.__details['formats'][0]['url'],
                "channel": self.__details["channel"],
                "like_count": self.__details["like_count"],
                "dislike_count": self.__details["dislike_count"],
                "thumbnail": self.__details["thumbnail"]
            }
        else:
            raise MusicError("Invalid Argument Exception in Music.get_details method.")