// ============================================
// CONFIGURACIÓN Y UTILIDADES
// ============================================

const Utils = {
    // Formatear tiempo (HH:MM)
    getTime() {
        const now = new Date();
        return `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;
    },

    // Escapar HTML para prevenir XSS
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    },

    // Auto-eliminar notificaciones
    autoRemoveNotifications() {
        const container = document.getElementById('notification-container');
        if (!container) return;

        setTimeout(() => {
            container.style.opacity = '0';
            container.style.transition = 'opacity 0.3s ease';
            setTimeout(() => container.remove(), 300);
        }, 5000);
    }
};

// ============================================
// NAVBAR - Efectos de Scroll
// ============================================

class NavbarController {
    constructor() {
        this.navbar = document.querySelector('.navbar');
        this.init();
    }

    init() {
        if (!this.navbar) return;
        window.addEventListener('scroll', () => this.handleScroll());
    }

    handleScroll() {
        if (window.pageYOffset > 10) {
            this.navbar.classList.add('scrolled');
        } else {
            this.navbar.classList.remove('scrolled');
        }
    }
}

// ============================================
// BÚSQUEDA DE CANALES
// ============================================

class SearchController {
    constructor() {
        this.input = document.getElementById('searchInput');
        this.init();
    }

    init() {
        if (!this.input) return;

        // Enter para buscar
        this.input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.performSearch();
            }
        });
    }

    performSearch() {
        const query = this.input.value.trim();
        if (!query) return;

        // Redirigir a la búsqueda
        window.location.href = `/search/?q=${encodeURIComponent(query)}`;
    }
}

// ============================================
// VIDEO PLAYER CON HLS
// ============================================

class VideoPlayer {
    constructor() {
        this.video = document.getElementById('videoPlayer');
        this.statusOverlay = document.getElementById('streamStatus');
        this.config = window.STREAM_CONFIG || {};
        this.hls = null;
        this.init();
    }

    init() {
        if (!this.video || !this.config.hlsUrl) return;

        // Si no está en vivo, mostrar offline
        if (!this.config.isLive) {
            this.setStatus('offline', 'Transmisión no disponible');
            return;
        }

        // Iniciar carga del stream
        this.setStatus('connecting', 'Conectando al stream...');
        this.setupPlayer();
    }

    setupPlayer() {
        if (Hls.isSupported()) {
            this.setupHLS();
        } else if (this.video.canPlayType('application/vnd.apple.mpegurl')) {
            // Safari nativo
            this.video.src = this.config.hlsUrl;
            this.video.addEventListener('loadedmetadata', () => {
                this.hideStatus();
            });
        } else {
            this.setStatus('error', 'Tu navegador no soporta streaming HLS');
        }
    }

    setupHLS() {
        this.hls = new Hls({
            enableWorker: true,
            lowLatencyMode: true,
            liveSyncDurationCount: 3,
            liveMaxLatencyDurationCount: 10,
            maxBufferLength: 30,
            maxMaxBufferLength: 60,
            manifestLoadingMaxRetry: 5,
            manifestLoadingRetryDelay: 1000,
            levelLoadingMaxRetry: 4
        });

        this.hls.loadSource(this.config.hlsUrl);
        this.hls.attachMedia(this.video);

        // Eventos HLS
        this.hls.on(Hls.Events.MANIFEST_PARSED, () => {
            this.hideStatus();
            this.video.play().catch(() => {
                // Auto-play bloqueado, esperamos interacción del usuario
            });
        });

        this.hls.on(Hls.Events.ERROR, (event, data) => {
            this.handleError(data);
        });
    }

    handleError(data) {
        if (!data.fatal) return;

        console.error('HLS Error:', data);

        switch (data.type) {
            case Hls.ErrorTypes.NETWORK_ERROR:
                this.setStatus('reconnecting', 'Reconectando...');
                setTimeout(() => {
                    if (this.hls) {
                        this.hls.startLoad();
                    }
                }, 2000);
                break;

            case Hls.ErrorTypes.MEDIA_ERROR:
                this.setStatus('reconnecting', 'Recuperando stream...');
                if (this.hls) {
                    this.hls.recoverMediaError();
                }
                break;

            default:
                this.setStatus('error', 'Error al cargar el stream');
                // Reintentar después de 5 segundos
                setTimeout(() => {
                    if (this.hls) {
                        this.hls.destroy();
                        this.setupHLS();
                    }
                }, 5000);
                break;
        }
    }

    setStatus(type, message) {
        if (!this.statusOverlay) return;

        const statusText = this.statusOverlay.querySelector('.status-text');
        const spinner = this.statusOverlay.querySelector('.status-spinner');

        if (statusText) {
            statusText.textContent = message;
        }

        // Mostrar/ocultar spinner según el tipo
        if (spinner) {
            spinner.style.display = (type === 'connecting' || type === 'reconnecting') ? 'block' : 'none';
        }

        this.statusOverlay.classList.remove('hidden');
    }

    hideStatus() {
        if (this.statusOverlay) {
            this.statusOverlay.classList.add('hidden');
        }
    }

    destroy() {
        if (this.hls) {
            this.hls.destroy();
            this.hls = null;
        }
    }
}

// ============================================
// CHAT EN VIVO
// ============================================

class ChatManager {
    constructor() {
        this.messagesContainer = document.getElementById('chatMessages');
        this.input = document.getElementById('chatInput');
        this.sendBtn = document.getElementById('chatSendBtn');
        this.charCount = document.getElementById('charCount');
        this.config = window.STREAM_CONFIG || {};
        this.init();
    }

    init() {
        if (!this.input || !this.sendBtn || !this.messagesContainer) return;

        // Event Listeners
        this.input.addEventListener('input', () => this.updateCharCount());
        this.input.addEventListener('keydown', (e) => this.handleKeyPress(e));
        this.sendBtn.addEventListener('click', () => this.sendMessage());

        // Auto-resize del textarea
        this.input.addEventListener('input', () => {
            this.input.style.height = 'auto';
            this.input.style.height = Math.min(this.input.scrollHeight, 120) + 'px';
        });

        // Mensaje de bienvenida
        setTimeout(() => {
            const welcomeMsg = this.config.isHome 
                ? '¡Bienvenido al chat oficial de Kaircam!'
                : `¡Bienvenido al chat de ${this.config.streamName}!`;
            
            this.addMessage({
                author: 'Sistema',
                text: welcomeMsg,
                isAdmin: true
            });
        }, 500);
    }

    updateCharCount() {
        const length = this.input.value.length;
        this.charCount.textContent = length;
        
        // Cambiar color si se acerca al límite
        if (length > 450) {
            this.charCount.style.color = 'var(--accent-red)';
        } else {
            this.charCount.style.color = 'var(--text-muted)';
        }
    }

    handleKeyPress(e) {
        // Enter sin Shift envía el mensaje
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            this.sendMessage();
        }
    }

    sendMessage() {
        const text = this.input.value.trim();
        
        // Validaciones
        if (!text || text.length > 500) return;

        // Añadir mensaje
        this.addMessage({
            author: 'Tú',
            text: text,
            isAdmin: false
        });

        // Limpiar input
        this.input.value = '';
        this.input.style.height = 'auto';
        this.updateCharCount();
    }

    addMessage(data) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message${data.isAdmin ? ' admin-message' : ''}`;
        
        const time = Utils.getTime();
        
        messageDiv.innerHTML = `
            <div class="message-header">
                <span class="message-author">${Utils.escapeHtml(data.author)}</span>
                <span class="message-time">${time}</span>
            </div>
            <p class="message-text">${Utils.escapeHtml(data.text)}</p>
        `;

        this.messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }

    scrollToBottom() {
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }
}

// ============================================
// INICIALIZACIÓN
// ============================================

class App {
    constructor() {
        this.navbar = null;
        this.search = null;
        this.videoPlayer = null;
        this.chat = null;
        this.init();
    }

    init() {
        // Esperar a que el DOM esté listo
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.start());
        } else {
            this.start();
        }
    }

    start() {
        // Inicializar componentes globales
        this.navbar = new NavbarController();
        this.search = new SearchController();

        // Auto-eliminar notificaciones
        Utils.autoRemoveNotifications();

        // Componentes específicos de la página de stream
        if (window.STREAM_CONFIG) {
            this.videoPlayer = new VideoPlayer();
            this.chat = new ChatManager();
        }

        console.log('✅ Kaircam inicializado correctamente');
    }

    destroy() {
        if (this.videoPlayer) {
            this.videoPlayer.destroy();
        }
    }
}

// Iniciar aplicación
const app = new App();

// Limpiar al salir de la página
window.addEventListener('beforeunload', () => {
    app.destroy();
});