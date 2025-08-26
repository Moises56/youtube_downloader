#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Solución para Error HTTP 400: Bad Request en pytube
==================================================

Este script proporciona soluciones alternativas cuando pytube falla con errores HTTP.
Incluye instalación automática de yt-dlp como respaldo.

Autor: Script de solución
Fecha: 2024
"""

import subprocess
import sys
import os

def instalar_paquete(paquete):
    """
    Instala un paquete usando pip.
    
    Args:
        paquete (str): Nombre del paquete a instalar
    """
    try:
        print(f"📦 Instalando {paquete}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", paquete])
        print(f"✅ {paquete} instalado exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando {paquete}: {e}")
        return False

def verificar_pytube():
    """
    Verifica si pytube está funcionando correctamente.
    
    Returns:
        bool: True si funciona, False si no
    """
    try:
        from pytube import YouTube
        # Probar con un video conocido
        test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        yt = YouTube(test_url)
        title = yt.title
        print(f"✅ pytube funciona correctamente. Video de prueba: {title}")
        return True
    except Exception as e:
        print(f"❌ pytube no funciona: {str(e)}")
        return False

def verificar_ytdlp():
    """
    Verifica si yt-dlp está funcionando correctamente.
    
    Returns:
        bool: True si funciona, False si no
    """
    try:
        import yt_dlp
        # Probar con un video conocido
        test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        ydl_opts = {'quiet': True, 'no_warnings': True}
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(test_url, download=False)
            title = info.get('title', 'N/A')
            print(f"✅ yt-dlp funciona correctamente. Video de prueba: {title}")
            return True
    except Exception as e:
        print(f"❌ yt-dlp no funciona: {str(e)}")
        return False

def actualizar_pytube():
    """
    Actualiza pytube a la última versión.
    
    Returns:
        bool: True si se actualizó exitosamente
    """
    try:
        print("🔄 Actualizando pytube...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pytube"])
        print("✅ pytube actualizado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error actualizando pytube: {e}")
        return False

def instalar_version_desarrollo_pytube():
    """
    Instala la versión de desarrollo de pytube desde GitHub.
    
    Returns:
        bool: True si se instaló exitosamente
    """
    try:
        print("🔄 Instalando versión de desarrollo de pytube...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "git+https://github.com/pytube/pytube.git"
        ])
        print("✅ Versión de desarrollo de pytube instalada")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando versión de desarrollo: {e}")
        return False

def diagnosticar_problema():
    """
    Diagnostica el problema y sugiere soluciones.
    """
    print("🔍 DIAGNÓSTICO DEL PROBLEMA")
    print("="*50)
    
    # Verificar Python
    print(f"🐍 Versión de Python: {sys.version}")
    
    # Verificar si pytube está instalado
    try:
        import pytube
        print(f"📦 pytube versión: {pytube.__version__}")
    except ImportError:
        print("❌ pytube no está instalado")
    except AttributeError:
        print("📦 pytube instalado (versión no disponible)")
    
    # Verificar si yt-dlp está instalado
    try:
        import yt_dlp
        print(f"📦 yt-dlp versión: {yt_dlp.version.__version__}")
    except ImportError:
        print("❌ yt-dlp no está instalado")
    except AttributeError:
        print("📦 yt-dlp instalado (versión no disponible)")
    
    print("\n🔧 PROBANDO FUNCIONALIDAD...")
    print("-"*30)
    
    pytube_funciona = verificar_pytube()
    ytdlp_funciona = verificar_ytdlp()
    
    print("\n💡 RECOMENDACIONES:")
    print("-"*20)
    
    if not pytube_funciona and not ytdlp_funciona:
        print("🚨 Ninguna librería funciona. Soluciones sugeridas:")
        print("   1. Actualizar pytube")
        print("   2. Instalar yt-dlp como alternativa")
        print("   3. Verificar conexión a internet")
        print("   4. Verificar firewall/proxy")
    elif pytube_funciona:
        print("✅ pytube funciona correctamente")
    elif ytdlp_funciona:
        print("✅ yt-dlp funciona correctamente")
        print("💡 Usa el script principal que automáticamente usará yt-dlp")
    
def menu_solucion():
    """
    Menú interactivo para solucionar problemas.
    """
    while True:
        print("\n" + "="*60)
        print("🛠️  SOLUCIONADOR DE PROBLEMAS - YOUTUBE DOWNLOADER")
        print("="*60)
        print("1. 🔍 Diagnosticar problema")
        print("2. 🔄 Actualizar pytube")
        print("3. 🚀 Instalar versión de desarrollo de pytube")
        print("4. 📦 Instalar yt-dlp como alternativa")
        print("5. 🧪 Probar pytube")
        print("6. 🧪 Probar yt-dlp")
        print("7. 📋 Mostrar información del sistema")
        print("8. ❌ Salir")
        print("="*60)
        
        opcion = input("\nElige una opción (1-8): ").strip()
        
        if opcion == '8':
            print("👋 ¡Hasta luego!")
            break
        elif opcion == '1':
            diagnosticar_problema()
        elif opcion == '2':
            actualizar_pytube()
        elif opcion == '3':
            instalar_version_desarrollo_pytube()
        elif opcion == '4':
            instalar_paquete("yt-dlp")
        elif opcion == '5':
            verificar_pytube()
        elif opcion == '6':
            verificar_ytdlp()
        elif opcion == '7':
            mostrar_info_sistema()
        else:
            print("❌ Opción no válida")
        
        input("\n⏸️  Presiona Enter para continuar...")

def mostrar_info_sistema():
    """
    Muestra información del sistema.
    """
    print("\n💻 INFORMACIÓN DEL SISTEMA")
    print("="*40)
    print(f"🐍 Python: {sys.version}")
    print(f"📁 Directorio actual: {os.getcwd()}")
    print(f"🖥️  Plataforma: {sys.platform}")
    
    # Verificar pip
    try:
        import pip
        print(f"📦 pip disponible")
    except ImportError:
        print("❌ pip no disponible")
    
    # Verificar git (para versión de desarrollo)
    try:
        result = subprocess.run(['git', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"🔧 Git: {result.stdout.strip()}")
        else:
            print("❌ Git no disponible")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ Git no disponible")

def solucion_rapida():
    """
    Aplica soluciones rápidas automáticamente.
    """
    print("🚀 APLICANDO SOLUCIONES RÁPIDAS...")
    print("="*40)
    
    # 1. Intentar actualizar pytube
    print("\n1️⃣ Actualizando pytube...")
    if actualizar_pytube():
        if verificar_pytube():
            print("✅ Problema resuelto con actualización de pytube")
            return True
    
    # 2. Intentar versión de desarrollo
    print("\n2️⃣ Probando versión de desarrollo de pytube...")
    if instalar_version_desarrollo_pytube():
        if verificar_pytube():
            print("✅ Problema resuelto con versión de desarrollo")
            return True
    
    # 3. Instalar yt-dlp como alternativa
    print("\n3️⃣ Instalando yt-dlp como alternativa...")
    if instalar_paquete("yt-dlp"):
        if verificar_ytdlp():
            print("✅ yt-dlp instalado y funcionando")
            print("💡 El script principal usará yt-dlp automáticamente")
            return True
    
    print("\n❌ No se pudo resolver automáticamente")
    print("💡 Usa el menú interactivo para más opciones")
    return False

def main():
    """
    Función principal.
    """
    print("🛠️  Solucionador de Problemas - YouTube Downloader")
    print("\n📋 Este script ayuda a resolver el error HTTP 400: Bad Request")
    print("\n¿Qué quieres hacer?")
    print("1. 🚀 Aplicar soluciones rápidas automáticamente")
    print("2. 🔧 Usar menú interactivo")
    print("3. 🔍 Solo diagnosticar")
    
    opcion = input("\nElige una opción (1-3): ").strip()
    
    if opcion == '1':
        solucion_rapida()
    elif opcion == '2':
        menu_solucion()
    elif opcion == '3':
        diagnosticar_problema()
    else:
        print("❌ Opción no válida")
        menu_solucion()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 ¡Hasta luego!")
    except Exception as e:
        print(f"\n❌ Error inesperado: {str(e)}")