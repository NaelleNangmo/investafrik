/**
 * Main JavaScript file for InvestAfrik
 */

// Alpine.js global configuration
document.addEventListener('alpine:init', () => {
    // Global Alpine.js stores and utilities can be defined here
});

// Notification system
class NotificationManager {
    constructor() {
        this.container = document.getElementById('notifications');
    }
    
    show(message, type = 'info', duration = 5000) {
        const notification = this.createNotification(message, type);
        this.container.appendChild(notification);
        
        // Auto remove after duration
        setTimeout(() => {
            this.remove(notification);
        }, duration);
        
        return notification;
    }
    
    createNotification(message, type) {
        const div = document.createElement('div');
        div.className = `notification animate-slide-up p-4 rounded-lg shadow-lg text-white max-w-sm ${this.getTypeClasses(type)}`;
        
        div.innerHTML = `
            <div class="flex items-center justify-between">
                <span>${message}</span>
                <button onclick="notifications.remove(this.parentElement.parentElement)" class="ml-2 text-white hover:text-gray-200">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                </button>
            </div>
        `;
        
        return div;
    }
    
    getTypeClasses(type) {
        const classes = {
            'success': 'bg-green-500',
            'error': 'bg-red-500',
            'warning': 'bg-yellow-500',
            'info': 'bg-blue-500'
        };
        return classes[type] || classes.info;
    }
    
    remove(notification) {
        if (notification && notification.parentElement) {
            notification.classList.add('animate-fade-out');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }
    }
}

// Initialize notification manager
const notifications = new NotificationManager();

// API Helper
class APIClient {
    constructor() {
        this.baseURL = '/api';
        this.token = localStorage.getItem('access_token');
    }
    
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };
        
        // Add auth token if available
        if (this.token) {
            config.headers['Authorization'] = `Bearer ${this.token}`;
        }
        
        try {
            const response = await fetch(url, config);
            
            if (response.status === 401) {
                // Token expired, try to refresh
                await this.refreshToken();
                // Retry original request
                config.headers['Authorization'] = `Bearer ${this.token}`;
                return await fetch(url, config);
            }
            
            return response;
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }
    
    async refreshToken() {
        const refreshToken = localStorage.getItem('refresh_token');
        if (!refreshToken) {
            this.logout();
            return;
        }
        
        try {
            const response = await fetch('/api/auth/refresh-token/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ refresh: refreshToken })
            });
            
            if (response.ok) {
                const data = await response.json();
                this.token = data.access;
                localStorage.setItem('access_token', data.access);
            } else {
                this.logout();
            }
        } catch (error) {
            this.logout();
        }
    }
    
    logout() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/auth/login/';
    }
}

// Initialize API client
const api = new APIClient();

// Utility functions
const utils = {
    formatCurrency(amount) {
        return new Intl.NumberFormat('fr-FR', {
            style: 'currency',
            currency: 'XAF',
            minimumFractionDigits: 0
        }).format(amount).replace('XAF', 'FCFA');
    },
    
    formatDate(dateString) {
        return new Intl.DateTimeFormat('fr-FR', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        }).format(new Date(dateString));
    },
    
    timeAgo(dateString) {
        const now = new Date();
        const date = new Date(dateString);
        const diffInSeconds = Math.floor((now - date) / 1000);
        
        if (diffInSeconds < 60) return 'À l\'instant';
        if (diffInSeconds < 3600) return `Il y a ${Math.floor(diffInSeconds / 60)} min`;
        if (diffInSeconds < 86400) return `Il y a ${Math.floor(diffInSeconds / 3600)} h`;
        return `Il y a ${Math.floor(diffInSeconds / 86400)} j`;
    }
};

// Make utilities globally available
window.notifications = notifications;
window.api = api;
window.utils = utils;