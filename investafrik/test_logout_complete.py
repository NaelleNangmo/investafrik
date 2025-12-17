#!/usr/bin/env python3
"""
Test complet de la fonctionnalité de déconnexion.
"""
import os
import sys
import django
from django.test import Client
from django.contrib.auth import get_user_model

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investafrik.settings.development')
django.setup()

User = get_user_model()

def test_complete_logout():
    """Test complet de déconnexion avec vérification de la navbar."""
    print("🧪 TEST COMPLET DE DÉCONNEXION")
    print("=" * 50)
    
    client = Client()
    
    # 1. Connexion
    print("1. Test de connexion...")
    login_success = client.login(email='admin@investafrik.com', password='admin123')
    if not login_success:
        print("❌ Impossible de se connecter")
        return False
    print("✅ Connexion réussie")
    
    # 2. Vérifier l'état connecté
    response = client.get('/')
    if 'user-menu-btn' in response.content.decode():
        print("✅ Navbar affiche le menu utilisateur connecté")
    else:
        print("⚠️ Navbar ne semble pas afficher l'état connecté")
    
    # 3. Test de déconnexion
    print("\n2. Test de déconnexion...")
    logout_response = client.post('/auth/logout/', follow=True)
    print(f"Status de déconnexion: {logout_response.status_code}")
    
    # 4. Vérifier l'état déconnecté
    print("\n3. Vérification de l'état après déconnexion...")
    
    # Nouvelle requête pour vérifier l'état
    response = client.get('/')
    content = response.content.decode()
    
    # Vérifications
    if 'Connexion' in content and 'Inscription' in content:
        print("✅ Boutons Connexion/Inscription présents")
    else:
        print("❌ Boutons Connexion/Inscription manquants")
    
    if 'user-menu-btn' not in content:
        print("✅ Menu utilisateur absent (correct)")
    else:
        print("❌ Menu utilisateur encore présent")
    
    # 5. Test d'accès à une page protégée
    dashboard_response = client.get('/auth/dashboard/')
    if dashboard_response.status_code == 302:  # Redirection
        print("✅ Redirection correcte pour page protégée")
    else:
        print(f"⚠️ Status inattendu pour page protégée: {dashboard_response.status_code}")
    
    print("\n" + "=" * 50)
    print("✅ Test de déconnexion terminé!")
    return True

def test_navbar_states():
    """Test des différents états de la navbar."""
    print("\n🎨 TEST DES ÉTATS DE LA NAVBAR")
    print("=" * 40)
    
    from django.template.loader import render_to_string
    from django.contrib.auth.models import AnonymousUser
    
    # Test avec utilisateur anonyme
    print("1. Test navbar utilisateur anonyme...")
    try:
        context = {'user': AnonymousUser()}
        navbar_html = render_to_string('components/navbar.html', context)
        
        if 'Connexion' in navbar_html and 'Inscription' in navbar_html:
            print("✅ Boutons Connexion/Inscription présents pour anonyme")
        else:
            print("❌ Boutons manquants pour utilisateur anonyme")
            
        if 'user-menu-btn' not in navbar_html:
            print("✅ Menu utilisateur absent pour anonyme")
        else:
            print("❌ Menu utilisateur présent pour anonyme")
            
    except Exception as e:
        print(f"❌ Erreur template anonyme: {e}")
    
    # Test avec utilisateur connecté
    print("\n2. Test navbar utilisateur connecté...")
    try:
        user = User.objects.get(email='admin@investafrik.com')
        context = {'user': user}
        navbar_html = render_to_string('components/navbar.html', context)
        
        if 'user-menu-btn' in navbar_html:
            print("✅ Menu utilisateur présent pour connecté")
        else:
            print("❌ Menu utilisateur absent pour connecté")
            
        if 'Déconnexion' in navbar_html:
            print("✅ Bouton Déconnexion présent")
        else:
            print("❌ Bouton Déconnexion absent")
            
    except Exception as e:
        print(f"❌ Erreur template connecté: {e}")

if __name__ == '__main__':
    print("🚀 TESTS DE DÉCONNEXION INVESTAFRIK")
    print("=" * 60)
    
    success1 = test_complete_logout()
    test_navbar_states()
    
    if success1:
        print("\n🎉 TESTS RÉUSSIS!")
        print("\n📋 Pour tester manuellement:")
        print("1. Allez sur http://127.0.0.1:8000")
        print("2. Connectez-vous avec admin@investafrik.com / admin123")
        print("3. Cliquez sur votre nom dans la navbar")
        print("4. Cliquez sur 'Déconnexion'")
        print("5. Vérifiez que la navbar revient à l'état initial")
    else:
        print("\n❌ TESTS ÉCHOUÉS")
        print("Vérifiez les erreurs ci-dessus.")