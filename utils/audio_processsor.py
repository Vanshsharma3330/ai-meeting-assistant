# Accepts any audio/video source and converts it into wav chunks ready for whisper to process. It also handles resampling and normalization of the audio.

# What this file does:
# 1. Detects if input is a Youtube URL, local file path, or a direct audio/video stream.
# 2. Downloads audio only stream from YouTube using yt-dlp
# 3. Converts any format(MP4/MP3/M4A) to wave using ffmpeg
# 4. Splits large audio files into 10 mins chunk for whisper
# 5. Reeturns a list fo chunk file paths to the next step


# yt-dlp is a powerful, open-source command-line tool and Python library used to download video and audio from YouTube and thousands of other websites.


import os
import yt_dlp
from pydub import AudioSegment          # will use it for audio chunking
import static_ffmpeg
static_ffmpeg.add_paths()

DOWNLOAD_DIR = "downloades"              # Directory to store downloaded audio files
os.makedirs(DOWNLOAD_DIR, exist_ok=True)# Create the downloaded directory if it does not exist


def download_youtube_audio(url: str) -> str:
    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192"
            }
        ],
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).replace(".webm", ".wav").replace(".m4a", ".wav")

    return filename



print(download_youtube_audio("https://youtu.be/T-D1OfcDW1M?si=k_6uQFPXPkzs3lRh"))