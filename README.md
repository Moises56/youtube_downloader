# YouTube Downloader 🎥

Un script en Python para descargar videos de YouTube o extraer solo el audio en formato MP3 utilizando la librería `pytube`.

## 📋 Características

- ✅ Descarga videos completos en formato MP4
- ✅ Extrae solo el audio en formato MP3
- ✅ Interfaz de usuario interactiva
- ✅ Nombres de archivo personalizables
- ✅ Manejo robusto de errores
- ✅ Validación de URLs
- ✅ Información detallada del video
- ✅ Organización automática en carpeta "downloads"

## 🚀 Instalación

### Prerrequisitos

- Python 3.6 o superior
- pip (gestor de paquetes de Python)

### Instalar dependencias

```bash
pip install pytube
```

**Nota:** Si experimentas problemas con `pytube`, puedes probar con la versión de desarrollo:

```bash
pip install git+https://github.com/pytube/pytube.git
```

## 📖 Uso

### Ejecutar el script

```bash
python youtube_downloader.py
```

### Flujo de uso

1. **Seleccionar tipo de descarga:**
   - Opción 1: Solo audio (MP3)
   - Opción 2: Video completo (MP4)
   - Opción 3: Salir

2. **Ingresar URL del video:**
   - Pega la URL completa del video de YouTube
   - Ejemplo: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`

3. **Nombre personalizado (opcional):**
   - Puedes asignar un nombre personalizado al archivo
   - Si no ingresas nada, se usará el título original del video

4. **Descarga automática:**
   - El archivo se guardará en la carpeta `downloads`
   - Se mostrará el progreso y confirmación de descarga

## 📁 Estructura de archivos

```
mp3Youtube/
├── youtube_downloader.py    # Script principal
├── README.md               # Este archivo
└── downloads/              # Carpeta de descargas (se crea automáticamente)
    ├── video1.mp4
    ├── audio1.mp3
    └── ...
```

## 🔧 Funcionalidades técnicas

### Validación de URLs

El script valida automáticamente que la URL proporcionada sea de YouTube, aceptando formatos como:
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://youtube.com/watch?v=VIDEO_ID`

### Manejo de errores

El script maneja los siguientes tipos de errores:
- ❌ URLs inválidas
- ❌ Videos no disponibles
- ❌ Transmisiones en vivo
- ❌ Problemas de conexión
- ❌ Caracteres inválidos en nombres de archivo

### Limpieza de nombres

Los nombres de archivo se limpian automáticamente removiendo caracteres no válidos:
- `< > : " / \ | ? *`

## 📊 Información del video

Antes de la descarga, el script muestra:
- 📹 Título del video
- 👤 Autor/Canal
- ⏱️ Duración
- 👀 Número de visualizaciones
- 🎵 Calidad de audio disponible
- 🎬 Resolución de video disponible
- 📁 Tamaño aproximado del archivo

## 🐛 Solución de problemas

### ⚠️ Error HTTP 400: Bad Request (Problema común)

Este es el error más frecuente con pytube. **Solución automática:**

```bash
python solucion_error_400.py
```

O manualmente:

1. **Actualizar pytube:**
   ```bash
   pip install --upgrade pytube
   ```

2. **Instalar versión de desarrollo:**
   ```bash
   pip install git+https://github.com/pytube/pytube.git
   ```

3. **Usar yt-dlp como alternativa (recomendado):**
   ```bash
   pip install yt-dlp
   ```
   El script detectará automáticamente yt-dlp y lo usará si pytube falla.

### Error: "No module named 'pytube'"

```bash
pip install pytube
```

### Error: "RegexMatchError" o problemas con pytube

Prueba instalando la versión de desarrollo:

```bash
pip uninstall pytube
pip install git+https://github.com/pytube/pytube.git
```

### Videos no disponibles

Algunos videos pueden no estar disponibles debido a:
- Restricciones geográficas
- Videos privados
- Videos eliminados
- Restricciones de edad

### Problemas de conexión

- Verifica tu conexión a internet
- Algunos firewalls pueden bloquear las descargas
- Intenta con una VPN si hay restricciones regionales

### Script de diagnóstico

Usa <mcfile name="solucion_error_400.py" path="c:\Users\GIS-MOISES\Desktop\WEBAPPS\EU\dist\mp3Youtube\solucion_error_400.py"></mcfile> para:
- 🔍 Diagnosticar problemas automáticamente
- 🔄 Actualizar librerías
- 📦 Instalar alternativas
- 🧪 Probar funcionalidad

## ⚖️ Consideraciones legales

- ✅ Usa este script solo para contenido del cual tengas derechos
- ✅ Respeta los términos de servicio de YouTube
- ✅ No redistribuyas contenido con derechos de autor
- ✅ Úsalo solo para fines educativos y personales

## 🔄 Actualizaciones

Para mantener el script funcionando correctamente:

```bash
pip install --upgrade pytube
```

## 📝 Notas adicionales

- Los archivos de audio se guardan con extensión `.mp3` pero mantienen el formato original (generalmente MP4/WebM)
- Para conversión real a MP3, considera instalar `ffmpeg` y `pydub`
- El script selecciona automáticamente la mejor calidad disponible
- Los videos progresivos (video + audio) tienen mejor compatibilidad

## 🤝 Contribuciones

Este es un script educativo. Siéntete libre de:
- Reportar bugs
- Sugerir mejoras
- Hacer fork del proyecto
- Contribuir con nuevas características

---

**Desarrollado con fines educativos para aprender sobre pytube y descarga de contenido multimedia.**