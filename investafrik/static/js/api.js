/**
 * API Client pour InvestAfrik
 */

class APIClient {
    constructor() {
        this.baseURL = window.location.origin;
        this.defaultHeaders = {
            'Content-Type': 'application/json',
        };
    }

    /**
     * Obtenir le token d'authentification
     */
    getAuthToken() {
        return localStorage.getItem('access_token');
    }

    /**
     * Obtenir le token CSRF
     */
    getCSRFToken() {
        // Try to get from meta tag first
        let csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
        if (!csrfToken) {
            // Try to get from form
            csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
        }
        if (!csrfToken) {
            // Try to get from cookies
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                const [name, value] = cookie.trim().split('=');
                if (name === 'csrftoken') {
                    csrfToken = value;
                    break;
                }
            }
        }
        return csrfToken;
    }

    /**
     * Obtenir les headers avec authentification
     */
    getHeaders(includeAuth = true) {
        const headers = { ...this.defaultHeaders };
        
        // Always include CSRF token for Django
        const csrfToken = this.getCSRFToken();
        if (csrfToken) {
            headers['X-CSRFToken'] = csrfToken;
        }
        
        if (includeAuth) {
            const token = this.getAuthToken();
            if (token) {
                headers['Authorization'] = `Bearer ${token}`;
            }
        }
        
        return headers;
    }

    /**
     * Effectuer une requête API
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: this.getHeaders(options.includeAuth !== false),
            credentials: 'same-origin', // Include cookies for Django session auth
            ...options
        };

        try {
            const response = await fetch(url, config);
            return response;
        } catch (error) {
            console.error('API Request Error:', error);
            throw error;
        }
    }

    /**
     * Requête GET
     */
    async get(endpoint, options = {}) {
        return this.request(endpoint, {
            method: 'GET',
            ...options
        });
    }

    /**
     * Requête POST
     */
    async post(endpoint, data, options = {}) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data),
            ...options
        });
    }

    /**
     * Requête PUT
     */
    async put(endpoint, data, options = {}) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data),
            ...options
        });
    }

    /**
     * Requête PATCH
     */
    async patch(endpoint, data, options = {}) {
        return this.request(endpoint, {
            method: 'PATCH',
            body: JSON.stringify(data),
            ...options
        });
    }

    /**
     * Requête DELETE
     */
    async delete(endpoint, options = {}) {
        return this.request(endpoint, {
            method: 'DELETE',
            ...options
        });
    }

    /**
     * Vérifier si l'utilisateur est connecté
     */
    isAuthenticated() {
        // Check for JWT token or Django session
        const hasToken = !!this.getAuthToken();
        const hasCSRF = !!this.getCSRFToken();
        
        // If we have CSRF token, we're likely in a Django session
        return hasToken || hasCSRF;
    }

    /**
     * Déconnexion
     */
    logout() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/';
    }
}

// Instance globale de l'API client
const api = new APIClient();

// Utilitaires
const utils = {
    /**
     * Formater une devise
     */
    formatCurrency(amount, currency = 'FCFA') {
        if (typeof amount !== 'number') {
            amount = parseFloat(amount) || 0;
        }
        return new Intl.NumberFormat('fr-FR').format(amount) + ' ' + currency;
    },

    /**
     * Formater une date
     */
    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('fr-FR', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    },

    /**
     * Calculer les jours restants
     */
    daysRemaining(endDate) {
        const end = new Date(endDate);
        const now = new Date();
        const diffTime = end - now;
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        return Math.max(0, diffDays);
    },

    /**
     * Calculer le pourcentage de financement
     */
    fundingPercentage(current, goal) {
        if (!goal || goal === 0) return 0;
        return (current / goal) * 100;
    },

    /**
     * Formater le temps relatif
     */
    formatRelativeTime(dateString) {
        if (!dateString) return '';
        
        const date = new Date(dateString);
        const now = new Date();
        const diffMs = now - date;
        const diffMins = Math.floor(diffMs / 60000);
        const diffHours = Math.floor(diffMs / 3600000);
        const diffDays = Math.floor(diffMs / 86400000);
        
        if (diffMins < 1) return 'À l\'instant';
        if (diffMins < 60) return `${diffMins}min`;
        if (diffHours < 24) return `${diffHours}h`;
        if (diffDays < 7) return `${diffDays}j`;
        
        return date.toLocaleDateString('fr-FR', {
            day: 'numeric',
            month: 'short'
        });
    }
};

// Système de notifications
const notifications = {
    container: null,

    init() {
        if (!this.container) {
            this.container = document.createElement('div');
            this.container.id = 'notifications-container';
            this.container.className = 'fixed top-4 right-4 z-50 space-y-2';
            document.body.appendChild(this.container);
        }
    },

    show(message, type = 'info', duration = 5000) {
        this.init();

        const notification = document.createElement('div');
        notification.className = `
            max-w-sm w-full bg-white shadow-lg rounded-lg pointer-events-auto 
            ring-1 ring-black ring-opacity-5 overflow-hidden transform transition-all duration-300
        `;

        const colors = {
            success: 'bg-green-500',
            error: 'bg-red-500',
            warning: 'bg-yellow-500',
            info: 'bg-blue-500'
        };

        const icons = {
            success: 'fas fa-check-circle',
            error: 'fas fa-exclamation-circle',
            warning: 'fas fa-exclamation-triangle',
            info: 'fas fa-info-circle'
        };

        notification.innerHTML = `
            <div class="p-4">
                <div class="flex items-start">
                    <div class="flex-shrink-0">
                        <i class="${icons[type]} text-${type === 'success' ? 'green' : type === 'error' ? 'red' : type === 'warning' ? 'yellow' : 'blue'}-500"></i>
                    </div>
                    <div class="ml-3 w-0 flex-1 pt-0.5">
                        <p class="text-sm font-medium text-gray-900">${message}</p>
                    </div>
                    <div class="ml-4 flex-shrink-0 flex">
                        <button class="bg-white rounded-md inline-flex text-gray-400 hover:text-gray-500" onclick="this.parentElement.parentElement.parentElement.parentElement.remove()">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                </div>
            </div>
            <div class="h-1 ${colors[type]} notification-progress"></div>
        `;

        this.container.appendChild(notification);

        // Animation d'entrée
        setTimeout(() => {
            notification.classList.add('translate-x-0');
        }, 100);

        // Barre de progression
        const progressBar = notification.querySelector('.notification-progress');
        if (progressBar && duration > 0) {
            progressBar.style.transition = `width ${duration}ms linear`;
            progressBar.style.width = '0%';
        }

        // Auto-suppression
        if (duration > 0) {
            setTimeout(() => {
                notification.style.transform = 'translateX(100%)';
                setTimeout(() => {
                    if (notification.parentNode) {
                        notification.parentNode.removeChild(notification);
                    }
                }, 300);
            }, duration);
        }
    }
};

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    notifications.init();
});