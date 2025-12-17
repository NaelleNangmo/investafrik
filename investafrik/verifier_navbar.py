#!/usr/bin/env python
"""
Script pour vérifier que la navbar contient tous les éléments nécessaires pour la déconnexion.
"""
import os
import re

def verifier_navbar():
    """Vérifier le contenu de la navbar."""
    print("🔍 VÉRIFICATION DE LA NAVBAR")
    print("=" * 50)
    
    navbar_path = "templates/components/navbar.html"
    
    if not os.path.exists(navbar_path):
        print(f"❌ Fichier navbar non trouvé: {navbar_path}")
        return False
    
    with open(navbar_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifications
    checks = [
        # IDs nécessaires
        ('id="auth-container"', "ID auth-container"),
        ('id="user-menu"', "ID user-menu"),
        ('id="user-dropdown"', "ID user-dropdown"),
        ('id="guest-buttons"', "ID guest-buttons"),
        ('id="mobile-auth-section"', "ID mobile-auth-section"),
        ('id="mobile-guest-section"', "ID mobile-guest-section"),
        
        # Classes CSS nécessaires
        ('auth-nav-link', "Classe auth-nav-link"),
        ('mobile-auth-link', "Classe mobile-auth-link"),
        
        # Fonctions JavaScript
        ('function logout()', "Fonction logout()"),
        ('function resetUIToGuestState()', "Fonction resetUIToGuestState()"),
        ('function showLogoutMessage()', "Fonction showLogoutMessage()"),
        ('function toggleUserMenu()', "Fonction toggleUserMenu()"),
        
        # Éléments critiques
        ('onclick="logout()"', "Bouton de déconnexion"),
        ('console.log', "Messages de debug"),
        ('document.getElementById(\'auth-container\')', "Sélection auth-container"),
        ('document.querySelectorAll(\'.auth-nav-link\')', "Sélection auth-nav-link"),
        ('document.querySelectorAll(\'.mobile-auth-link\')', "Sélection mobile-auth-link"),
    ]
    
    all_good = True
    
    for pattern, description in checks:
        if pattern in content:
            print(f"✅ {description}")
        else:
            print(f"❌ {description} - MANQUANT!")
            all_good = False
    
    # Vérifications spéciales
    print("\n🔍 Vérifications spéciales:")
    
    # Vérifier que resetUIToGuestState contient la logique correcte
    if 'authContainer.innerHTML' in content:
        print("✅ Logique de remplacement du conteneur d'auth")
    else:
        print("❌ Logique de remplacement du conteneur d'auth - MANQUANTE!")
        all_good = False
    
    # Vérifier les messages de debug
    debug_messages = [
        '🔄 DÉBUT - Réinitialisation',
        '📝 Remplacement du conteneur',
        '✅ Boutons Connexion/Inscription affichés',
        '🔒 Lien desktop masqué',
        '✅ FIN - Interface utilisateur',
        '🎉 SUCCÈS - Boutons guest visibles'
    ]
    
    for msg in debug_messages:
        if msg in content:
            print(f"✅ Message debug: {msg}")
        else:
            print(f"❌ Message debug manquant: {msg}")
            all_good = False
    
    print("\n" + "=" * 50)
    if all_good:
        print("🎉 NAVBAR COMPLÈTE - Tous les éléments sont présents!")
        print("✅ La déconnexion devrait fonctionner correctement")
    else:
        print("❌ NAVBAR INCOMPLÈTE - Des éléments manquent!")
        print("⚠️  La déconnexion risque de ne pas fonctionner")
    
    return all_good

def afficher_structure_navbar():
    """Afficher la structure de la navbar."""
    print("\n🏗️  STRUCTURE ATTENDUE DE LA NAVBAR:")
    print("=" * 50)
    
    structure = """
    <nav>
        <div id="auth-container">
            {% if user.is_authenticated %}
                <div id="user-menu">
                    <button onclick="toggleUserMenu()">...</button>
                    <div id="user-dropdown">
                        <button onclick="logout()">Déconnexion</button>
                    </div>
                </div>
            {% else %}
                <div id="guest-buttons">
                    <a href="/auth/login/">Connexion</a>
                    <a href="/auth/register/">Inscription</a>
                </div>
            {% endif %}
        </div>
        
        <div id="mobile-menu">
            {% if user.is_authenticated %}
                <a class="mobile-auth-link">Mes Projets</a>
                <a class="mobile-auth-link">Messages</a>
                <div id="mobile-auth-section">
                    <button onclick="logout()">Déconnexion</button>
                </div>
            {% else %}
                <div id="mobile-guest-section">
                    <a href="/auth/login/">Connexion</a>
                    <a href="/auth/register/">Inscription</a>
                </div>
            {% endif %}
        </div>
    </nav>
    
    <script>
        function logout() {
            resetUIToGuestState();
            // ... logique de déconnexion
        }
        
        function resetUIToGuestState() {
            // 1. Remplacer auth-container
            // 2. Masquer .auth-nav-link
            // 3. Masquer .mobile-auth-link
            // 4. Remplacer mobile-auth-section
        }
    </script>
    """
    
    print(structure)

def main():
    """Fonction principale."""
    print("🔧 VÉRIFICATEUR DE NAVBAR INVESTAFRIK")
    print("=" * 60)
    
    # Vérifier la navbar
    navbar_ok = verifier_navbar()
    
    # Afficher la structure attendue
    afficher_structure_navbar()
    
    print("\n" + "=" * 60)
    print("📋 PROCHAINES ÉTAPES:")
    print("=" * 60)
    
    if navbar_ok:
        print("1. ✅ La navbar semble complète")
        print("2. 🧪 Lancez: python test_deconnexion_direct.py")
        print("3. 🌐 Testez la déconnexion sur http://127.0.0.1:8000/")
    else:
        print("1. ❌ Corrigez les éléments manquants dans la navbar")
        print("2. 🔄 Relancez cette vérification")
        print("3. 🧪 Puis testez avec: python test_deconnexion_direct.py")
    
    return navbar_ok

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)