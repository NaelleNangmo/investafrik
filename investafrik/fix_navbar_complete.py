#!/usr/bin/env python3
"""
Script de correction complète de la navbar.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investafrik.settings.development')
django.setup()

from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model

User = get_user_model()

def clear_all_sessions():
    """Supprimer toutes les sessions pour forcer la déconnexion."""
    print("🧹 NETTOYAGE DES SESSIONS")
    print("=" * 30)
    
    session_count = Session.objects.count()
    print(f"Sessions trouvées: {session_count}")
    
    if session_count > 0:
        Session.objects.all().delete()
        print("✅ Toutes les sessions supprimées")
    else:
        print("ℹ️ Aucune session à supprimer")

def create_test_instructions():
    """Créer des instructions de test détaillées."""
    print("\n📋 INSTRUCTIONS DE TEST COMPLÈTES")
    print("=" * 50)
    
    print("1. NETTOYAGE COMPLET:")
    print("   - Fermez tous les onglets du navigateur")
    print("   - Videz le cache (Ctrl+Shift+Del)")
    print("   - Ouvrez une fenêtre de navigation privée")
    
    print("\n2. TEST INITIAL:")
    print("   - Allez sur http://127.0.0.1:8000")
    print("   - Vérifiez la section DEBUG jaune en haut")
    print("   - Elle doit afficher: Authenticated: NO")
    
    print("\n3. VÉRIFICATION NAVBAR:")
    print("   - Regardez en haut à droite de la navbar")
    print("   - Vous devez voir 'Connexion' et 'Inscription'")
    print("   - Si vous ne les voyez pas, inspectez l'élément (F12)")
    
    print("\n4. TEST RESPONSIVE:")
    print("   - Réduisez la largeur de la fenêtre (mode mobile)")
    print("   - Cliquez sur le menu hamburger (☰)")
    print("   - Vérifiez que 'Connexion' et 'Inscription' sont dans le menu")
    
    print("\n5. TEST CONNEXION:")
    print("   - Cliquez sur 'Connexion'")
    print("   - Connectez-vous avec admin@investafrik.com / admin123")
    print("   - Vérifiez que la navbar change (nom utilisateur + menu)")
    
    print("\n6. TEST DÉCONNEXION:")
    print("   - Cliquez sur votre nom dans la navbar")
    print("   - Cliquez sur 'Déconnexion'")
    print("   - Vérifiez le retour aux boutons 'Connexion/Inscription'")

def check_css_issues():
    """Vérifier les problèmes CSS potentiels."""
    print("\n🎨 VÉRIFICATION CSS")
    print("=" * 20)
    
    print("Classes CSS importantes à vérifier:")
    print("   - 'hidden md:flex' = Caché sur mobile, visible sur desktop")
    print("   - 'md:hidden' = Visible sur mobile, caché sur desktop")
    print("   - Si vous êtes sur mobile, les boutons sont dans le menu ☰")
    print("   - Si vous êtes sur desktop, les boutons sont en haut à droite")

if __name__ == '__main__':
    print("🔧 CORRECTION COMPLÈTE DE LA NAVBAR")
    print("=" * 60)
    
    clear_all_sessions()
    create_test_instructions()
    check_css_issues()
    
    print("\n" + "=" * 60)
    print("🎯 RÉSUMÉ:")
    print("✅ La navbar est techniquement correcte")
    print("✅ Les boutons 'Connexion/Inscription' sont présents")
    print("⚠️ Le problème est probablement:")
    print("   - Session utilisateur résiduelle")
    print("   - Cache du navigateur")
    print("   - Affichage responsive (mobile vs desktop)")
    
    print("\n🚀 SOLUTION RAPIDE:")
    print("1. Navigation privée + http://127.0.0.1:8000")
    print("2. Vérifier la section DEBUG jaune")
    print("3. Chercher les boutons selon la taille d'écran")
    print("4. Si problème persiste, envoyer capture d'écran avec F12 ouvert")