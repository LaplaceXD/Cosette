from app.music.schema.music import MusicSchema
from app.music.embed import MusicEmbed

class Music(MusicSchema):
    def __str__(self):        
        title = self.title
        channel = self.channel
        duration = self.duration.formatted
        requester = self.requester.name.mention
        url = self.url.page

        return f"{title} | `📺 {channel}` | `🕒 {duration}` | 🔥 {requester} | [youtube]({url})"

    def embed(self, header: str, show_tags: bool = False, simplified: bool = False):
        embed = (MusicEmbed(title=self.title, url=self.url.page)
            .set_thumbnail(url=self.thumbnail)
            .add_header(header=header)
            .add_footer())
        
        if not simplified:
            channel = self.channel
            channel_url = self.uploader.url
            embed.add_fields({
                "📺 Channel": f"[{channel}]({channel_url})",
                "🔥 Requested By": self.requester.name.mention,
                "🕒 Duration": self.duration.formatted,
                "👍 Likes": self.stats.likes,
                "👀 Views": self.stats.views
            }, ["🕒 Duration"])

        if show_tags and len(self.tags) != 0:
            embed.add_tags(self.tags, name="🏷️ Tags", inline=False)

        return embed

class MusicError(Exception):
    def __init__(self, *args):
        self.message = args[0] if args else None

    def __str__(self):
        return f"MUSIC ERROR: {self.message}" if self.message else f"MUSIC ERROR has been raised!"