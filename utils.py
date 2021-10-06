import math
import urllib
import re

def search(searchStr):
    query_string = urllib.parse.urlencode({ "search_query": searchStr })
    htm_content = urllib.request.urlopen(
        "http://www.youtube.com/results?" + query_string
    )

    search_results = re.findall("\\/watch\\?v=(.{11})", htm_content.read().decode())
    
    return "https://www.youtube.com/watch?v=" + search_results[0]

def extract_youtube_data(url, data): 
    return {
        "title": data["title"],
        "duration": data["duration"],
        "url": url,
        "channel": data["channel"],
        "like_count": data["like_count"],
        "dislike_count": data["dislike_count"],
        "download_url": data['formats'][0]['url']
    }

def format_youtube_data(data):
    duration = int(data["duration"])
    minutes = math.floor(duration / 60)
    seconds = duration - (minutes * 60)

    channel = data["channel"]
    title = data["title"]

    return f"[__{channel}__] **{title}** | (Duration: {minutes}:{seconds})"