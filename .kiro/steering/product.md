# Product Overview

## YouTube Downloader

A Python-based YouTube video and audio downloader with both command-line interface and web interface. The application allows users to download YouTube videos in MP4 format or extract audio in MP3 format.

### Key Features

- Download complete videos in MP4 format
- Extract audio-only in MP3 format  
- Interactive command-line interface
- Modern web interface with responsive design
- Robust error handling and fallback mechanisms
- Automatic file organization in downloads folder
- Support for custom filenames
- URL validation and video information display
- Playlist detection and handling
- Multiple quality options

### Target Use Case

Educational tool for learning about YouTube content downloading, pytube library usage, and multimedia processing. Designed for personal use and educational purposes only.

### Technical Approach

- Primary library: pytube for YouTube API interaction
- Fallback library: yt-dlp for enhanced reliability
- Web interface: Pure HTML/CSS/JavaScript (no backend)
- Error recovery: Automatic fallback mechanisms and troubleshooting tools
- File management: Organized downloads with cleaned filenames