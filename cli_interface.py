from constants import Constants
from downloader import search_tracks, format_track_info, download_track, clear_screen
import os

class CLIInterface:
    def __init__(self, cache_manager):
        self.cache = cache_manager
    
    def run(self):
        clear_screen()
        self._show_logo()
        self._show_menu()
        
        try:
            choice = int(input("введите: "))
        except ValueError:
            print("введите номер действия")
            return
        
        if choice == 1:
            self._handle_search()
        elif choice == 2:
            self._handle_directory_change()
    
    def _show_logo(self):
        print(r" ____  __  __ _  _  _")
        print(r"(  __)(  )(  ( \( \/ )")
        print(r" ) _)  )( /    / )  ( ")
        print(r"(__)  (__)\_)__)(_/\_)")
    
    def _show_menu(self):
        print("1. Найти трек")
        print("2. Папка для скачивания")
    
    def _handle_search(self):
        track_name = input("название трека: ")
        if not track_name.strip():
            print("название трека не может быть пустым")
            return
        
        self._search_and_download(track_name)
    
    def _search_and_download(self, query):
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