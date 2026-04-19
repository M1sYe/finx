# Finx - Music Downloader

A lightweight, CLI-based utility for downloading music. Built with simplicity and efficiency in mind.

## Features

- Search tracks
- Download audio in MP3 format (192kbps quality)
- Simple and intuitive CLI interface
- Fast downloads with yt-dlp backend

## Requirements

- **Python 3.10 or higher**
- **FFmpeg** (for audio conversion)

## Build
```
python -m PyInstaller --noconfirm --onefile --console --hidden-import "yt_dlp" --hidden-import "ytmusicapi" --hidden-import "yt_dlp.extractor.youtube" --hidden-import "yt_dlp.downloader" --collect-all "yt_dlp" --collect-all "ytmusicapi"  "main.py"
```
