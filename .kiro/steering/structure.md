# Project Structure

## Root Directory Organization

```
mp3Youtube/
├── .git/                           # Git version control
├── .kiro/                          # Kiro IDE configuration
├── .vscode/                        # VS Code settings
├── downloads/                      # Output folder for downloaded files
│   ├── *.mp3                      # Downloaded audio files
│   ├── *.mp4                      # Downloaded video files
│   └── playlist/                  # Playlist downloads subfolder
├── ffmpeg-8.0-essentials_build/   # Local ffmpeg binaries
├── youtube_downloader.py          # Main CLI application
├── ejemplo_avanzado.py            # Advanced features demo
├── solucion_error_400.py          # Troubleshooting utility
├── index.html                     # Web interface
├── styles.css                     # Web interface styling
├── requirements.txt               # Python dependencies
├── README.md                      # Project documentation
└── .gitignore                     # Git ignore rules
```

## File Responsibilities

### Core Python Files
- **`youtube_downloader.py`**: Main application entry point with interactive CLI
- **`ejemplo_avanzado.py`**: Educational examples showing advanced pytube features
- **`solucion_error_400.py`**: Diagnostic and repair utility for common issues

### Web Interface Files
- **`index.html`**: Complete web interface with responsive design
- **`styles.css`**: Modern CSS styling with dark theme and animations
- **Note**: Web interface is frontend-only, requires Python CLI for actual downloads

### Configuration Files
- **`requirements.txt`**: Python package dependencies with version constraints
- **`README.md`**: Comprehensive documentation in Spanish
- **`.gitignore`**: Excludes downloads folder and common Python artifacts

## Folder Conventions

### Downloads Organization
- **`downloads/`**: Main output directory (auto-created)
- **`downloads/playlist/`**: Playlist downloads (created by advanced script)
- **`downloads/calidad_especifica/`**: Quality-specific downloads

### Naming Conventions
- **Python Files**: Snake_case with descriptive names
- **Downloaded Files**: Sanitized titles with proper extensions
- **Folders**: Lowercase with underscores for multi-word names

## Development Patterns

### File Creation
- Downloads folder created automatically on first run
- Subfolders created as needed by specific features
- Safe filename sanitization for cross-platform compatibility

### Import Structure
- Conditional imports with fallback handling
- Try/except blocks for optional dependencies
- Clear error messages when dependencies missing

### Code Organization
- Single-purpose functions with clear docstrings
- Consistent error handling patterns
- Spanish language for user-facing messages