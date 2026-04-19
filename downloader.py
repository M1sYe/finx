import os
import sys
from ytmusicapi import YTMusic
import yt_dlp
from constants import Constants

def get_resource_path():
    try:
        return sys._MEIPASS
    except Exception:
        return os.path.abspath(".")

def search_tracks(query, limit=Constants.SEARCH_LIMIT):
    ytmusic = YTMusic()
    results = ytmusic.search(query, filter='songs', limit=limit)
    return results

def format_track_info(track):
    artists = ', '.join([a['name'] for a in track.get('artists', [])])
    return f"{track['title']} - {artists}"

def download_track(track, download_dir):
    video_id = track['videoId']
    url = f"https://music.youtube.com/watch?v={video_id}"
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': Constants.AUDIO_FORMAT,
            'preferredquality': Constants.AUDIO_QUALITY,
        }],
        'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
        'quiet': False,
        'no_warnings': False,
        'sleep_interval': Constants.SLEEP_INTERVAL,
        'max_sleep_interval': Constants.MAX_SLEEP_INTERVAL,
        'sleep_interval_requests': Constants.SLEEP_INTERVAL_REQUESTS,
        'retries': Constants.RETRIES,
        'fragment_retries': Constants.FRAGMENT_RETRIES,
        'ffmpeg_location': Constants.FFMPEG_PATH,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')