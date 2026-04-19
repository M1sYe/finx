python -m PyInstaller --noconfirm --onefile --console --hidden-import "yt_dlp" --hidden-import "ytmusicapi" --hidden-import "yt_dlp.extractor.youtube" --hidden-import "yt_dlp.downloader" --collect-all "yt_dlp" --collect-all "ytmusicapi"  "main.py"
rmdir /s /q build
del /q *.spec

