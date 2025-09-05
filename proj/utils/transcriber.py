# utils/transcriber.py
import os
from pytube import YouTube
import openai

# Try to import moviepy, but handle gracefully if it fails
try:
    from moviepy.editor import VideoFileClip
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False
    print("Warning: moviepy not available. Audio extraction will be limited.")

class VideoTranscriber:
    def __init__(self, api_key):
        self.client = openai.OpenAI(api_key=api_key)
        
    def download_youtube_video(self, url, output_path="temp"):
        """Download a YouTube video and return the file path and title."""
        os.makedirs(output_path, exist_ok=True)
        try:
            yt = YouTube(url)
            video = yt.streams.filter(progressive=True, file_extension="mp4").first()
            if not video:
                raise ValueError("No suitable video stream found.")
            video_path = video.download(output_path)
            return video_path, yt.title
        except Exception as e:
            print(f"[Download Error] {e}")
            raise
     
    def extract_audio(self, video_path, output_path="temp"):
        """Extract audio from video file."""
        if not MOVIEPY_AVAILABLE:
            raise ImportError("moviepy is required for audio extraction. Please install it with: pip install moviepy")
        
        audio_path = os.path.join(output_path, "audio.mp3")
        try:
            video = VideoFileClip(video_path)
            video.audio.write_audiofile(audio_path)
            video.close()  # Properly close the video file
            return audio_path
        except Exception as e:
            print(f"[Audio Extraction Error] {e}")
            raise
     
    def transcribe_audio(self, audio_path):
        """Transcribe audio using OpenAI's Whisper API."""
        try:
            with open(audio_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            return transcript.text
        except Exception as e:
            print(f"[Transcription Error] {e}")
            raise
     
    def process_local_video(self, video_path):
        """Process a local video file: extract audio and transcribe."""
        audio_path = self.extract_audio(video_path)
        transcript = self.transcribe_audio(audio_path)
        
        # Clean up temporary files
        if os.path.exists(audio_path):
            os.remove(audio_path)
        
        return transcript
     
    def process_youtube_video(self, url):
        """Process a YouTube video: download, extract audio, and transcribe."""
        video_path, title = self.download_youtube_video(url)
        audio_path = self.extract_audio(video_path)
        transcript = self.transcribe_audio(audio_path)
        
        # Clean up temporary files
        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(audio_path):
            os.remove(audio_path)
        
        return transcript, title