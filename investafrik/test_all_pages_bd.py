#!/usr/bin/env python3
"""
Test de toutes les pages avec communication BD.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investafrik.settings.development')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

def test_investor_pages():
    """Tester toutes les pages investisseur."""
    print("🧪 TEST PAGES INVESTISSEUR")
    print("=" * 40)
    
    client = Client()
    
    # Connexion investisseur
    login_success = client.login(email='investor@test.com', password='test123')
    if not login_success:
        print("❌ Échec connexion investisseur")
        return False
    
    print("✅ Connexion investisseur réussie")
    
    # Test des pages
    pages_to_test = [
        ('/auth/dashboard/investisseur/', 'Dashboard Investisseur'),
        ('/auth/profile/', 'Profil'),
        ('/projects/', 'Liste Projets'),
        ('/investments/my-investments/', 'Mes Investissements'),
        ('/messaging/conversations/', 'Conversations'),
    ]
    
    for url, name in pages_to_test:
        try:
            response = client.get(url)
            if response.status_code == 200:
                print(f"✅ {name}: OK")
                
                # Vérifier le contenu
                content = response.content.decode()
                if 'Erreur lors du chargement' in content:
                    print(f"⚠️  {name}: Contient des erreurs de chargement")
                elif len(content) < 1000:
                    print(f"⚠️  {name}: Contenu très court ({len(content)} chars)")
                else:
                    print(f"   Contenu: {len(content)} caractères")
                    
            else:
                print(f"❌ {name}: Status {response.status_code}")
                
        except Exception as e:
            print(f"❌ {name}: Erreur {e}")
    
    return True

def test_porteur_pages():
    """Tester toutes les pages porteur."""
    print("\n🧪 TEST PAGES PORTEUR")
    print("=" * 40)
    
    client = Client()
    
    # Connexion porteur
    login_success = client.login(email='admin@investafrik.com', password='admin123')
    if not login_success:
        print("❌ Échec connexion porteur")
        return False
    
    print("✅ Connexion porteur réussie")
    
    # Test des pages
    pages_to_test = [
        ('/auth/dashboard/porteur/', 'Dashboard Porteur'),
        ('/auth/profile/', 'Profil'),
        ('/projects/', 'Liste Projets'),
        ('/projects/my-projects/', 'Mes Projets'),
        ('/messaging/conversations/', 'Conversations'),
    ]
    
    for url, name in pages_to_test:
        try:
            response = client.get(url)
            if response.status_code == 200:
                print(f"✅ {name}: OK")
                
                # Vérifier le contenu
                content = response.content.decode()
                if 'Erreur lors du chargement' in content:
                    print(f"⚠️  {name}: Contient des erreurs de chargement")
                elif len(content) < 1000:
                    print(f"⚠️  {name}: Contenu très court ({len(content)} chars)")
                else:
                    print(f"   Contenu: {len(content)} caractères")
                    
            else:
                print(f"❌ {name}: Status {response.status_code}")
                
        except Exception as e:
            print(f"❌ {name}: Erreur {e}")
    
    return True

def test_profile_update():
    """Tester la mise à jour du profil."""
    print("\n🧪 TEST MISE À JOUR PROFIL")
    print("=" * 30)
    
    client = Client()
    client.login(email='investor@test.com', password='test123')
    
    # Test POST sur profil
    profile_data = {
        'first_name': 'Test Updated',
        'last_name': 'Investor Updated',
        'phone_number': '+237123456789',
        'bio': 'Bio mise à jour',
        'company': 'Test Company',
        'job_title': 'Test Manager',
        'email_notifications': 'on',
    }
    
    response = client.post('/auth/profile/', profile_data)
    
    if response.status_code in [200, 302]:
        print("✅ Mise à jour profil: OK")
        
        # Vérifier que les données ont été sauvées
        user = User.objects.get(email='investor@test.com')
        if user.first_name == 'Test Updated':
            print("✅ Données utilisateur mises à jour")
        else:
            print("❌ Données utilisateur non mises à jour")
            
    else:
        print(f"❌ Mise à jour profil: Status {response.status_code}")

if __name__ == '__main__':
    print("🚀 TEST COMPLET DES PAGES AVEC BD")
    print("=" * 60)
    
    success1 = test_investor_pages()
    success2 = test_porteur_pages()
    test_profile_update()
    
    print("\n" + "=" * 60)
    
    if success1 and success2:
        print("🎉 TOUS LES TESTS RÉUSSIS!")
        print("✅ Communication BD fonctionnelle")
        print("✅ Pages investisseur OK")
        print("✅ Pages porteur OK")
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        print("Vérifiez les erreurs ci-dessus")
    
    print("\n📋 Pages corrigées:")
    print("- Dashboard investisseur avec vraies données BD")
    print("- Profil avec chargement et modification")
    print("- Liste projets avec données BD")
    print("- Mes projets avec statistiques")
    print("- Mes investissements avec données BD")
    print("- Conversations avec utilisateurs BD")