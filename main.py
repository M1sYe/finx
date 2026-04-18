from ytmusicapi import YTMusic
import yt_dlp
import os
import sys

def search_and_download(query):
    ytmusic = YTMusic()
    
    print(f"\nищем: {query}")
    results = ytmusic.search(query, filter='songs', limit=5)
    
    if not results:
        print("ничего не найдено")
        return
    
    print("\nнайденные треки:")
    for i, track in enumerate(results, 1):
        artists = ', '.join([a['name'] for a in track.get('artists', [])])
        print(f"{i}. {track['title']} - {artists}")
    
    try:
        choice = int(input("\nВыберите номер трека для скачивания: ")) - 1
        if choice == -1: return
        if 0 <= choice < len(results):
            track = results[choice]
            video_id = track['videoId']
            url = f"https://music.youtube.com/watch?v={video_id}"
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print(f"\nскачивание: {track['title']}")
            
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': 'downloads/%(title)s.%(ext)s',
                'quiet': False,
                'no_warnings': False,
                'sleep_interval': 5,
                'max_sleep_interval': 10,
                'sleep_interval_requests': 1,
                'retries': 10,
                'fragment_retries': 10,
                'ffmpeg_location': r'C:\Program Files\ffmpeg-master-latest-win64-gpl-shared\bin\ffmpeg.exe',
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                os.system('cls' if os.name == 'nt' else 'clear')

            print("готово")
        else:
            print("неверный номер трека")
            
    except Exception as e:
        print(f"ошибка: {e}")

class cli_client():
    def __init__(self):
        self.dir = None

    def __call__(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(r" ____  __  __ _  _  _")
        print(r"(  __)(  )(  ( \( \/ )")
        print(r" ) _)  )( /    / )  ( ")
        print(r"(__)  (__)\_)__)(_/\_)")
        print("1. Найти трек")
        print("2. Изменить директорию для сохранения")
        
        
        try:
            user_input_case = int(input("ваш выбор: "))
        except ValueError:
            print("введите номер действия")
            return
        
        match user_input_case:
            case 2:
                new_path = input("путь: ")
                if new_path:
                    os.makedirs(new_path, exist_ok=True)
                    self.dir = new_path
                    print(f"директория: {self.dir}")
                else:
                    print("неверный путь")
            case 1:
                track_name = input("название трека: ")
                search_and_download(track_name)
os.makedirs('downloads', exist_ok=True)

cli = cli_client()
while True:
    try:
        cli()
    except KeyboardInterrupt:
        print("\n\nработа завершена")
        break
    except Exception as e:
        print(f"ошибка: {e}")