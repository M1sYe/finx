from constants import Constants
import sys
from logger import log_execution
from downloader import (
    search_tracks, 
    format_track_info, 
    download_track,
    search_albums,
    get_album_tracks,
    download_album,
    clear_screen
)
import os

class CLIInterface:
    @log_execution
    def __init__(self, cache_manager):
        self.cache = cache_manager
    
    @log_execution
    def run(self):
        clear_screen()
        self._show_logo()
        self._show_menu()
        
        try:
            choice = int(input("введите: "))
        except ValueError:
            print("введите номер действия")
            return
        if choice == 0:
            sys.exit()
        if choice == 1:
            self._handle_search()
        elif choice == 2:
            self._handle_album_search()
        elif choice == 3:
            self._handle_directory_change()
    
    @log_execution
    def _show_logo(self):
        print(r" ____  __  __ _  _  _")
        print(r"(  __)(  )(  ( \( \/ )")
        print(r" ) _)  )( /    / )  ( ")
        print(r"(__)  (__)\_)__)(_/\_)")
    
    @log_execution
    def _show_menu(self):
        print("0. Выход")
        print("1. Найти трек")
        print("2. Найти альбом")
        print("3. Папка для скачивания")
    
    @log_execution
    def _handle_search(self):
        track_name = input("название трека: ")
        if not track_name.strip():
            print("название трека не может быть пустым")
            return
        
        self._search_and_download_track(track_name)
    
    @log_execution
    def _handle_album_search(self):
        album_name = input("название альбома: ")
        if not album_name.strip():
            print("название альбома не может быть пустым")
            return
        
        self._search_and_download_album(album_name)
    
    @log_execution
    def _search_and_download_track(self, query):
        download_dir = self.cache.get_download_dir()
        
        print(f"\nищем: {query}")
        results = search_tracks(query)
        
        if not results:
            print("ничего не найдено")
            return
        
        print("\nнайденные треки:")
        for i, track in enumerate(results, 1):
            print(f"{i}. {format_track_info(track)}")
        
        try:
            choice = int(input("\nвыберите номер трека для скачивания: ")) - 1
            if choice == -1:
                return
            
            if 0 <= choice < len(results):
                track = results[choice]
                clear_screen()
                print(f"\nскачивание: {track['title']}")
                
                download_track(track, download_dir)
                clear_screen()
                print("готово")
            else:
                print("неверный номер трека")
                
        except ValueError:
            print("пожалуйста, введите число")
        except Exception as e:
            print(f"ошибка при скачивании: {e}")
    
    @log_execution
    def _search_and_download_album(self, query):
        download_dir = self.cache.get_download_dir()
        
        print(f"\nищем альбомы: {query}")
        results = search_albums(query)
        
        if not results:
            print("альбомы не найдены")
            return
        
        print("\nнайденные альбомы:")
        for i, album in enumerate(results, 1):
            album_title = album.get('title', 'Unknown')
            artists = album.get('artists', [])
            artist_str = ', '.join([a['name'] for a in artists]) if artists else 'Unknown Artist'
            print(f"{i}. {album_title} - {artist_str}")
        
        try:
            choice = int(input("\nвыберите номер альбома для скачивания (0 для отмены): ")) - 1
            
            if choice == -1:
                return
            
            if 0 <= choice < len(results):
                album = results[choice]
                album_id = album.get('browseId')
                album_title = album.get('title', 'Unknown Album')
                
                clear_screen()
                success = download_album(album_id, album_title, download_dir, embed_cover=True)
                
                clear_screen()
                if success:
                    print("альбом успешно скачан!")
                else:
                    print("ошибка при скачивании альбома")
            else:
                print("неверный номер альбома")
                
        except ValueError:
            print("пожалуйста, введите число")
        except Exception as e:
            print(f"ошибка при скачивании: {e}")
    
    @log_execution
    def _handle_directory_change(self):
        current_dir = self.cache.get_download_dir()
        print(f"текущая папка: {current_dir}")
        print("введите новый путь (0 для отмены, пустая строка для папки по умолчанию):")
        
        new_path = input().strip()
        
        if new_path == "0":
            return
        
        if not new_path:
            self.cache.reset_to_default()
            print(f"папка сброшена на: {self.cache.get_download_dir()}")
            return
        
        if os.path.exists(new_path):
            if self.cache.set_download_dir(new_path):
                print(f"папка изменена на: {new_path}")
            else:
                print("ошибка при сохранении папки")
        else:
            print("указанная папка не существует")