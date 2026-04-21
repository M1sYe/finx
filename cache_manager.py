import os
from constants import Constants
from logger import log_execution

class CacheManager:
    @log_execution
    def __init__(self):
        self.cache_path = Constants.CACHE_FILE
        self.download_dir = None
        self._initialize_cache()
    
    @log_execution
    def _initialize_cache(self):
        os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
        
        if os.path.exists(self.cache_path):
            self._load_cache()
        else:
            self._create_default_cache()
    
    @log_execution
    def _load_cache(self):
        try:
            with open(self.cache_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    self.download_dir = content
                else:
                    self.download_dir = Constants.DEFAULT_DOWNLOAD_DIR
        except (IOError, OSError):
            self.download_dir = Constants.DEFAULT_DOWNLOAD_DIR
    
    @log_execution
    def _create_default_cache(self):
        self.download_dir = Constants.DEFAULT_DOWNLOAD_DIR
        self._save_cache()
    
    @log_execution
    def _save_cache(self):
        try:
            with open(self.cache_path, 'w', encoding='utf-8') as f:
                f.write(self.download_dir)
        except (IOError, OSError):
            pass
    
    @log_execution
    def get_download_dir(self):
        return self.download_dir
    
    @log_execution
    def set_download_dir(self, new_dir):
        if new_dir and os.path.exists(new_dir):
            self.download_dir = new_dir
            self._save_cache()
            return True
        return False
    
    @log_execution
    def reset_to_default(self):
        self.download_dir = Constants.DEFAULT_DOWNLOAD_DIR
        self._save_cache()