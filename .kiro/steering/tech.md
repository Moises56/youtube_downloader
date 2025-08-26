# Technology Stack

## Core Technologies

### Python Environment
- **Python Version**: 3.6+ required
- **Package Manager**: pip for dependency management
- **Virtual Environment**: Recommended for isolation

### Primary Dependencies
- **pytube**: Main library for YouTube video downloading
- **yt-dlp**: Fallback library for enhanced reliability and error recovery
- **requests**: HTTP connectivity verification
- **ffmpeg**: Required for yt-dlp audio conversion (external binary)

### Web Interface
- **Frontend**: Pure HTML5, CSS3, JavaScript (no framework dependencies)
- **Styling**: CSS Grid/Flexbox, CSS custom properties
- **Icons**: Font Awesome 6.0
- **Fonts**: Google Fonts (Inter)
- **No Backend**: Static files only, relies on Python CLI for actual downloading

## Build System & Commands

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Alternative installations for troubleshooting
pip install --upgrade pytube
pip install git+https://github.com/pytube/pytube.git
pip install yt-dlp
```

### Running the Application
```bash
# Main CLI application
python youtube_downloader.py

# Advanced examples and features
python ejemplo_avanzado.py

# Troubleshooting and error resolution
python solucion_error_400.py
```

### Testing & Validation
```bash
# Test pytube functionality
python -c "from pytube import YouTube; print('pytube working')"

# Test yt-dlp functionality  
python -c "import yt_dlp; print('yt-dlp working')"
```

## Architecture Patterns

### Error Handling Strategy
- **Graceful Degradation**: Automatic fallback from pytube to yt-dlp
- **User-Friendly Messages**: Clear error descriptions with suggested solutions
- **Retry Logic**: Built-in retry mechanisms for network issues
- **Validation**: URL validation before processing

### File Management
- **Organized Structure**: Automatic creation of downloads folder
- **Safe Filenames**: Character sanitization for cross-platform compatibility
- **Extension Handling**: Proper file extension management (.mp4/.mp3)

### Code Organization
- **Modular Functions**: Single responsibility principle
- **Error Recovery**: Dedicated troubleshooting utilities
- **Configuration**: External requirements.txt for dependencies