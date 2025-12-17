#!/usr/bin/env python3
"""
Script pour corriger les problèmes d'authentification.
"""
import os
import sys
import django
from django.contrib.auth import authenticate

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investafrik.settings.development')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

def fix_authentication():
    """Corriger les problèmes d'authentification."""
    print("🔧 Correction des problèmes d'authentification")
    print("=" * 50)
    
    # 1. Vérifier les utilisateurs existants
    print("📋 Utilisateurs existants:")
    users = User.objects.all()
    for user in users:
        print(f"  - {user.email} (Type: {user.user_type}, Active: {user.is_active})")
    
    # 2. Vérifier l'utilisateur admin
    try:
        admin_user = User.objects.get(email='admin@investafrik.com')
        print(f"\n✅ Utilisateur admin trouvé: {admin_user.email}")
        print(f"   - Username: {admin_user.username}")
        print(f"   - Is active: {admin_user.is_active}")
        print(f"   - Is staff: {admin_user.is_staff}")
        print(f"   - Is superuser: {admin_user.is_superuser}")
        print(f"   - User type: {admin_user.user_type}")
        
        # 3. Réinitialiser le mot de passe admin
        print("\n🔑 Réinitialisation du mot de passe admin...")
        admin_user.set_password('admin123')
        admin_user.is_active = True
        admin_user.save()
        print("✅ Mot de passe admin réinitialisé")
        
        # 4. Test d'authentification
        print("\n🧪 Test d'authentification...")
        auth_user = authenticate(email='admin@investafrik.com', password='admin123')
        if auth_user:
            print("✅ Authentification réussie!")
        else:
            print("❌ Échec de l'authentification")
            
            # Essayer avec username
            auth_user = authenticate(username='admin@investafrik.com', password='admin123')
            if auth_user:
                print("✅ Authentification réussie avec username!")
            else:
                print("❌ Échec avec username aussi")
        
    except User.DoesNotExist:
        print("❌ Utilisateur admin non trouvé, création...")
        
        # Créer l'utilisateur admin
        admin_user = User.objects.create_superuser(
            email='admin@investafrik.com',
            password='admin123',
            first_name='Admin',
            last_name='User',
            user_type='porteur',
            country='CM'
        )
        print(f"✅ Utilisateur admin créé: {admin_user.email}")
    
    # 5. Créer un utilisateur de test investisseur
    try:
        investor = User.objects.get(email='investor@test.com')
        print(f"\n✅ Utilisateur investisseur trouvé: {investor.email}")
    except User.DoesNotExist:
        print("\n👤 Création d'un utilisateur investisseur de test...")
        investor = User.objects.create_user(
            email='investor@test.com',
            password='test123',
            first_name='Test',
            last_name='Investor',
            user_type='investisseur',
            country='CM'
        )
        print(f"✅ Utilisateur investisseur créé: {investor.email}")
    
    # 6. Vérifier la configuration d'authentification
    print("\n⚙️ Vérification de la configuration d'authentification...")
    from django.conf import settings
    
    print(f"AUTH_USER_MODEL: {getattr(settings, 'AUTH_USER_MODEL', 'Non défini')}")
    
    # Vérifier les backends d'authentification
    auth_backends = getattr(settings, 'AUTHENTICATION_BACKENDS', [])
    print("AUTHENTICATION_BACKENDS:")
    for backend in auth_backends:
        print(f"  - {backend}")
    
    print("\n" + "=" * 50)
    print("✅ Correction de l'authentification terminée!")
    
    return True

def test_login_api():
    """Tester l'API de login."""
    print("\n🌐 Test de l'API de login")
    print("=" * 30)
    
    from django.test import Client
    import json
    
    client = Client()
    
    # Test avec les bonnes credentials
    login_data = {
        'email': 'admin@investafrik.com',
        'password': 'admin123'
    }
    
    response = client.post(
        '/api/auth/login/',
        data=json.dumps(login_data),
        content_type='application/json'
    )
    
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.content.decode()}")
    
    if response.status_code == 200:
        print("✅ API de login fonctionne!")
        return True
    else:
        print("❌ Problème avec l'API de login")
        return False

if __name__ == '__main__':
    print("🚀 Démarrage de la correction d'authentification")
    print("=" * 60)
    
    success1 = fix_authentication()
    success2 = test_login_api()
    
    if success1 and success2:
        print("\n🎉 AUTHENTIFICATION CORRIGÉE!")
        print("\n📋 Comptes de test disponibles:")
        print("   Admin: admin@investafrik.com / admin123")
        print("   Investisseur: investor@test.com / test123")
    else:
        print("\n❌ PROBLÈMES DÉTECTÉS")
        print("Vérifiez les erreurs ci-dessus.")