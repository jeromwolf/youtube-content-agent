from youtube_transcript_api import YouTubeTranscriptApi

video_id = "jNQXAC9IVRw"

print("Attempting instantiation...")
try:
    api = YouTubeTranscriptApi()
    print("Instantiation success")
    
    print("Attempting api.list(video_id)...")
    try:
        transcripts = api.list(video_id)
        print(f"List success: {transcripts}")
    except Exception as e:
        print(f"List failed: {e}")

    print("Attempting api.fetch(video_id)...")
    try:
        transcript = api.fetch(video_id)
        print(f"Fetch success: {transcript[:50]}...")
    except Exception as e:
        print(f"Fetch failed: {e}")

except Exception as e:
    print(f"Instantiation failed: {e}")
