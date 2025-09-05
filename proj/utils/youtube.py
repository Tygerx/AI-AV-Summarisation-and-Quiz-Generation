# utils/youtube.py

from pytube import YouTube

def download_audio(youtube_url, output_path="temp_audio.mp4"):
    yt = YouTube(youtube_url)
    stream = yt.streams.filter(only_audio=True).first()
    stream.download(filename=output_path)
    return output_path