/**
 * JavaScript principal pour InvestAfrik
 */

// Fonctions utilitaires globales
window.InvestAfrik = {
    // Initialisation de l'application
    init() {
        this.setupCSRF();
        this.setupAuth();
        this.setupNavigation();
    },

    // Configuration CSRF pour Django
    setupCSRF() {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
        if (csrfToken) {
            // Ajouter le token CSRF aux requêtes API
            api.defaultHeaders['X-CSRFToken'] = csrfToken;
        }
    },

    // Gestion de l'authentification
    setupAuth() {
        // Vérifier si l'utilisateur est connecté
        if (api.isAuthenticated()) {
            this.updateUIForAuthenticatedUser();
        }
    },

    // Mise à jour de l'interface pour utilisateur connecté
    updateUIForAuthenticatedUser() {
        // Masquer les boutons de connexion/inscription
        const guestButtons = document.getElementById('guest-buttons');
        const mobileGuestButtons = document.getElementById('mobile-guest-buttons');
        
        if (guestButtons) guestButtons.style.display = 'none';
        if (mobileGuestButtons) mobileGuestButtons.style.display = 'none';
        
        // Afficher le menu utilisateur
        const userMenu = document.getElementById('user-menu');
        const mobileLogout = document.getElementById('mobile-logout');
        
        if (userMenu) userMenu.style.display = 'block';
        if (mobileLogout) mobileLogout.style.display = 'block';
    },

    // Configuration de la navigation
    setupNavigation() {
        // Gestion du menu mobile
        window.toggleMobileMenu = () => {
            const menu = document.getElementById('mobile-menu');
            if (menu) {
                menu.classList.toggle('hidden');
            }
        };

        // Gestion du menu utilisateur
        window.toggleUserMenu = () => {
            const dropdown = document.getElementById('user-dropdown');
            if (dropdown) {
                dropdown.classList.toggle('hidden');
            }
        };

        // Fermer les menus en cliquant à l'extérieur
        document.addEventListener('click', (event) => {
            const userMenu = document.querySelector('[onclick="toggleUserMenu()"]');
            const dropdown = document.getElementById('user-dropdown');
            
            if (userMenu && dropdown && 
                !userMenu.contains(event.target) && 
                !dropdown.contains(event.target)) {
                dropdown.classList.add('hidden');
            }
        });

        // Fonction de déconnexion globale
        window.logout = () => {
            api.logout();
        };
    }
};

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    InvestAfrik.init();
});

// Gestion des erreurs globales
window.addEventListener('error', function(event) {
    console.error('Erreur JavaScript:', event.error);
});

// Gestion des erreurs de promesses non capturées
window.addEventListener('unhandledrejection', function(event) {
    console.error('Promesse rejetée:', event.reason);
});