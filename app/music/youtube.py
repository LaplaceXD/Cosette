import urllib
import re
import time

class Youtube:
    def generate_schema(self, url, data):
        return {
            "title": data["title"], 
            "duration": data["duration"],
            "url": url,
            "channel": data["channel"],
            "like_count": data["like_count"],
            "dislike_count": data["dislike_count"],
            "download_url": data['formats'][0]['url'],
            "thumbnail": data["thumbnail"]
        }

    def msg_format(self, data):
        channel = data["channel"]
        title = data["title"]
        duration = int(data["duration"])

        return f"[__{channel}__] **{title}** | (Duration: {time.strftime('%H:%M:%S', time.gmtime(duration))})"