import os
import sys
from PIL import Image
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

def remove_black_bars(image_path, output_path, threshold=5):
    """
    Удаляет черные полосы по краям изображения
    threshold - значение яркости (0-255), считающееся черным
    """
    try:
        img = Image.open(image_path)
        
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        pixels = img.load()
        width, height = img.size
        
        left = width
        right = 0
        top = height
        bottom = 0
        
        for x in range(width):
            for y in range(height):
                r, g, b = pixels[x, y]
                brightness = (r + g + b) / 3
                
                if brightness > threshold:
                    if x < left:
                        left = x
                    if x > right:
                        right = x
                    if y < top:
                        top = y
                    if y > bottom:
                        bottom = y
        
        if left < right and top < bottom:
            img = img.crop((left, top, right + 1, bottom + 1))
        
        size = min(img.size)
        left_crop = (img.width - size) // 2
        top_crop = (img.height - size) // 2
        img = img.crop((left_crop, top_crop, left_crop + size, top_crop + size))
        
        img = img.resize((Constants.THUMBNAIL_SIZE, Constants.THUMBNAIL_SIZE), Image.Resampling.LANCZOS)
        img.save(output_path, 'JPEG', quality=90)
        
        return True
    except Exception as e:
        print(f"не удалось обработать обложку: {e}")
        return False

def download_track(track, download_dir, embed_cover=True):
    video_id = track['videoId']
    url = f"https://music.youtube.com/watch?v={video_id}"
    
    safe_title = "".join(c for c in track['title'] if c.isalnum() or c in (' ', '-', '_')).strip()
    output_template = os.path.join(download_dir, f'{safe_title}.%(ext)s')
    temp_thumbnail = os.path.join(download_dir, f'{safe_title}_temp.jpg')
    final_thumbnail = os.path.join(download_dir, f'{safe_title}_cover.jpg')
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': Constants.AUDIO_FORMAT,
            'preferredquality': Constants.AUDIO_QUALITY,
        }],
        'outtmpl': output_template,
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
    
    if embed_cover:
        mp3_path = os.path.join(download_dir, f'{safe_title}.mp3')
        
        download_thumbnail_with_ytdlp(track, download_dir, safe_title, temp_thumbnail)
        
        if os.path.exists(temp_thumbnail):
            if remove_black_bars(temp_thumbnail, final_thumbnail):
                embed_thumbnail_to_mp3(mp3_path, final_thumbnail)
                os.remove(final_thumbnail)
            os.remove(temp_thumbnail)
            print("  обложка добавлена (без черных полос)")

def download_thumbnail_with_ytdlp(track, download_dir, safe_title, output_path):
    """Скачивает обложку через yt-dlp"""
    video_id = track['videoId']
    url = f"https://music.youtube.com/watch?v={video_id}"
    
    ydl_opts_thumb = {
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
        'writethumbnail': True,
        'outtmpl': os.path.join(download_dir, safe_title),
    }
    
    with yt_dlp.YoutubeDL(ydl_opts_thumb) as ydl:
        ydl.download([url])
    
    for ext in ['jpg', 'webp', 'png']:
        thumb_path = os.path.join(download_dir, f'{safe_title}.{ext}')
        if os.path.exists(thumb_path):
            os.rename(thumb_path, output_path)
            break

def embed_thumbnail_to_mp3(mp3_path, thumbnail_path):
    """Встраивает обложку в MP3 файл"""
    try:
        from mutagen.mp3 import MP3
        from mutagen.id3 import ID3, APIC, error
        
        audio = MP3(mp3_path, ID3=ID3)
        
        try:
            audio.add_tags()
        except error:
            pass
        
        with open(thumbnail_path, 'rb') as f:
            audio.tags.add(
                APIC(
                    encoding=3,
                    mime='image/jpeg',
                    type=3,
                    desc='Cover',
                    data=f.read()
                )
            )
        
        audio.save()
        return True
    except Exception as e:
        print(f"не удалось встроить обложку: {e}")
        return False

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')