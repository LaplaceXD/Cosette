import time

class Youtube:

    def msg_format(self, data):
        channel = data["channel"]
        title = data["title"]
        duration = int(data["duration"])

        return f"[__{channel}__] **{title}** | (Duration: {time.strftime('%H:%M:%S', time.gmtime(duration))})"