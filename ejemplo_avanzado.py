#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejemplo Avanzado de YouTube Downloader
======================================

Este script muestra funcionalidades avanzadas de pytube para fines educativos.
Incluye ejemplos de cómo trabajar con diferentes streams, playlists y metadatos.

Autor: Script educativo
Fecha: 2024
"""

from pytube import YouTube, Playlist
from pytube.exceptions import RegexMatchError, VideoUnavailable
import os

def explorar_streams_disponibles(url):
    """
    Explora y muestra todos los streams disponibles para un video.
    
    Args:
        url (str): URL del video de YouTube
    """
    try:
        yt = YouTube(url)
        print(f"\n🎬 Analizando: {yt.title}")
        print("="*60)
        
        # Mostrar información básica
        print(f"📺 Canal: {yt.author}")
        print(f"📅 Fecha de publicación: {yt.publish_date}")
        print(f"📝 Descripción (primeros 100 chars): {yt.description[:100]}...")
        print(f"🏷️  Tags: {', '.join(yt.keywords[:5]) if yt.keywords else 'No disponibles'}")
        
        print("\n🎵 STREAMS DE AUDIO:")
        print("-" * 40)
        audio_streams = yt.streams.filter(only_audio=True)
        for i, stream in enumerate(audio_streams, 1):
            print(f"{i}. Codec: {stream.audio_codec}, Bitrate: {stream.abr}, Tamaño: {stream.filesize_mb:.1f}MB")
        
        print("\n🎬 STREAMS DE VIDEO (Solo video):")
        print("-" * 40)
        video_only_streams = yt.streams.filter(only_video=True)
        for i, stream in enumerate(video_only_streams, 1):
            print(f"{i}. Resolución: {stream.resolution}, Codec: {stream.video_codec}, FPS: {stream.fps}, Tamaño: {stream.filesize_mb:.1f}MB")
        
        print("\n🎭 STREAMS PROGRESIVOS (Video + Audio):")
        print("-" * 40)
        progressive_streams = yt.streams.filter(progressive=True)
        for i, stream in enumerate(progressive_streams, 1):
            print(f"{i}. Resolución: {stream.resolution}, Codec: {stream.video_codec}, Tamaño: {stream.filesize_mb:.1f}MB")
        
        print("\n📊 STREAMS ADAPTATIVOS (Mejor calidad):")
        print("-" * 40)
        adaptive_streams = yt.streams.filter(adaptive=True)
        for i, stream in enumerate(adaptive_streams[:10], 1):  # Mostrar solo los primeros 10
            tipo = "🎵 Audio" if stream.includes_audio_track and not stream.includes_video_track else "🎬 Video"
            print(f"{i}. {tipo} - Resolución: {stream.resolution}, Codec: {stream.video_codec or stream.audio_codec}, Tamaño: {stream.filesize_mb:.1f}MB")
        
    except Exception as e:
        print(f"❌ Error al analizar el video: {str(e)}")

def descargar_playlist_ejemplo(playlist_url, limite=3):
    """
    Ejemplo de cómo descargar videos de una playlist.
    
    Args:
        playlist_url (str): URL de la playlist
        limite (int): Número máximo de videos a descargar
    """
    try:
        print(f"\n📋 Analizando playlist...")
        playlist = Playlist(playlist_url)
        
        print(f"📋 Título de la playlist: {playlist.title}")
        print(f"👤 Propietario: {playlist.owner}")
        print(f"📊 Total de videos: {len(playlist.video_urls)}")
        
        carpeta_playlist = os.path.join("downloads", "playlist")
        if not os.path.exists(carpeta_playlist):
            os.makedirs(carpeta_playlist)
        
        print(f"\n⬇️  Descargando primeros {limite} videos...")
        
        for i, video_url in enumerate(playlist.video_urls[:limite], 1):
            try:
                print(f"\n🎬 Descargando video {i}/{limite}...")
                yt = YouTube(video_url)
                print(f"📹 {yt.title}")
                
                # Descargar audio de mejor calidad
                audio_stream = yt.streams.filter(only_audio=True).first()
                if audio_stream:
                    archivo = audio_stream.download(
                        output_path=carpeta_playlist,
                        filename=f"{i:02d}_{yt.title[:50]}.mp3"
                    )
                    print(f"✅ Descargado: {os.path.basename(archivo)}")
                
            except Exception as e:
                print(f"❌ Error descargando video {i}: {str(e)}")
                continue
        
        print(f"\n🎉 Descarga de playlist completada en: {carpeta_playlist}")
        
    except Exception as e:
        print(f"❌ Error al procesar la playlist: {str(e)}")

def buscar_calidad_especifica(url, resolucion_deseada="720p"):
    """
    Busca y descarga un video en una resolución específica.
    
    Args:
        url (str): URL del video
        resolucion_deseada (str): Resolución deseada (ej: "720p", "1080p")
    """
    try:
        yt = YouTube(url)
        print(f"\n🎯 Buscando resolución {resolucion_deseada} para: {yt.title}")
        
        # Buscar stream con la resolución específica
        stream_deseado = yt.streams.filter(
            progressive=True, 
            res=resolucion_deseada
        ).first()
        
        if stream_deseado:
            print(f"✅ Encontrado stream en {resolucion_deseada}")
            print(f"📊 Tamaño: {stream_deseado.filesize_mb:.1f}MB")
            
            carpeta_calidad = os.path.join("downloads", "calidad_especifica")
            if not os.path.exists(carpeta_calidad):
                os.makedirs(carpeta_calidad)
            
            archivo = stream_deseado.download(
                output_path=carpeta_calidad,
                filename=f"{yt.title}_{resolucion_deseada}.mp4"
            )
            print(f"✅ Descargado en {resolucion_deseada}: {os.path.basename(archivo)}")
        else:
            print(f"❌ No se encontró stream en {resolucion_deseada}")
            print("📋 Resoluciones disponibles:")
            resoluciones = set()
            for stream in yt.streams.filter(progressive=True):
                if stream.resolution:
                    resoluciones.add(stream.resolution)
            for res in sorted(resoluciones, key=lambda x: int(x[:-1]), reverse=True):
                print(f"   - {res}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def obtener_metadatos_detallados(url):
    """
    Obtiene metadatos detallados de un video sin descargarlo.
    
    Args:
        url (str): URL del video
    """
    try:
        yt = YouTube(url)
        
        print(f"\n📊 METADATOS DETALLADOS")
        print("="*50)
        print(f"📹 Título: {yt.title}")
        print(f"👤 Autor: {yt.author}")
        print(f"📺 Canal ID: {yt.channel_id}")
        print(f"🔗 URL del canal: {yt.channel_url}")
        print(f"⏱️  Duración: {yt.length} segundos ({yt.length//60}:{yt.length%60:02d})")
        print(f"👀 Vistas: {yt.views:,}")
        print(f"📅 Fecha de publicación: {yt.publish_date}")
        print(f"⭐ Rating: {yt.rating if hasattr(yt, 'rating') else 'No disponible'}")
        print(f"🆔 Video ID: {yt.video_id}")
        print(f"🖼️  Thumbnail: {yt.thumbnail_url}")
        
        if yt.keywords:
            print(f"🏷️  Tags: {', '.join(yt.keywords[:10])}")
        
        print(f"\n📝 Descripción (primeros 200 caracteres):")
        print(f"{yt.description[:200]}...")
        
        # Información técnica
        print(f"\n🔧 INFORMACIÓN TÉCNICA:")
        print(f"📊 Total de streams: {len(yt.streams)}")
        print(f"🎵 Streams de audio: {len(yt.streams.filter(only_audio=True))}")
        print(f"🎬 Streams de video: {len(yt.streams.filter(only_video=True))}")
        print(f"🎭 Streams progresivos: {len(yt.streams.filter(progressive=True))}")
        
        # Mejor calidad disponible
        mejor_video = yt.streams.filter(progressive=True).get_highest_resolution()
        mejor_audio = yt.streams.filter(only_audio=True).first()
        
        if mejor_video:
            print(f"🏆 Mejor calidad de video: {mejor_video.resolution} ({mejor_video.filesize_mb:.1f}MB)")
        if mejor_audio:
            print(f"🎵 Mejor calidad de audio: {mejor_audio.abr} ({mejor_audio.filesize_mb:.1f}MB)")
        
    except Exception as e:
        print(f"❌ Error obteniendo metadatos: {str(e)}")

def menu_ejemplos_avanzados():
    """
    Menú interactivo para ejemplos avanzados.
    """
    while True:
        print("\n" + "="*60)
        print("🎓 EJEMPLOS AVANZADOS DE PYTUBE")
        print("="*60)
        print("1. 🔍 Explorar todos los streams disponibles")
        print("2. 📋 Descargar muestra de playlist (3 videos)")
        print("3. 🎯 Buscar calidad específica")
        print("4. 📊 Obtener metadatos detallados")
        print("5. ❌ Volver al menú principal")
        print("="*60)
        
        opcion = input("\nElige una opción (1-5): ").strip()
        
        if opcion == '5':
            break
        
        if opcion in ['1', '3', '4']:
            url = input("\n🔗 Ingresa la URL del video: ").strip()
            if not url:
                print("❌ URL no válida")
                continue
        
        if opcion == '1':
            explorar_streams_disponibles(url)
        elif opcion == '2':
            playlist_url = input("\n🔗 Ingresa la URL de la playlist: ").strip()
            if playlist_url:
                descargar_playlist_ejemplo(playlist_url)
        elif opcion == '3':
            resolucion = input("\n🎯 Resolución deseada (ej: 720p, 1080p): ").strip() or "720p"
            buscar_calidad_especifica(url, resolucion)
        elif opcion == '4':
            obtener_metadatos_detallados(url)
        else:
            print("❌ Opción no válida")
        
        input("\n⏸️  Presiona Enter para continuar...")

if __name__ == "__main__":
    print("🎓 Ejemplos Avanzados de pytube")
    print("Este script muestra funcionalidades avanzadas para fines educativos.")
    print("\n⚠️  Nota: Asegúrate de tener pytube instalado: pip install pytube")
    
    try:
        menu_ejemplos_avanzados()
    except KeyboardInterrupt:
        print("\n\n👋 ¡Hasta luego!")
    except Exception as e:
        print(f"\n❌ Error inesperado: {str(e)}")