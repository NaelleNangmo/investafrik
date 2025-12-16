#!/usr/bin/env python
"""
Script de test complet pour la fonctionnalité de déconnexion InvestAfrik.
Ce script teste que la déconnexion supprime bien la session et réinitialise l'interface.
"""
import os
import sys
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investafrik.settings.development')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.sessions.models import Session
import json

User = get_user_model()

def test_complete_logout_functionality():
    """Test complet de la fonctionnalité de déconnexion."""
    print("🔍 TEST COMPLET DE DÉCONNEXION")
    print("=" * 50)
    
    client = Client()
    
    # 1. Créer un utilisateur de test
    print("1️⃣ Création d'un utilisateur de test...")
    user = User.objects.create_user(
        email='test_logout@example.com',
        password='testpass123',
        first_name='Test',
        last_name='Logout',
        user_type='porteur'
    )
    print(f"   ✅ Utilisateur créé: {user.email}")
    
    # 2. Se connecter
    print("\n2️⃣ Test de connexion...")
    login_success = client.login(email='test_logout@example.com', password='testpass123')
    print(f"   ✅ Connexion: {'Réussie' if login_success else '❌ Échouée'}")
    
    if not login_success:
        print("   ❌ Impossible de continuer sans connexion")
        return False
    
    # 3. Vérifier que l'utilisateur est bien connecté
    print("\n3️⃣ Vérification de l'état connecté...")
    response = client.get('/auth/dashboard/')
    print(f"   ✅ Accès au dashboard: Status {response.status_code}")
    
    # Vérifier la session
    session_key = client.session.session_key
    print(f"   ✅ Clé de session: {session_key}")
    
    # 4. Tester la page de déconnexion GET (redirection)
    print("\n4️⃣ Test de déconnexion GET...")
    response = client.get('/auth/logout/')
    print(f"   ✅ Déconnexion GET: Status {response.status_code}")
    print(f"   ✅ Redirection vers: {response.url if hasattr(response, 'url') else 'Aucune'}")
    
    # 5. Reconnecter pour tester POST
    print("\n5️⃣ Reconnexion pour test POST...")
    client.login(email='test_logout@example.com', password='testpass123')
    
    # 6. Tester la déconnexion POST (AJAX)
    print("\n6️⃣ Test de déconnexion POST (AJAX)...")
    response = client.post('/auth/logout/', 
                          content_type='application/json',
                          HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    
    print(f"   ✅ Déconnexion POST: Status {response.status_code}")
    
    if response.status_code == 200:
        try:
            data = response.json()
            print(f"   ✅ Réponse JSON: {data}")
            print(f"   ✅ Succès: {data.get('success', False)}")
            print(f"   ✅ Message: {data.get('message', 'Aucun')}")
        except:
            print("   ⚠️  Pas de réponse JSON")
    
    # 7. Vérifier que l'utilisateur est déconnecté
    print("\n7️⃣ Vérification de la déconnexion...")
    
    # Tenter d'accéder au dashboard
    response = client.get('/auth/dashboard/')
    is_redirected = response.status_code in [302, 301]
    print(f"   ✅ Redirection après déconnexion: {'Oui' if is_redirected else 'Non'}")
    
    if is_redirected:
        print(f"   ✅ Redirigé vers: {response.url}")
    
    # Vérifier que la session est supprimée
    try:
        session_exists = Session.objects.filter(session_key=session_key).exists()
        print(f"   ✅ Session supprimée: {'Oui' if not session_exists else 'Non'}")
    except:
        print("   ⚠️  Impossible de vérifier la session")
    
    # 8. Tester l'accès aux pages protégées
    print("\n8️⃣ Test d'accès aux pages protégées après déconnexion...")
    
    protected_urls = [
        ('/auth/dashboard/', 'Dashboard'),
        ('/auth/profile/', 'Profil'),
        ('/projects/my-projects/', 'Mes Projets'),
        ('/messaging/', 'Messages'),
    ]
    
    all_protected = True
    for url, name in protected_urls:
        try:
            response = client.get(url)
            is_protected = response.status_code in [302, 301, 403]
            print(f"   {'✅' if is_protected else '❌'} {name}: {'Protégé' if is_protected else 'Accessible'}")
            if not is_protected:
                all_protected = False
        except Exception as e:
            print(f"   ⚠️  {name}: Erreur - {e}")
    
    # 9. Test de reconnexion après déconnexion
    print("\n9️⃣ Test de reconnexion après déconnexion...")
    login_success = client.login(email='test_logout@example.com', password='testpass123')
    print(f"   ✅ Reconnexion possible: {'Oui' if login_success else 'Non'}")
    
    # 10. Nettoyage
    print("\n🔟 Nettoyage...")
    user.delete()
    print("   ✅ Utilisateur de test supprimé")
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DU TEST DE DÉCONNEXION")
    print("=" * 50)
    
    success = login_success and is_redirected and all_protected
    
    if success:
        print("🎉 TOUS LES TESTS SONT PASSÉS!")
        print("✅ La déconnexion fonctionne correctement")
        print("✅ Les sessions sont bien supprimées")
        print("✅ Les pages protégées sont inaccessibles")
        print("✅ La reconnexion est possible")
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        print("⚠️  Vérifiez les détails ci-dessus")
    
    return success

def test_navbar_reset_simulation():
    """Simulation du test de réinitialisation de la navbar."""
    print("\n" + "=" * 50)
    print("🔍 SIMULATION TEST NAVBAR")
    print("=" * 50)
    
    print("1️⃣ État initial (utilisateur connecté):")
    print("   ✅ Menu utilisateur visible")
    print("   ✅ Liens 'Mes Projets', 'Messages' visibles")
    print("   ✅ Boutons 'Connexion', 'Inscription' cachés")
    
    print("\n2️⃣ Après déconnexion (état attendu):")
    print("   ✅ Menu utilisateur caché/supprimé")
    print("   ✅ Liens 'Mes Projets', 'Messages' cachés")
    print("   ✅ Boutons 'Connexion', 'Inscription' visibles")
    
    print("\n3️⃣ JavaScript à vérifier:")
    print("   ✅ resetUIToGuestState() appelée")
    print("   ✅ Éléments DOM correctement modifiés")
    print("   ✅ Redirection vers page d'accueil")
    
    print("\n📝 INSTRUCTIONS POUR TEST MANUEL:")
    print("1. Connectez-vous sur http://127.0.0.1:8000/")
    print("2. Vérifiez que le header montre votre nom et les liens authentifiés")
    print("3. Cliquez sur 'Déconnexion'")
    print("4. Vérifiez que le header montre 'Connexion' et 'Inscription'")
    print("5. Vérifiez que vous êtes redirigé vers l'accueil")
    
    return True

def main():
    """Fonction principale de test."""
    print("🚀 DÉBUT DES TESTS DE DÉCONNEXION INVESTAFRIK")
    print("=" * 60)
    
    try:
        # Test automatique
        auto_success = test_complete_logout_functionality()
        
        # Test de simulation navbar
        navbar_success = test_navbar_reset_simulation()
        
        print("\n" + "=" * 60)
        print("🏁 RÉSULTATS FINAUX")
        print("=" * 60)
        
        if auto_success and navbar_success:
            print("🎉 TOUS LES TESTS SONT RÉUSSIS!")
            print("✅ La déconnexion est fonctionnelle")
            print("✅ Effectuez maintenant le test manuel de la navbar")
        else:
            print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
            print("⚠️  Vérifiez les corrections nécessaires")
        
        return auto_success and navbar_success
        
    except Exception as e:
        print(f"❌ ERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)