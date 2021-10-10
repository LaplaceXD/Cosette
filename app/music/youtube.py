class Youtube:
    def msg_format(self, music):
        data = music.get(*["channel", "title", "duration"])

        channel = data["channel"]
        title = data["title"]
        duration = data["duration"]["hh:mm:ss"]

        return f"[__{channel}__] **{title}** | (Duration: {duration})"