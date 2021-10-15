from app.music.source.schema import MusicSchema
from app.music.embed import MusicEmbed

class Music(MusicSchema):
    def __str__(self):        
        title = self.title
        channel = self.channel
        duration = self.duration["hh:mm:ss"]
        requester = self.requester.get("name").mention
        url = self.url.get("page")

        return f"{title} | `📺 {channel}` | `🕒 {duration}` | 🔥 {requester} | [youtube]({url})"

    def embed(self, header: str, show_tags: bool = False, simplified: bool = False):
        embed = (MusicEmbed(title=self.title, url=self.url.get("page"))
            .set_thumbnail(url=self.thumbnail)
            .add_header(header=header)
            .add_footer())
        
        if not simplified:
            channel = self.channel
            channel_url = self.uploader.get("url")
            embed.add_fields({
                "📺 Channel": f"[{channel}]({channel_url})",
                "🔥 Requested By": self.requester.get("name").mention,
                "🕒 Duration": self.duration.get("hh:mm:ss"),
                "👍 Likes": self.stats.get("likes"),
                "👎 Dislikes": self.stats.get("dislikes")
            }, ["🕒 Duration"])

        if show_tags and len(self.tags) != 0:
            embed.add_tags(self.tags, name="🏷️ Tags", inline=False)

        return embed

class MusicError(Exception):
    def __init__(self, *args):
        self.message = args[0] if args else None

    def __str__(self):
        return f"MUSIC ERROR: {self.message}" if self.message else f"MUSIC ERROR has been raised!"