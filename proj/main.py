from utils import VideoTranscriber

API_KEY = "your-openai-api-key"
VIDEO_URL = "https://www.youtube.com/watch?v=2lAe1cqCOXo"

transcriber = VideoTranscriber(API_KEY)
print(transcriber.title)
transcript, title = transcriber.process_youtube_video(VIDEO_URL)

# Now that transcript and title are defined, you can save them
with open(f"{title}.txt", "w", encoding="utf-8") as f:
    f.write(transcript)

print(f"Transcript saved as {title}.txt")