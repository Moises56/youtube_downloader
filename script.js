// YouTube Downloader - Frontend JavaScript

class YouTubeDownloader {
    constructor() {
        this.currentDownload = null;
        this.downloadInterval = null;
        this.currentVideoInfo = null;
        this.init();
    }

    validateDownloadPath(path) {
        // Validación básica de ruta en Windows
        const windowsPathRegex = /^[a-zA-Z]:\\(?:[^\\/:*?"<>|\r\n]+\\)*[^\\/:*?"<>|\r\n]*$/;
        
        if (windowsPathRegex.test(path)) {
            this.showToast('Ruta válida configurada', 'success', 2000);
        } else {
            this.showToast('Formato de ruta inválido. Usa formato Windows: C:\\carpeta\\subcarpeta', 'warning', 4000);
        }
    }

    init() {
        this.bindEvents();
        this.setupToastContainer();
    }

    bindEvents() {
        // URL Input and Analysis
        const urlInput = document.getElementById('urlInput');
        const analyzeBtn = document.getElementById('analyzeBtn');
        
        urlInput.addEventListener('input', () => this.validateURL());
        urlInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.analyzeURL();
            }
        });
        
        analyzeBtn.addEventListener('click', () => this.analyzeURL());

        // Format Toggle
        const formatBtns = document.querySelectorAll('.format-btn');
        formatBtns.forEach(btn => {
            btn.addEventListener('click', () => this.toggleFormat(btn.dataset.format));
        });

        // Download Button
        const downloadBtn = document.getElementById('downloadBtn');
        downloadBtn.addEventListener('click', () => this.startDownload());

        // Cancel Button
        const cancelBtn = document.getElementById('cancelBtn');
        cancelBtn.addEventListener('click', () => this.cancelDownload());

        // Path Selection
        const selectPathBtn = document.getElementById('selectPathBtn');
        selectPathBtn.addEventListener('click', () => this.selectDownloadPath());

        // Success Actions
        const downloadAnotherBtn = document.getElementById('downloadAnotherBtn');
        const openFolderBtn = document.getElementById('openFolderBtn');
        
        downloadAnotherBtn.addEventListener('click', () => this.resetInterface());
        openFolderBtn.addEventListener('click', () => this.openDownloadFolder());
    }

    validateURL() {
        const urlInput = document.getElementById('urlInput');
        const validation = document.getElementById('urlValidation');
        const url = urlInput.value.trim();

        if (!url) {
            validation.style.display = 'none';
            return false;
        }

        const youtubeRegex = /^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+/;
        
        if (youtubeRegex.test(url)) {
            validation.className = 'url-validation success';
            validation.innerHTML = '<i class="fas fa-check-circle"></i> URL de YouTube válida';
            return true;
        } else {
            validation.className = 'url-validation error';
            validation.innerHTML = '<i class="fas fa-exclamation-circle"></i> Por favor, ingresa una URL válida de YouTube';
            return false;
        }
    }

    async analyzeURL() {
        if (!this.validateURL()) {
            this.showToast('Por favor, ingresa una URL válida de YouTube', 'error');
            return;
        }

        const url = document.getElementById('urlInput').value.trim();
        this.showLoading(true);

        try {
            const response = await fetch('http://localhost:5000/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url })
            });

            const data = await response.json();

            if (data.success) {
                this.currentVideoInfo = data.info;
                this.displayVideoInfo(data.info);
                this.showDownloadOptions(data.info);
                this.showToast('Video analizado correctamente', 'success');
            } else {
                this.showToast(data.error || 'Error al analizar el video', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            this.showToast('Error de conexión. Verifica que el servidor esté ejecutándose.', 'error');
        } finally {
            this.showLoading(false);
        }
    }

    displayVideoInfo(info) {
        const videoInfo = document.getElementById('videoInfo');
        const thumbnail = document.getElementById('videoThumbnail');
        const title = document.getElementById('videoTitle');
        const channel = document.getElementById('videoChannel');
        const duration = document.getElementById('videoDuration');
        const views = document.getElementById('videoViews');
        const date = document.getElementById('videoDate');

        // Set video information
        thumbnail.src = info.thumbnail || 'https://via.placeholder.com/200x112?text=No+Image';
        thumbnail.alt = info.title || 'Video thumbnail';
        title.textContent = info.title || 'Título no disponible';
        channel.textContent = info.uploader || 'Canal no disponible';
        duration.textContent = this.formatDuration(info.duration);
        views.textContent = this.formatNumber(info.view_count) + ' visualizaciones';
        date.textContent = this.formatDate(info.upload_date);

        // Show playlist options if it's a playlist
        const playlistOptions = document.getElementById('playlistOptions');
        const playlistDescription = document.getElementById('playlistDescription');
        
        if (info.is_playlist) {
            playlistDescription.textContent = `Esta playlist contiene ${info.playlist_count || 'varios'} videos`;
            playlistOptions.style.display = 'block';
        } else {
            playlistOptions.style.display = 'none';
        }

        videoInfo.style.display = 'block';
    }

    showDownloadOptions(info) {
        const downloadOptions = document.getElementById('downloadOptions');
        downloadOptions.style.display = 'block';
        
        // Store video info for download
        this.currentVideoInfo = info;
    }

    async selectDownloadPath() {
        try {
            // Intentar usar la File System Access API si está disponible
            if ('showDirectoryPicker' in window) {
                const directoryHandle = await window.showDirectoryPicker();
                const pathInput = document.getElementById('downloadPath');
                
                // Guardar el handle para uso posterior
                this.selectedDirectoryHandle = directoryHandle;
                
                // Mostrar el nombre de la carpeta seleccionada
                pathInput.value = directoryHandle.name;
                pathInput.setAttribute('data-full-path', 'selected');
                
                this.showToast(`Carpeta seleccionada: ${directoryHandle.name}`, 'success', 3000);
                return;
            }
        } catch (error) {
            if (error.name !== 'AbortError') {
                console.log('File System Access API no disponible o error:', error);
            }
        }
        
        // Fallback: permitir entrada manual de ruta
        const pathInput = document.getElementById('downloadPath');
        pathInput.readOnly = false;
        pathInput.placeholder = 'Ingresa la ruta completa de la carpeta (ej: C:\\Users\\Usuario\\Downloads)';
        pathInput.focus();
        
        this.showToast('Ingresa manualmente la ruta de la carpeta donde deseas guardar los archivos', 'info', 5000);
        
        // Agregar evento para validar la ruta cuando el usuario termine de escribir
        pathInput.addEventListener('blur', () => {
            const path = pathInput.value.trim();
            if (path) {
                this.validateDownloadPath(path);
            }
            pathInput.readOnly = true;
        }, { once: true });
    }

    toggleFormat(format) {
        const formatBtns = document.querySelectorAll('.format-btn');
        const audioOptions = document.getElementById('audioOptions');
        const videoOptions = document.getElementById('videoOptions');

        // Update button states
        formatBtns.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.format === format);
        });

        // Show/hide options
        if (format === 'audio') {
            audioOptions.classList.add('active');
            videoOptions.classList.remove('active');
        } else {
            videoOptions.classList.add('active');
            audioOptions.classList.remove('active');
        }
    }

    async startDownload() {
        if (!this.currentVideoInfo) {
            this.showToast('Primero debes analizar un video', 'error');
            return;
        }

        const url = document.getElementById('urlInput').value.trim();
        const activeFormat = document.querySelector('.format-btn.active').dataset.format;
        const quality = document.getElementById(activeFormat === 'audio' ? 'audioQuality' : 'videoQuality').value;
        const playlistChoice = document.querySelector('input[name="playlistChoice"]:checked')?.value || 'single';

        const pathInput = document.getElementById('downloadPath');
        let downloadPath = pathInput.value.trim();
        
        // Si se usó File System Access API, intentar obtener la ruta real
        if (this.selectedDirectoryHandle && pathInput.getAttribute('data-full-path') === 'selected') {
            try {
                // Para File System Access API, necesitamos manejar esto de manera especial
                // Por ahora, usaremos el nombre de la carpeta y dejaremos que el backend maneje el fallback
                downloadPath = `FSAPI:${this.selectedDirectoryHandle.name}`;
            } catch (error) {
                console.log('Error accediendo al directoryHandle:', error);
                downloadPath = pathInput.value.trim();
            }
        }
        
        const downloadData = {
            url,
            format: activeFormat,
            quality,
            playlist: playlistChoice === 'all',
            download_path: downloadPath || null
        };

        try {
            const response = await fetch('http://localhost:5000/api/download', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(downloadData)
            });

            const data = await response.json();

            if (data.success) {
                this.currentDownload = data.download_id;
                this.showProgressSection();
                this.startProgressTracking();
                this.showToast('Descarga iniciada', 'success');
            } else {
                this.showToast(data.error || 'Error al iniciar la descarga', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            this.showToast('Error de conexión', 'error');
        }
    }

    showProgressSection() {
        document.getElementById('downloadOptions').style.display = 'none';
        document.getElementById('progressSection').style.display = 'block';
    }

    startProgressTracking() {
        this.downloadInterval = setInterval(async () => {
            if (!this.currentDownload) return;

            try {
                const response = await fetch(`http://localhost:5000/api/progress/${this.currentDownload}`);
                const data = await response.json();

                if (data.success) {
                    this.updateProgress(data.progress);
                    
                    if (data.progress.status === 'completed') {
                        this.downloadCompleted(data.progress);
                    } else if (data.progress.status === 'error') {
                        this.downloadError(data.progress.error);
                    }
                }
            } catch (error) {
                console.error('Error tracking progress:', error);
            }
        }, 1000);
    }

    updateProgress(progress) {
        const statusText = document.getElementById('status-text');
        const progressText = document.getElementById('progress-text');
        const speedText = document.getElementById('speed-text');
        const etaText = document.getElementById('eta-text');
        const progressFill = document.getElementById('progressFill');
        const downloadSpeed = document.getElementById('downloadSpeed');
        const timeRemaining = document.getElementById('timeRemaining');

        // Actualizar elementos principales de progreso
        if (statusText) statusText.textContent = progress.status_text || 'Descargando...';
        if (progressText) progressText.textContent = `${Math.round(progress.percentage || 0)}%`;
        if (speedText) speedText.textContent = progress.speed || '--';
        if (etaText) etaText.textContent = progress.eta || '--';
        if (progressFill) progressFill.style.width = `${progress.percentage || 0}%`;
        
        // Actualizar elementos de estadísticas (compatibilidad)
        if (downloadSpeed) downloadSpeed.textContent = progress.speed || '-- KB/s';
        if (timeRemaining) timeRemaining.textContent = progress.eta || '--:--';
    }

    downloadCompleted(progress) {
        clearInterval(this.downloadInterval);
        this.currentDownload = null;
        
        document.getElementById('progressSection').style.display = 'none';
        document.getElementById('successSection').style.display = 'block';
        
        const successMessage = document.getElementById('successMessage');
        successMessage.textContent = progress.filename ? 
            `Archivo descargado: ${progress.filename}` : 
            'Tu archivo se ha descargado correctamente.';
        
        this.showToast('¡Descarga completada!', 'success');
    }

    downloadError(error) {
        clearInterval(this.downloadInterval);
        this.currentDownload = null;
        
        document.getElementById('progressSection').style.display = 'none';
        this.showToast(`Error en la descarga: ${error}`, 'error');
    }

    async cancelDownload() {
        if (!this.currentDownload) return;

        try {
            await fetch(`http://localhost:5000/api/cancel/${this.currentDownload}`, {
                method: 'POST'
            });
            
            clearInterval(this.downloadInterval);
            this.currentDownload = null;
            
            document.getElementById('progressSection').style.display = 'none';
            document.getElementById('downloadOptions').style.display = 'block';
            
            this.showToast('Descarga cancelada', 'warning');
        } catch (error) {
            console.error('Error canceling download:', error);
            this.showToast('Error al cancelar la descarga', 'error');
        }
    }

    resetInterface() {
        // Hide all sections except URL input
        document.getElementById('videoInfo').style.display = 'none';
        document.getElementById('downloadOptions').style.display = 'none';
        document.getElementById('progressSection').style.display = 'none';
        document.getElementById('successSection').style.display = 'none';
        
        // Clear URL input
        document.getElementById('urlInput').value = '';
        document.getElementById('urlValidation').style.display = 'none';
        
        // Reset format to audio
        this.toggleFormat('audio');
        
        // Clear stored data
        this.currentVideoInfo = null;
        this.currentDownload = null;
        
        if (this.downloadInterval) {
            clearInterval(this.downloadInterval);
        }
    }

    async openDownloadFolder() {
        try {
            const response = await fetch('http://localhost:5000/api/open-folder', {
                method: 'POST'
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.showToast('Carpeta de descargas abierta', 'success');
            } else {
                this.showToast('Error al abrir carpeta', 'error');
            }
        } catch (error) {
            console.error('Error opening folder:', error);
            this.showToast('No se pudo abrir la carpeta de descargas', 'error');
        }
    }

    showLoading(show) {
        const overlay = document.getElementById('loadingOverlay');
        overlay.style.display = show ? 'flex' : 'none';
    }

    setupToastContainer() {
        if (!document.getElementById('toastContainer')) {
            const container = document.createElement('div');
            container.id = 'toastContainer';
            container.className = 'toast-container';
            document.body.appendChild(container);
        }
    }

    showToast(message, type = 'info', duration = 5000) {
        const container = document.getElementById('toastContainer');
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        
        const icon = {
            success: 'fas fa-check-circle',
            error: 'fas fa-exclamation-circle',
            warning: 'fas fa-exclamation-triangle',
            info: 'fas fa-info-circle'
        }[type] || 'fas fa-info-circle';
        
        // Para mensajes largos, usar formato de texto preformateado
        const messageContent = message.includes('\n') ? 
            `<pre style="white-space: pre-wrap; margin: 0; font-family: inherit;">${message}</pre>` : 
            `<span>${message}</span>`;
        
        toast.innerHTML = `
            <i class="${icon}"></i>
            ${messageContent}
        `;
        
        container.appendChild(toast);
        
        // Auto remove after specified duration
        setTimeout(() => {
            if (toast.parentNode) {
                toast.style.animation = 'slideOutRight 0.3s ease-out';
                setTimeout(() => {
                    if (toast.parentNode) {
                        container.removeChild(toast);
                    }
                }, 300);
            }
        }, duration);
    }

    // Función para ocultar información del video
    hideVideoInfo() {
        const videoInfoSection = document.getElementById('videoInfoSection');
        const downloadOptionsSection = document.getElementById('downloadOptionsSection');
        
        if (videoInfoSection) {
            videoInfoSection.style.display = 'none';
        }
        if (downloadOptionsSection) {
            downloadOptionsSection.style.display = 'none';
        }
        
        this.currentVideoInfo = null;
    }

    // Utility functions
    formatDuration(seconds) {
        if (!seconds) return 'N/A';
        
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = seconds % 60;
        
        if (hours > 0) {
            return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        } else {
            return `${minutes}:${secs.toString().padStart(2, '0')}`;
        }
    }

    formatNumber(num) {
        if (!num) return '0';
        
        if (num >= 1000000) {
            return (num / 1000000).toFixed(1) + 'M';
        } else if (num >= 1000) {
            return (num / 1000).toFixed(1) + 'K';
        } else {
            return num.toString();
        }
    }

    formatDate(dateString) {
        if (!dateString) return 'N/A';
        
        try {
            // YouTube date format: YYYYMMDD
            const year = dateString.substring(0, 4);
            const month = dateString.substring(4, 6);
            const day = dateString.substring(6, 8);
            
            const date = new Date(year, month - 1, day);
            return date.toLocaleDateString('es-ES', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });
        } catch (error) {
            return dateString;
        }
    }
}

// Additional CSS animations for toast removal
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOutRight {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(100%);
        }
    }
`;
document.head.appendChild(style);

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new YouTubeDownloader();
});

// Handle page visibility changes to pause/resume progress tracking
document.addEventListener('visibilitychange', () => {
    const downloader = window.youtubeDownloader;
    if (downloader && downloader.downloadInterval) {
        if (document.hidden) {
            // Page is hidden, could pause tracking
        } else {
            // Page is visible again, resume tracking
        }
    }
});