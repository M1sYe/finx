import os
import tempfile

class Constants:
    APP_NAME = "finx"
    CACHE_DIR = os.path.join(tempfile.gettempdir(), 'finx')
    CACHE_FILE = os.path.join(CACHE_DIR, 'cache.txt')
    FFMPEG_PATH = "ffmpeg.exe"
    DEFAULT_DOWNLOAD_DIR = os.path.join(os.path.expanduser("~"), "Downloads")
    SEARCH_LIMIT = 5
    AUDIO_QUALITY = '192'
    AUDIO_FORMAT = 'mp3'
    SLEEP_INTERVAL = 5
    MAX_SLEEP_INTERVAL = 10
    SLEEP_INTERVAL_REQUESTS = 1
    RETRIES = 10
    FRAGMENT_RETRIES = 10
    THUMBNAIL_SIZE = 512
    AUTO_CROP_THUMBNAIL = True
    CROP_THRESHOLD = 0.05
    LOG_NAME = "logs.log"