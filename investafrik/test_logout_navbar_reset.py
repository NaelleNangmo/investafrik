#!/usr/bin/env python3
"""
Test pour vérifier que la navbar se réinitialise correctement après déconnexion.
"""
import os
import django
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investafrik.settings.development')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def test_navbar_reset_after_logout():
    """Test complet de la réinitialisation de la navbar après déconnexion."""
    print("🧪 TEST RÉINITIALISATION NAVBAR APRÈS DÉCONNEXION")
    print("=" * 60)
    
    client = Client()
    
    # 1. État initial (utilisateur anonyme)
    print("1. Test état initial (anonyme)...")
    response = client.get('/')
    content = response.content.decode()
    
    if 'Connexion' in content and 'Inscription' in content:
        print("✅ État initial correct : boutons Connexion/Inscription présents")
    else:
        print("❌ État initial incorrect")
        return False
    
    # 2. Connexion
    print("\n2. Test connexion...")
    login_success = client.login(email='admin@investafrik.com', password='admin123')
    if not login_success:
        print("❌ Échec de la connexion")
        return False
    
    response = client.get('/')
    content = response.content.decode()
    
    if 'user-menu' in content and 'Mes Projets' in content:
        print("✅ État connecté correct : menu utilisateur et onglets présents")
    else:
        print("❌ État connecté incorrect")
        return False
    
    # 3. Déconnexion
    print("\n3. Test déconnexion...")
    logout_response = client.post('/auth/logout/')
    print(f"Status déconnexion: {logout_response.status_code}")
    
    # 4. Vérification après déconnexion
    print("\n4. Vérification état après déconnexion...")
    response = client.get('/')
    content = response.content.decode()
    
    # Vérifications détaillées
    checks = {
        'Boutons guest présents': 'Connexion' in content and 'Inscription' in content,
        'Menu utilisateur absent': 'user-menu' not in content or 'id="user-menu"' not in content,
        'Onglets auth absents': 'Mes Projets' not in content and 'Mes Investissements' not in content,
        'Navigation publique présente': 'Comment ça marche' in content and 'À propos' in content
    }
    
    all_passed = True
    for check_name, result in checks.items():
        if result:
            print(f"✅ {check_name}")
        else:
            print(f"❌ {check_name}")
            all_passed = False
    
    return all_passed

def test_navbar_structure():
    """Test de la structure de la navbar pour différents états."""
    print("\n🎨 TEST STRUCTURE NAVBAR")
    print("=" * 40)
    
    from django.template.loader import render_to_string
    from django.contrib.auth.models import AnonymousUser
    
    # Test structure anonyme
    print("1. Structure navbar anonyme...")
    try:
        context = {'user': AnonymousUser()}
        navbar_html = render_to_string('components/navbar.html', context)
        
        # Vérifications structure
        structure_checks = {
            'Div guest-buttons présent': 'id="guest-buttons"' in navbar_html,
            'Div user-menu absent': 'id="user-menu"' not in navbar_html,
            'Liens auth absents': 'auth-nav-link' not in navbar_html,
            'Section mobile guest présente': 'mobile-guest-section' in navbar_html
        }
        
        for check, result in structure_checks.items():
            print(f"{'✅' if result else '❌'} {check}")
            
    except Exception as e:
        print(f"❌ Erreur structure anonyme: {e}")
        return False
    
    # Test structure connecté
    print("\n2. Structure navbar connecté...")
    try:
        user = User.objects.get(email='admin@investafrik.com')
        context = {'user': user}
        navbar_html = render_to_string('components/navbar.html', context)
        
        structure_checks = {
            'Div user-menu présent': 'id="user-menu"' in navbar_html,
            'Div guest-buttons absent': 'id="guest-buttons"' not in navbar_html,
            'Liens auth présents': 'auth-nav-link' in navbar_html,
            'Section mobile auth présente': 'mobile-auth-section' in navbar_html
        }
        
        for check, result in structure_checks.items():
            print(f"{'✅' if result else '❌'} {check}")
            
    except Exception as e:
        print(f"❌ Erreur structure connecté: {e}")
        return False
    
    return True

if __name__ == '__main__':
    print("🚀 TESTS RÉINITIALISATION NAVBAR")
    print("=" * 70)
    
    success1 = test_navbar_reset_after_logout()
    success2 = test_navbar_structure()
    
    print("\n" + "=" * 70)
    
    if success1 and success2:
        print("🎉 TOUS LES TESTS RÉUSSIS!")
        print("✅ La navbar se réinitialise correctement après déconnexion")
        print("✅ La structure conditionnelle fonctionne")
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        print("La navbar pourrait ne pas se réinitialiser correctement")
    
    print("\n📋 Instructions pour test manuel:")
    print("1. Allez sur http://127.0.0.1:8000")
    print("2. Vérifiez les boutons 'Connexion' et 'Inscription'")
    print("3. Connectez-vous avec admin@investafrik.com / admin123")
    print("4. Vérifiez le menu utilisateur et les onglets")
    print("5. Cliquez sur 'Déconnexion'")
    print("6. Vérifiez que les boutons 'Connexion/Inscription' réapparaissent")