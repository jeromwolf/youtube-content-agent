import youtube_transcript_api
from youtube_transcript_api import YouTubeTranscriptApi

print(f"Module dir: {dir(youtube_transcript_api)}")
print(f"Class dir: {dir(YouTubeTranscriptApi)}")

try:
    print(f"Type of YouTubeTranscriptApi: {type(YouTubeTranscriptApi)}")
except:
    pass
