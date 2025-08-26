#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube Downloader Script
=========================

Este script permite descargar videos de YouTube en formato MP4 o solo el audio en formato MP3.
Utiliza la librería pytube para interactuar con YouTube.

Instalación de dependencias:
    pip install pytube
    pip install pydub  # Para conversión de audio (opcional)

Autor: Script educativo
Fecha: 2024
"""

import os
import sys
import re
import subprocess
import requests
from urllib.parse import urlparse, parse_qs

try:
    from pytube import YouTube
    from pytube.exceptions import RegexMatchError, VideoUnavailable, LiveStreamError
    PYTUBE_AVAILABLE = True
except ImportError:
    PYTUBE_AVAILABLE = False
    print("⚠️  pytube no está instalado. Instálalo con: pip install pytube")

# Verificar si yt-dlp está disponible como alternativa
try:
    import yt_dlp
    YT_DLP_AVAILABLE = True
except ImportError:
    YT_DLP_AVAILABLE = False

def crear_carpeta_downloads():
    """
    Crea la carpeta 'downloads' si no existe.
    
    Returns:
        str: Ruta de la carpeta downloads
    """
    carpeta_downloads = os.path.join(os.getcwd(), "downloads")
    if not os.path.exists(carpeta_downloads):
        os.makedirs(carpeta_downloads)
        print(f"✅ Carpeta 'downloads' creada en: {carpeta_downloads}")
    return carpeta_downloads

def validar_url(url):
    """
    Valida si la URL proporcionada es una URL válida de YouTube.
    
    Args:
        url (str): URL a validar
        
    Returns:
        bool: True si es válida, False en caso contrario
    """
    patron_youtube = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
    return bool(re.match(patron_youtube, url))

def limpiar_nombre_archivo(nombre):
    """
    Limpia el nombre del archivo removiendo caracteres no válidos.
    
    Args:
        nombre (str): Nombre original del archivo
        
    Returns:
        str: Nombre limpio del archivo
    """
    # Caracteres no permitidos en nombres de archivo
    caracteres_invalidos = '<>:"/\\|?*'
    for char in caracteres_invalidos:
        nombre = nombre.replace(char, '_')
    return nombre.strip()

def obtener_informacion_video(url):
    """
    Obtiene información básica del video de YouTube.
    
    Args:
        url (str): URL del video de YouTube
        
    Returns:
        YouTube: Objeto YouTube con la información del video o dict con info si usa yt-dlp
    """
    if PYTUBE_AVAILABLE:
        try:
            # Intentar con pytube primero
            yt = YouTube(url)
            print(f"\n📹 Título: {yt.title}")
            print(f"👤 Autor: {yt.author}")
            print(f"⏱️  Duración: {yt.length // 60}:{yt.length % 60:02d} minutos")
            print(f"👀 Vistas: {yt.views:,}")
            return yt
        except (RegexMatchError, VideoUnavailable, LiveStreamError) as e:
            print(f"❌ Error con pytube: {str(e)}")
            if YT_DLP_AVAILABLE:
                print("🔄 Intentando con yt-dlp como alternativa...")
                return obtener_info_con_ytdlp(url)
            return None
        except Exception as e:
            error_msg = str(e)
            if "HTTP Error 400" in error_msg or "HTTP Error 403" in error_msg:
                print(f"❌ Error de conexión con pytube: {error_msg}")
                if YT_DLP_AVAILABLE:
                    print("🔄 Intentando con yt-dlp como alternativa...")
                    
                    # Verificar conectividad antes de continuar
                    if verificar_conectividad(url):
                        return obtener_info_con_ytdlp(url)
                    else:
                        print("❌ Problemas de conectividad detectados")
                        return None
                else:
                    print("💡 Sugerencia: Instala yt-dlp como alternativa: pip install yt-dlp")
                    print("💡 O actualiza pytube: pip install --upgrade pytube")
            else:
                print(f"❌ Error inesperado: {error_msg}")
            return None
    elif YT_DLP_AVAILABLE:
        return obtener_info_con_ytdlp(url)
    else:
        print("❌ No hay librerías de descarga disponibles.")
        print("💡 Instala pytube: pip install pytube")
        print("💡 O instala yt-dlp: pip install yt-dlp")
        return None

def verificar_conectividad(url):
    """
    Verifica si la URL es accesible antes de procesarla.
    """
    try:
        print("🌐 Verificando conectividad...")
        response = requests.head(url, timeout=10)
        if response.status_code == 200:
            print("✅ Conectividad verificada")
            return True
        else:
            print(f"⚠️  Respuesta HTTP: {response.status_code}")
            return True  # Continuar de todas formas
    except requests.exceptions.Timeout:
        print("⚠️  Timeout de conexión - continuando de todas formas...")
        return True
    except Exception as e:
        print(f"⚠️  Error de conectividad: {str(e)} - continuando de todas formas...")
        return True

def detectar_playlist(url):
    """
    Detecta si la URL es una playlist y ofrece opciones al usuario.
    
    Args:
        url (str): URL de YouTube
        
    Returns:
        str: URL modificada o None si el usuario cancela
    """
    if 'list=' in url:
        print("\n🎵 ¡PLAYLIST DETECTADA!")
        print("La URL contiene una playlist que podría tener cientos de videos.")
        print("\n¿Qué deseas hacer?")
        print("1. Descargar SOLO el video actual (recomendado)")
        print("2. Descargar TODA la playlist (puede tardar mucho)")
        print("3. Cancelar")
        
        while True:
            try:
                opcion = input("\nSelecciona una opción (1-3): ").strip()
                
                if opcion == '1':
                    # Extraer solo el video ID y crear nueva URL
                    if 'v=' in url:
                        video_id = url.split('v=')[1].split('&')[0]
                        nueva_url = f"https://www.youtube.com/watch?v={video_id}"
                        print(f"✅ Descargando solo el video: {nueva_url}")
                        return nueva_url
                    else:
                        print("❌ No se pudo extraer el ID del video")
                        return None
                        
                elif opcion == '2':
                    print("⚠️  ADVERTENCIA: Esto descargará TODA la playlist")
                    confirmacion = input("¿Estás seguro? (s/N): ").strip().lower()
                    if confirmacion in ['s', 'si', 'sí', 'y', 'yes']:
                        print("📋 Descargando playlist completa...")
                        return url
                    else:
                        continue
                        
                elif opcion == '3':
                    print("❌ Operación cancelada")
                    return None
                    
                else:
                    print("❌ Opción inválida. Por favor selecciona 1, 2 o 3.")
                    
            except KeyboardInterrupt:
                print("\n❌ Operación cancelada por el usuario")
                return None
    
    return url

def obtener_info_con_ytdlp(url):
    """
    Obtiene información del video usando yt-dlp como alternativa.
    
    Args:
        url (str): URL del video de YouTube
        
    Returns:
        dict: Información del video
    """
    try:
        # Detectar y manejar playlists
        url_procesada = detectar_playlist(url)
        if not url_procesada:
            return None
            
        print("⏳ Conectando con YouTube...")
        
        # Ruta local de ffmpeg
        ffmpeg_path = os.path.join(os.path.dirname(__file__), 'ffmpeg-8.0-essentials_build', 'bin')
        
        ydl_opts = {
            'quiet': False,  # Mostrar progreso
            'no_warnings': False,  # Mostrar advertencias
            'socket_timeout': 30,  # Timeout de 30 segundos
            'retries': 3,  # Reintentar 3 veces
            'extract_flat': False,
            'ignoreerrors': False,
            'noplaylist': 'list=' not in url_procesada or url != url_procesada,  # No playlist si se modificó la URL
            'ffmpeg_location': ffmpeg_path,  # Especificar ruta de ffmpeg
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("🔍 Extrayendo información del video...")
            info = ydl.extract_info(url_procesada, download=False)
            
            if info:
                # Verificar si es una playlist
                if info.get('_type') == 'playlist':
                    print(f"\n📋 Playlist: {info.get('title', 'N/A')}")
                    print(f"📊 Número de videos: {len(info.get('entries', []))}")
                    print(f"👤 Autor: {info.get('uploader', 'N/A')}")
                else:
                    print(f"\n📹 Título: {info.get('title', 'N/A')}")
                    print(f"👤 Autor: {info.get('uploader', 'N/A')}")
                    
                    duration = info.get('duration', 0)
                    if duration:
                        print(f"⏱️  Duración: {duration // 60}:{duration % 60:02d} minutos")
                    
                    views = info.get('view_count')
                    if views:
                        print(f"👀 Vistas: {views:,}")
                
                # Crear un objeto similar a pytube para compatibilidad
                info['_es_ytdlp'] = True
                info['_url_original'] = url
                info['_url_procesada'] = url_procesada
                return info
            else:
                print("❌ No se pudo obtener información del video")
                return None
                
    except Exception as e:
        print(f"❌ Error con yt-dlp: {str(e)}")
        return None

def descargar_audio(yt, carpeta_destino, nombre_personalizado=None):
    """
    Descarga solo el audio del video en la mejor calidad disponible.
    
    Args:
        yt (YouTube o dict): Objeto YouTube o información del video
        carpeta_destino (str): Carpeta donde guardar el archivo
        nombre_personalizado (str, optional): Nombre personalizado para el archivo
    """
    try:
        # Verificar si es información de yt-dlp
        if isinstance(yt, dict) and yt.get('_es_ytdlp'):
            return descargar_audio_ytdlp(yt, carpeta_destino, nombre_personalizado)
        
        print("\n🔍 Buscando stream de audio...")
        
        # Obtener el stream de audio de mejor calidad
        audio_stream = yt.streams.filter(only_audio=True).first()
        
        if not audio_stream:
            print("❌ No se encontró stream de audio disponible.")
            return
        
        print(f"🎵 Calidad de audio encontrada: {audio_stream.abr}")
        
        # Definir nombre del archivo
        if nombre_personalizado:
            nombre_archivo = limpiar_nombre_archivo(nombre_personalizado)
        else:
            nombre_archivo = limpiar_nombre_archivo(yt.title)
        
        print(f"⬇️  Descargando audio: {nombre_archivo}...")
        
        # Descargar el archivo
        archivo_descargado = audio_stream.download(
            output_path=carpeta_destino,
            filename=f"{nombre_archivo}.mp4"
        )
        
        # Renombrar a .mp3 (nota: el archivo sigue siendo mp4/webm, solo cambia la extensión)
        archivo_mp3 = archivo_descargado.replace('.mp4', '.mp3')
        os.rename(archivo_descargado, archivo_mp3)
        
        print(f"✅ Audio descargado exitosamente: {archivo_mp3}")
        
    except Exception as e:
        print(f"❌ Error al descargar audio: {str(e)}")

def descargar_audio_ytdlp(info, carpeta_destino, nombre_personalizado=None):
    """
    Descarga audio usando yt-dlp.
    
    Args:
        info (dict): Información del video de yt-dlp
        carpeta_destino (str): Carpeta donde guardar el archivo
        nombre_personalizado (str, optional): Nombre personalizado para el archivo
    """
    try:
        print("\n🎵 Iniciando descarga de audio con yt-dlp...")
        
        # Definir nombre del archivo
        if nombre_personalizado:
            nombre_archivo = limpiar_nombre_archivo(nombre_personalizado)
        else:
            nombre_archivo = limpiar_nombre_archivo(info.get('title', 'audio'))
        
        archivo_salida = os.path.join(carpeta_destino, f"{nombre_archivo}.%(ext)s")
        
        # Ruta local de ffmpeg
        ffmpeg_path = os.path.join(os.path.dirname(__file__), 'ffmpeg-8.0-essentials_build', 'bin')
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': archivo_salida,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': False,  # Mostrar progreso
            'socket_timeout': 30,
            'retries': 3,
            'ffmpeg_location': ffmpeg_path,  # Especificar ruta de ffmpeg
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Usar la URL procesada si está disponible
            url_descarga = info.get('_url_procesada', info.get('webpage_url', info.get('_url_original')))
            ydl.download([url_descarga])
        
        print(f"✅ Audio descargado exitosamente en: {carpeta_destino}")
        
    except Exception as e:
        print(f"❌ Error al descargar audio con yt-dlp: {str(e)}")
        print("💡 Nota: yt-dlp requiere ffmpeg para conversión de audio")
        print("💡 Instala ffmpeg desde: https://ffmpeg.org/download.html")

def descargar_video(yt, carpeta_destino, nombre_personalizado=None):
    """
    Descarga el video completo en la mejor calidad disponible.
    
    Args:
        yt (YouTube o dict): Objeto YouTube o información del video
        carpeta_destino (str): Carpeta donde guardar el archivo
        nombre_personalizado (str, optional): Nombre personalizado para el archivo
    """
    try:
        # Verificar si es información de yt-dlp
        if isinstance(yt, dict) and yt.get('_es_ytdlp'):
            return descargar_video_ytdlp(yt, carpeta_destino, nombre_personalizado)
        
        print("\n🔍 Buscando streams de video...")
        
        # Obtener streams de video disponibles
        video_streams = yt.streams.filter(progressive=True, file_extension='mp4')
        
        if not video_streams:
            print("❌ No se encontraron streams de video MP4 disponibles.")
            return
        
        # Seleccionar la mejor calidad
        mejor_stream = video_streams.get_highest_resolution()
        
        print(f"🎬 Calidad de video encontrada: {mejor_stream.resolution}")
        print(f"📁 Tamaño aproximado: {mejor_stream.filesize_mb:.1f} MB")
        
        # Definir nombre del archivo
        if nombre_personalizado:
            nombre_archivo = limpiar_nombre_archivo(nombre_personalizado)
        else:
            nombre_archivo = limpiar_nombre_archivo(yt.title)
        
        print(f"⬇️  Descargando video: {nombre_archivo}...")
        
        # Descargar el archivo
        archivo_descargado = mejor_stream.download(
            output_path=carpeta_destino,
            filename=f"{nombre_archivo}.mp4"
        )
        
        print(f"✅ Video descargado exitosamente: {archivo_descargado}")
        
    except Exception as e:
        print(f"❌ Error al descargar video: {str(e)}")

def descargar_video_ytdlp(info, carpeta_destino, nombre_personalizado=None):
    """
    Descarga video usando yt-dlp.
    
    Args:
        info (dict): Información del video de yt-dlp
        carpeta_destino (str): Carpeta donde guardar el archivo
        nombre_personalizado (str, optional): Nombre personalizado para el archivo
    """
    try:
        print("\n🎬 Iniciando descarga de video con yt-dlp...")
        
        # Definir nombre del archivo
        if nombre_personalizado:
            nombre_archivo = limpiar_nombre_archivo(nombre_personalizado)
        else:
            nombre_archivo = limpiar_nombre_archivo(info.get('title', 'video'))
        
        archivo_salida = os.path.join(carpeta_destino, f"{nombre_archivo}.%(ext)s")
        
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': archivo_salida,
            'quiet': False,  # Mostrar progreso
            'socket_timeout': 30,
            'retries': 3,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Usar la URL procesada si está disponible
            url_descarga = info.get('_url_procesada', info.get('webpage_url', info.get('_url_original')))
            ydl.download([url_descarga])
        
        print(f"✅ Video descargado exitosamente en: {carpeta_destino}")
        
    except Exception as e:
        print(f"❌ Error al descargar video con yt-dlp: {str(e)}")

def mostrar_menu():
    """
    Muestra el menú de opciones al usuario.
    """
    print("\n" + "="*50)
    print("🎥 DESCARGADOR DE YOUTUBE")
    print("="*50)
    print("Selecciona el tipo de descarga:")
    print("1. 🎵 Solo audio (MP3)")
    print("2. 🎬 Video completo (MP4)")
    print("3. ❌ Salir")
    print("="*50)

def main():
    """
    Función principal del programa.
    """
    print("🚀 Iniciando YouTube Downloader...")
    print("\n📋 Dependencias requeridas:")
    print("   pip install pytube")
    print("\n💡 Asegúrate de tener las dependencias instaladas antes de continuar.")
    
    # Crear carpeta de descargas
    carpeta_downloads = crear_carpeta_downloads()
    
    while True:
        try:
            mostrar_menu()
            
            # Obtener opción del usuario
            opcion = input("\nElige una opción (1-3): ").strip()
            
            if opcion == '3':
                print("👋 ¡Hasta luego!")
                break
            
            if opcion not in ['1', '2']:
                print("❌ Opción no válida. Por favor, elige 1, 2 o 3.")
                continue
            
            # Obtener URL del video
            print("\n" + "-"*50)
            url = input("🔗 Ingresa la URL del video de YouTube: ").strip()
            
            if not url:
                print("❌ No se proporcionó ninguna URL.")
                continue
            
            # Validar URL
            if not validar_url(url):
                print("❌ La URL no parece ser una URL válida de YouTube.")
                continue
            
            # Obtener información del video
            print("\n🔄 Obteniendo información del video...")
            yt = obtener_informacion_video(url)
            
            if not yt:
                continue
            
            # Preguntar por nombre personalizado
            nombre_personalizado = input("\n📝 Nombre personalizado (presiona Enter para usar el título original): ").strip()
            if not nombre_personalizado:
                nombre_personalizado = None
            
            # Procesar según la opción elegida
            if opcion == '1':
                descargar_audio(yt, carpeta_downloads, nombre_personalizado)
            elif opcion == '2':
                descargar_video(yt, carpeta_downloads, nombre_personalizado)
            
            # Preguntar si quiere continuar
            continuar = input("\n🔄 ¿Quieres descargar otro video? (s/n): ").strip().lower()
            if continuar not in ['s', 'si', 'sí', 'y', 'yes']:
                print("👋 ¡Hasta luego!")
                break
                
        except KeyboardInterrupt:
            print("\n\n⚠️  Operación cancelada por el usuario.")
            print("👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"\n❌ Error inesperado: {str(e)}")
            print("🔄 Intentando continuar...")

if __name__ == "__main__":
    main()