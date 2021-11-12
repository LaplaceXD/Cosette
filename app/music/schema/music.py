import time, dacite
from typing import List
from discord import FFmpegPCMAudio
from dataclasses import dataclass, field

@dataclass(frozen=True)
class UrlData:
    download: str
    page: str

@dataclass(frozen=True)
class RequsterData:
    name: object
    channel: object

@dataclass(frozen=True)
class UploaderData:
    name: str
    url: str

@dataclass(frozen=True)
class StatsData:
    likes: int = field(default=0)
    views: int = field(default=0)

@dataclass(frozen=True)
class DurationData:
    seconds: int = field(default=0)

    @property
    def formatted(self):
        return time.strftime('%H:%M:%S', time.gmtime(self.seconds))

@dataclass(frozen=True)
class MusicSchema:
    title: str
    description: str
    channel: str
    thumbnail: str
    upload_date: str
    url: UrlData
    duration: DurationData
    uploader: UploaderData
    requester: RequsterData
    stats: StatsData
    tags: List[str] = field(default_factory=list)
    
    @property
    def source(self):
        return FFmpegPCMAudio(self.url.download, **{
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            "options": "-vn"
        })
    
    @classmethod
    def generate_schema(self, **kwargs):
        return dacite.from_dict(data_class=self, data={
            "title": kwargs.get("title"),
            "description": kwargs.get("description"),
            "duration": {
                "seconds": kwargs.get("duration"),
            },
            "channel": kwargs.get("channel"),
            "thumbnail": kwargs.get("thumbnail"),
            "url": {
                "page": kwargs.get("webpage_url"),
                "download": kwargs.get("formats")[0].get("url")
            },
            "stats": {
                "likes": kwargs.get("like_count"), 
                "views": kwargs.get("view_count")
            },
            "upload_date": kwargs.get("upload_date"),
            "uploader": {
                "name": kwargs.get("uploader"),
                "url": kwargs.get("uploader_url")
            },
            "requester": {
                "name": kwargs.get("ctx").author,
                "channel": kwargs.get("ctx").channel
            },
            "tags": kwargs.get("tags"),
        })