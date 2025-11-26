from youtube_transcript_api import YouTubeTranscriptApi
import sys

video_id = "jNQXAC9IVRw" # Me at the zoo (short video)

print("Attempting YouTubeTranscriptApi.list...")
try:
    transcripts = YouTubeTranscriptApi.list(video_id)
    print(f"List success: {transcripts}")
except Exception as e:
    print(f"List failed: {e}")

print("\nAttempting YouTubeTranscriptApi.fetch...")
try:
    transcript = YouTubeTranscriptApi.fetch(video_id)
    print(f"Fetch success: {transcript[:50]}...")
except Exception as e:
    print(f"Fetch failed: {e}")
