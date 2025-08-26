#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask Web API para YouTube Downloader
Conecta la interfaz web con el script de descarga existente
"""

import os
import sys
import json
import uuid
import threading
import subprocess
from datetime import datetime
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import yt_dlp
from pathlib import Path

# Importar funciones del script existente
try:
    import yt_dlp
except ImportError:
    print("Error: No se pudo importar yt-dlp")
    sys.exit(1)

app = Flask(__name__)
CORS(app)

# Configuración
DOWNLOADS_FOLDER = os.path.join(os.getcwd(), 'downloads')
FFMPEG_PATH = os.path.join(os.getcwd(), 'ffmpeg-8.0-essentials_build', 'bin')

# Asegurar que existe la carpeta de descargas
os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)

# Almacenamiento en memoria para el progreso de descargas
download_progress = {}
active_downloads = {}

def get_video_info(url):
    """Obtener información del video usando yt-dlp sin interacción del usuario"""
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'socket_timeout': 30,
            'retries': 3,
            'extract_flat': False,
            'ignoreerrors': False,
            'noplaylist': True,  # Por defecto no descargar playlist completa
            'ffmpeg_location': FFMPEG_PATH,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info
            
    except Exception as e:
        print(f"Error al obtener información: {e}")
        return None

def download_audio_api(url, quality, progress_callback=None, target_folder=None):
    """Descargar audio usando yt-dlp para la API"""
    try:
        # Usar carpeta especificada o la por defecto
        download_folder = target_folder if target_folder else DOWNLOADS_FOLDER
        
        # Configurar opciones de descarga de audio
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
            'ffmpeg_location': FFMPEG_PATH,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': quality,
            }],
            'progress_hooks': [progress_callback] if progress_callback else [],
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            return True
            
    except Exception as e:
        print(f"Error al descargar audio: {e}")
        return False

def download_video_api(url, quality, progress_callback=None, target_folder=None):
    """Descargar video usando yt-dlp para la API"""
    try:
        # Usar carpeta especificada o la por defecto
        download_folder = target_folder if target_folder else DOWNLOADS_FOLDER
        
        # Configurar opciones de descarga de video
        if quality == 'best':
            video_format = 'best'
        else:
            video_format = f'best[height<={quality}]/best'
            
        ydl_opts = {
            'format': video_format,
            'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
            'ffmpeg_location': FFMPEG_PATH,
            'progress_hooks': [progress_callback] if progress_callback else [],
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            return True
            
    except Exception as e:
        print(f"Error al descargar video: {e}")
        return False

class DownloadProgress:
    def __init__(self, download_id):
        self.download_id = download_id
        self.status = 'starting'
        self.percentage = 0
        self.speed = None
        self.eta = None
        self.filename = None
        self.error = None
        self.status_text = 'Iniciando descarga...'
        self.completed = False

    def update(self, d):
        """Callback para yt-dlp progress hook"""
        if d['status'] == 'downloading':
            self.status = 'downloading'
            self.status_text = 'Descargando...'
            
            # Calcular porcentaje
            if 'total_bytes' in d and d['total_bytes']:
                self.percentage = (d['downloaded_bytes'] / d['total_bytes']) * 100
            elif 'total_bytes_estimate' in d and d['total_bytes_estimate']:
                self.percentage = (d['downloaded_bytes'] / d['total_bytes_estimate']) * 100
            
            # Velocidad de descarga
            if 'speed' in d and d['speed']:
                speed_kbps = d['speed'] / 1024
                if speed_kbps > 1024:
                    self.speed = f"{speed_kbps/1024:.1f} MB/s"
                else:
                    self.speed = f"{speed_kbps:.1f} KB/s"
            
            # Tiempo estimado
            if 'eta' in d and d['eta']:
                eta_minutes = d['eta'] // 60
                eta_seconds = d['eta'] % 60
                self.eta = f"{eta_minutes:02d}:{eta_seconds:02d}"
                
        elif d['status'] == 'finished':
            self.status = 'processing'
            self.status_text = 'Procesando archivo...'
            self.percentage = 95
            self.filename = os.path.basename(d['filename'])
            
        elif d['status'] == 'error':
            self.status = 'error'
            self.error = str(d.get('error', 'Error desconocido'))
            self.status_text = f'Error: {self.error}'

    def complete(self, filename=None):
        """Marcar descarga como completada"""
        self.status = 'completed'
        self.status_text = 'Descarga completada'
        self.percentage = 100
        self.completed = True
        if filename:
            self.filename = filename

    def set_error(self, error_msg):
        """Marcar descarga como error"""
        self.status = 'error'
        self.error = error_msg
        self.status_text = f'Error: {error_msg}'

    def to_dict(self):
        """Convertir a diccionario para JSON"""
        return {
            'status': self.status,
            'percentage': self.percentage,
            'speed': self.speed,
            'eta': self.eta,
            'filename': self.filename,
            'error': self.error,
            'status_text': self.status_text,
            'completed': self.completed
        }

@app.route('/')
def index():
    """Servir la página principal"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Servir archivos estáticos"""
    return send_from_directory('.', filename)

@app.route('/api/analyze', methods=['POST'])
def analyze_video():
    """Analizar URL de YouTube y obtener información del video"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se recibieron datos'
            })
            
        url = (data.get('url') or '').strip()
        
        if not url:
            return jsonify({
                'success': False,
                'error': 'URL no proporcionada'
            })
        
        # Obtener información del video/playlist directamente
        info = get_video_info(url)
        
        if not info:
            return jsonify({
                'success': False,
                'error': 'No se pudo obtener información del video'
            })
        
        # Detectar si es playlist basado en la información obtenida
        is_playlist = info.get('_type') == 'playlist'
        playlist_count = len(info.get('entries', [])) if is_playlist else 0
        
        # Preparar respuesta
        response_data = {
            'success': True,
            'info': {
                'title': info.get('title', 'Título no disponible'),
                'uploader': info.get('uploader', 'Canal no disponible'),
                'duration': info.get('duration', 0),
                'view_count': info.get('view_count', 0),
                'upload_date': info.get('upload_date', ''),
                'thumbnail': info.get('thumbnail', ''),
                'webpage_url': info.get('webpage_url', url),
                'is_playlist': is_playlist,
                'playlist_count': playlist_count
            }
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"Error en analyze_video: {e}")
        return jsonify({
            'success': False,
            'error': f'Error al analizar el video: {str(e)}'
        })

@app.route('/api/download', methods=['POST'])
def start_download():
    """Iniciar descarga de video/audio"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se recibieron datos'
            })
            
        url = (data.get('url') or '').strip()
        format_type = data.get('format', 'audio')  # 'audio' o 'video'
        quality = data.get('quality', 'best')
        is_playlist = data.get('playlist', False)
        download_path = (data.get('download_path') or '').strip()
        
        if not url:
            return jsonify({
                'success': False,
                'error': 'URL no proporcionada'
            })
        
        # Generar ID único para la descarga
        download_id = str(uuid.uuid4())
        
        # Crear objeto de progreso
        progress = DownloadProgress(download_id)
        download_progress[download_id] = progress
        
        # Determinar carpeta de descarga
        target_folder = DOWNLOADS_FOLDER  # Default
        
        if download_path:
            # Si viene con prefijo FSAPI, usar carpeta por defecto (limitación del navegador)
            if download_path.startswith('FSAPI:'):
                folder_name = download_path.replace('FSAPI:', '')
                print(f"📁 Carpeta seleccionada via File System API: {folder_name}")
                print(f"⚠️  Usando carpeta por defecto debido a limitaciones del navegador: {DOWNLOADS_FOLDER}")
                target_folder = DOWNLOADS_FOLDER
            # Si es una ruta manual, validarla
            elif os.path.isabs(download_path):
                if os.path.isdir(download_path):
                    target_folder = download_path
                    print(f"📁 Usando carpeta personalizada: {target_folder}")
                else:
                    # Intentar crear la carpeta si no existe
                    try:
                        os.makedirs(download_path, exist_ok=True)
                        target_folder = download_path
                        print(f"📁 Carpeta creada y configurada: {target_folder}")
                    except Exception as e:
                        print(f"❌ Error creando carpeta {download_path}: {e}")
                        print(f"📁 Usando carpeta por defecto: {DOWNLOADS_FOLDER}")
                        target_folder = DOWNLOADS_FOLDER
            else:
                print(f"⚠️  Ruta inválida: {download_path}")
                print(f"📁 Usando carpeta por defecto: {DOWNLOADS_FOLDER}")
                target_folder = DOWNLOADS_FOLDER
        
        # Iniciar descarga en hilo separado
        download_thread = threading.Thread(
            target=download_worker,
            args=(download_id, url, format_type, quality, is_playlist, progress, target_folder)
        )
        download_thread.daemon = True
        download_thread.start()
        
        active_downloads[download_id] = download_thread
        
        return jsonify({
            'success': True,
            'download_id': download_id,
            'message': 'Descarga iniciada'
        })
        
    except Exception as e:
        print(f"Error en start_download: {e}")
        return jsonify({
            'success': False,
            'error': f'Error al iniciar descarga: {str(e)}'
        })

def download_worker(download_id, url, format_type, quality, is_playlist, progress, target_folder):
    """Worker para realizar la descarga en segundo plano"""
    try:
        if format_type == 'audio':
            success = download_audio_api(url, quality, progress.update, target_folder)
        else:
            success = download_video_api(url, quality, progress.update, target_folder)
        
        if success:
            progress.complete()
        else:
            progress.set_error("Error durante la descarga")
            
    except Exception as e:
        print(f"Error en download_worker: {e}")
        progress.set_error(str(e))
    
    finally:
        # Limpiar hilo activo
        if download_id in active_downloads:
            del active_downloads[download_id]

@app.route('/api/progress/<download_id>', methods=['GET'])
def get_progress(download_id):
    """Obtener progreso de descarga"""
    try:
        if download_id not in download_progress:
            return jsonify({
                'success': False,
                'error': 'ID de descarga no encontrado'
            })
        
        progress = download_progress[download_id]
        
        return jsonify({
            'success': True,
            'progress': progress.to_dict()
        })
        
    except Exception as e:
        print(f"Error en get_progress: {e}")
        return jsonify({
            'success': False,
            'error': f'Error al obtener progreso: {str(e)}'
        })

@app.route('/api/cancel/<download_id>', methods=['POST'])
def cancel_download(download_id):
    """Cancelar descarga"""
    try:
        if download_id in active_downloads:
            # Marcar como cancelado
            if download_id in download_progress:
                download_progress[download_id].set_error('Descarga cancelada por el usuario')
            
            # Limpiar
            del active_downloads[download_id]
            
            return jsonify({
                'success': True,
                'message': 'Descarga cancelada'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Descarga no encontrada o ya finalizada'
            })
            
    except Exception as e:
        print(f"Error en cancel_download: {e}")
        return jsonify({
            'success': False,
            'error': f'Error al cancelar descarga: {str(e)}'
        })

@app.route('/api/open-folder', methods=['POST'])
def open_download_folder():
    """Abrir carpeta de descargas"""
    try:
        if os.name == 'nt':  # Windows
            os.startfile(DOWNLOADS_FOLDER)
        elif os.name == 'posix':  # macOS y Linux
            subprocess.run(['open' if sys.platform == 'darwin' else 'xdg-open', DOWNLOADS_FOLDER])
        
        return jsonify({
            'success': True,
            'message': 'Carpeta abierta'
        })
        
    except Exception as e:
        print(f"Error en open_download_folder: {e}")
        return jsonify({
            'success': False,
            'error': f'Error al abrir carpeta: {str(e)}'
        })

@app.route('/api/downloads', methods=['GET'])
def list_downloads():
    """Listar archivos descargados"""
    try:
        files = []
        if os.path.exists(DOWNLOADS_FOLDER):
            for filename in os.listdir(DOWNLOADS_FOLDER):
                filepath = os.path.join(DOWNLOADS_FOLDER, filename)
                if os.path.isfile(filepath):
                    stat = os.stat(filepath)
                    files.append({
                        'name': filename,
                        'size': stat.st_size,
                        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        'type': 'audio' if filename.endswith('.mp3') else 'video'
                    })
        
        return jsonify({
            'success': True,
            'files': sorted(files, key=lambda x: x['modified'], reverse=True)
        })
        
    except Exception as e:
        print(f"Error en list_downloads: {e}")
        return jsonify({
            'success': False,
            'error': f'Error al listar descargas: {str(e)}'
        })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint no encontrado'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Error interno del servidor'
    }), 500

if __name__ == '__main__':
    print("🚀 Iniciando YouTube Downloader Web API...")
    print(f"📁 Carpeta de descargas: {DOWNLOADS_FOLDER}")
    print(f"🎬 FFmpeg path: {FFMPEG_PATH}")
    print("🌐 Servidor disponible en: http://localhost:5000")
    print("\n" + "="*50)
    print("YouTube Downloader Web Interface")
    print("Presiona Ctrl+C para detener el servidor")
    print("="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)