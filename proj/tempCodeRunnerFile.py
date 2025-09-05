from utils.transcriber import VideoTranscriber

API_KEY = "your-openai-api-key"
VIDEO_URL = "https://youtu.be/4WVZBtqqVM4?si=vRx0j243Y6fhievt"

transcriber = VideoTranscriber(API_KEY)
transcript, title = transcriber.process_youtube_video(VIDEO_URL)

print(f"Title: {title}")
print("Transcript:")
print(transcript)