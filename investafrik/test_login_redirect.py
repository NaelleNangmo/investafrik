#!/usr/bin/env python3
"""
Test de la redirection après connexion selon le type d'utilisateur.
"""
import os
import django
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investafrik.settings.development')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def test_login_redirects():
    """Test des redirections après connexion selon le type d'utilisateur."""
    print("🧪 TEST DES REDIRECTIONS APRÈS CONNEXION")
    print("=" * 50)
    
    client = Client()
    
    # Test 1: Connexion admin (porteur)
    print("1. Test connexion admin (porteur)...")
    response = client.post('/auth/login/', {
        'email': 'admin@investafrik.com',
        'password': 'admin123'
    }, follow=True)
    
    print(f"Status: {response.status_code}")
    print(f"URL finale: {response.wsgi_request.path}")
    
    if '/auth/dashboard/porteur/' in response.wsgi_request.path:
        print("✅ Redirection correcte vers dashboard porteur")
    else:
        print("❌ Redirection incorrecte")
    
    # Déconnexion
    client.logout()
    
    # Test 2: Connexion investisseur
    print("\n2. Test connexion investisseur...")
    try:
        investor = User.objects.get(email='investor@test.com')
        response = client.post('/auth/login/', {
            'email': 'investor@test.com',
            'password': 'test123'
        }, follow=True)
        
        print(f"Status: {response.status_code}")
        print(f"URL finale: {response.wsgi_request.path}")
        
        if '/auth/dashboard/investisseur/' in response.wsgi_request.path:
            print("✅ Redirection correcte vers dashboard investisseur")
        else:
            print("❌ Redirection incorrecte")
            
    except User.DoesNotExist:
        print("⚠️ Utilisateur investisseur non trouvé")
    
    # Test 3: Vérification de la navbar après connexion
    print("\n3. Test de la navbar après connexion...")
    client.login(email='admin@investafrik.com', password='admin123')
    response = client.get('/')
    content = response.content.decode()
    
    if 'Mes Projets' in content:
        print("✅ Onglet 'Mes Projets' visible pour porteur")
    else:
        print("❌ Onglet 'Mes Projets' manquant")
    
    if 'Messages' in content:
        print("✅ Onglet 'Messages' visible")
    else:
        print("❌ Onglet 'Messages' manquant")
    
    print("\n" + "=" * 50)
    print("✅ Tests terminés!")

def test_navbar_by_user_type():
    """Test de l'affichage de la navbar selon le type d'utilisateur."""
    print("\n🎨 TEST NAVBAR PAR TYPE D'UTILISATEUR")
    print("=" * 40)
    
    client = Client()
    
    # Test porteur
    print("1. Test navbar porteur...")
    client.login(email='admin@investafrik.com', password='admin123')
    response = client.get('/')
    content = response.content.decode()
    
    if 'Mes Projets' in content and 'Mes Investissements' not in content:
        print("✅ Navbar correcte pour porteur")
    else:
        print("❌ Navbar incorrecte pour porteur")
    
    client.logout()
    
    # Test investisseur
    print("\n2. Test navbar investisseur...")
    try:
        client.login(email='investor@test.com', password='test123')
        response = client.get('/')
        content = response.content.decode()
        
        if 'Mes Investissements' in content and 'Mes Projets' not in content:
            print("✅ Navbar correcte pour investisseur")
        else:
            print("❌ Navbar incorrecte pour investisseur")
            
    except Exception as e:
        print(f"⚠️ Erreur test investisseur: {e}")

if __name__ == '__main__':
    print("🚀 TESTS DE REDIRECTION ET NAVBAR")
    print("=" * 60)
    
    test_login_redirects()
    test_navbar_by_user_type()
    
    print("\n📋 Instructions pour test manuel:")
    print("1. Allez sur http://127.0.0.1:8000/auth/login/")
    print("2. Connectez-vous avec admin@investafrik.com / admin123")
    print("3. Vérifiez la redirection vers /auth/dashboard/porteur/")
    print("4. Vérifiez que la navbar affiche 'Mes Projets' et 'Messages'")
    print("5. Déconnectez-vous et testez avec investor@test.com / test123")