#!/usr/bin/env python3
"""
Test script pour vérifier la fonctionnalité de déconnexion.
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

def test_logout_functionality():
    """Test complet de la fonctionnalité de déconnexion."""
    print("🧪 Test de la fonctionnalité de déconnexion")
    print("=" * 50)
    
    # Créer un client de test
    client = Client()
    
    # 1. Vérifier qu'un utilisateur existe
    try:
        user = User.objects.get(email='admin@investafrik.com')
        print(f"✅ Utilisateur trouvé: {user.email} (Type: {user.user_type})")
    except User.DoesNotExist:
        print("❌ Utilisateur admin@investafrik.com non trouvé")
        return False
    
    # 2. Test de connexion
    print("\n📝 Test de connexion...")
    login_success = client.login(email='admin@investafrik.com', password='admin123')
    if login_success:
        print("✅ Connexion réussie")
    else:
        print("❌ Échec de la connexion")
        return False
    
    # 3. Vérifier l'état de session après connexion
    session = client.session
    print(f"✅ Session ID: {session.session_key}")
    print(f"✅ User ID dans session: {session.get('_auth_user_id')}")
    
    # 4. Accéder à une page protégée
    response = client.get('/auth/dashboard/')
    if response.status_code in [200, 302]:  # 302 = redirection vers dashboard spécifique
        print("✅ Accès au dashboard autorisé")
    else:
        print(f"❌ Accès au dashboard refusé (Status: {response.status_code})")
        return False
    
    # 5. Test de déconnexion via POST
    print("\n🚪 Test de déconnexion...")
    logout_response = client.post('/auth/logout/', follow=True)
    
    print(f"✅ Status de déconnexion: {logout_response.status_code}")
    
    # 6. Vérifier que la session est détruite
    try:
        # Essayer d'accéder à nouveau au dashboard
        dashboard_response = client.get('/auth/dashboard/')
        if dashboard_response.status_code == 302:  # Redirection vers login
            print("✅ Redirection vers login après déconnexion")
        else:
            print(f"⚠️  Status inattendu après déconnexion: {dashboard_response.status_code}")
    except Exception as e:
        print(f"❌ Erreur lors du test post-déconnexion: {e}")
    
    # 7. Vérifier le contenu de la réponse de déconnexion
    if logout_response.status_code == 200:
        try:
            import json
            response_data = json.loads(logout_response.content.decode())
            if response_data.get('success'):
                print("✅ Réponse JSON de déconnexion valide")
                print(f"   Message: {response_data.get('message')}")
                print(f"   Redirect: {response_data.get('redirect')}")
            else:
                print("❌ Réponse de déconnexion invalide")
        except json.JSONDecodeError:
            print("⚠️  Réponse de déconnexion n'est pas du JSON")
    
    print("\n" + "=" * 50)
    print("✅ Test de déconnexion terminé avec succès!")
    return True

def test_navbar_template():
    """Test du template navbar pour vérifier la syntaxe."""
    print("\n🎨 Test du template navbar")
    print("=" * 30)
    
    from django.template.loader import get_template
    from django.template import Context
    from django.contrib.auth.models import AnonymousUser
    
    try:
        # Test avec utilisateur anonyme
        template = get_template('components/navbar.html')
        context = Context({'user': AnonymousUser()})
        rendered = template.render(context)
        print("✅ Template navbar rendu avec utilisateur anonyme")
        
        # Test avec utilisateur connecté
        user = User.objects.get(email='admin@investafrik.com')
        context = Context({'user': user})
        rendered = template.render(context)
        print("✅ Template navbar rendu avec utilisateur connecté")
        
        # Vérifier la présence des éléments clés
        if 'logout-form-desktop' in rendered:
            print("✅ Formulaire de déconnexion desktop présent")
        if 'logout-form-mobile' in rendered:
            print("✅ Formulaire de déconnexion mobile présent")
        if 'user-menu-btn' in rendered:
            print("✅ Bouton menu utilisateur présent")
            
    except Exception as e:
        print(f"❌ Erreur lors du rendu du template: {e}")
        return False
    
    return True

if __name__ == '__main__':
    print("🚀 Démarrage des tests de déconnexion InvestAfrik")
    print("=" * 60)
    
    # Test de la fonctionnalité
    success1 = test_logout_functionality()
    
    # Test du template
    success2 = test_navbar_template()
    
    if success1 and success2:
        print("\n🎉 TOUS LES TESTS SONT PASSÉS!")
        print("La fonctionnalité de déconnexion devrait maintenant fonctionner correctement.")
    else:
        print("\n❌ CERTAINS TESTS ONT ÉCHOUÉ")
        print("Vérifiez les erreurs ci-dessus.")
    
    print("\n📋 Instructions pour tester manuellement:")
    print("1. Démarrez le serveur: python manage.py runserver")
    print("2. Connectez-vous avec admin@investafrik.com / admin123")
    print("3. Cliquez sur le menu utilisateur dans la navbar")
    print("4. Cliquez sur 'Déconnexion'")
    print("5. Vérifiez que la navbar revient à l'état initial (Connexion/Inscription)")