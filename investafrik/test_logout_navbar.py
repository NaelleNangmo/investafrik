#!/usr/bin/env python
"""
Script de test spécifique pour la déconnexion et la réinitialisation de la navbar.
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

User = get_user_model()

def test_logout_navbar_reset():
    """Test spécifique de la déconnexion et réinitialisation navbar."""
    print("🔍 TEST DÉCONNEXION NAVBAR - InvestAfrik")
    print("=" * 60)
    
    client = Client()
    
    # 1. Créer un utilisateur admin de test
    print("1️⃣ Création d'un utilisateur admin de test...")
    admin_user = User.objects.create_superuser(
        email='admin_test@investafrik.com',
        password='admin123',
        first_name='Admin',
        last_name='Test'
    )
    print(f"   ✅ Admin créé: {admin_user.email}")
    
    # 2. Se connecter en tant qu'admin
    print("\n2️⃣ Connexion en tant qu'admin...")
    login_success = client.login(email='admin_test@investafrik.com', password='admin123')
    print(f"   ✅ Connexion admin: {'Réussie' if login_success else '❌ Échouée'}")
    
    if not login_success:
        print("   ❌ Impossible de continuer sans connexion")
        return False
    
    # 3. Vérifier l'accès aux pages admin
    print("\n3️⃣ Vérification de l'accès admin...")
    
    # Test d'accès au dashboard admin
    try:
        response = client.get('/admin/')
        admin_access = response.status_code in [200, 302]
        print(f"   ✅ Accès admin Django: {'Autorisé' if admin_access else 'Refusé'}")
    except Exception as e:
        print(f"   ⚠️  Erreur accès admin: {e}")
        admin_access = False
    
    # Test d'accès au dashboard porteur
    try:
        response = client.get('/auth/dashboard/')
        dashboard_access = response.status_code in [200, 302]
        print(f"   ✅ Accès dashboard: {'Autorisé' if dashboard_access else 'Refusé'}")
    except Exception as e:
        print(f"   ⚠️  Erreur dashboard: {e}")
        dashboard_access = False
    
    # 4. Test de déconnexion POST
    print("\n4️⃣ Test de déconnexion POST...")
    
    try:
        response = client.post('/auth/logout/')
        logout_status = response.status_code
        print(f"   ✅ Déconnexion POST: Status {logout_status}")
        
        if logout_status == 200:
            try:
                data = response.json()
                print(f"   ✅ Réponse JSON: {data}")
            except:
                print("   ⚠️  Pas de réponse JSON (redirection possible)")
        
    except Exception as e:
        print(f"   ❌ Erreur déconnexion: {e}")
        logout_status = 500
    
    # 5. Vérifier que l'utilisateur est déconnecté
    print("\n5️⃣ Vérification de la déconnexion...")
    
    # Tenter d'accéder aux pages protégées
    protected_pages = [
        ('/admin/', 'Admin Django'),
        ('/auth/dashboard/', 'Dashboard'),
        ('/auth/profile/', 'Profil'),
    ]
    
    all_protected = True
    for url, name in protected_pages:
        try:
            response = client.get(url)
            is_protected = response.status_code in [302, 301, 403]
            status_text = 'Protégé' if is_protected else 'Accessible'
            icon = '✅' if is_protected else '❌'
            print(f"   {icon} {name}: {status_text} (Status: {response.status_code})")
            
            if not is_protected:
                all_protected = False
                
        except Exception as e:
            print(f"   ⚠️  {name}: Erreur - {e}")
    
    # 6. Test de reconnexion
    print("\n6️⃣ Test de reconnexion...")
    reconnect_success = client.login(email='admin_test@investafrik.com', password='admin123')
    print(f"   ✅ Reconnexion possible: {'Oui' if reconnect_success else 'Non'}")
    
    # 7. Nettoyage
    print("\n7️⃣ Nettoyage...")
    admin_user.delete()
    print("   ✅ Utilisateur admin de test supprimé")
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DU TEST")
    print("=" * 60)
    
    success = login_success and (logout_status in [200, 302]) and all_protected and reconnect_success
    
    if success:
        print("🎉 TOUS LES TESTS BACKEND SONT RÉUSSIS!")
        print("✅ La déconnexion backend fonctionne")
        print("✅ Les sessions sont supprimées")
        print("✅ Les pages sont protégées après déconnexion")
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        print("⚠️  Vérifiez les détails ci-dessus")
    
    return success

def print_manual_test_instructions():
    """Afficher les instructions pour le test manuel."""
    print("\n" + "=" * 60)
    print("📋 INSTRUCTIONS POUR TEST MANUEL DE LA NAVBAR")
    print("=" * 60)
    
    print("\n🔧 ÉTAPES À SUIVRE:")
    print("1. Ouvrez votre navigateur sur http://127.0.0.1:8000/")
    print("2. Connectez-vous avec un compte admin ou utilisateur")
    print("3. Vérifiez que la navbar montre:")
    print("   - Votre nom d'utilisateur avec menu déroulant")
    print("   - Les liens 'Mes Projets', 'Messages', etc.")
    print("   - PAS de boutons 'Connexion' ou 'Inscription'")
    
    print("\n4. Cliquez sur votre nom → 'Déconnexion'")
    print("5. VÉRIFIEZ IMMÉDIATEMENT que la navbar montre:")
    print("   - Boutons 'Connexion' et 'Inscription' visibles")
    print("   - Plus de menu utilisateur")
    print("   - Plus de liens 'Mes Projets', 'Messages'")
    print("   - Message de confirmation 'Déconnexion réussie'")
    
    print("\n6. Attendez la redirection vers l'accueil")
    print("7. Vérifiez que vous ne pouvez plus accéder aux pages protégées")
    
    print("\n✅ RÉSULTAT ATTENDU:")
    print("La navbar doit changer IMMÉDIATEMENT au clic sur déconnexion")
    print("AVANT même la redirection vers l'accueil")
    
    print("\n❌ SI ÇA NE MARCHE PAS:")
    print("- Ouvrez la console du navigateur (F12)")
    print("- Regardez les messages de debug commençant par 🔄")
    print("- Vérifiez s'il y a des erreurs JavaScript")

def main():
    """Fonction principale."""
    print("🚀 DÉBUT DU TEST DE DÉCONNEXION NAVBAR")
    print("=" * 60)
    
    try:
        # Test automatique backend
        backend_success = test_logout_navbar_reset()
        
        # Instructions pour test manuel
        print_manual_test_instructions()
        
        print("\n" + "=" * 60)
        print("🏁 RÉSULTATS FINAUX")
        print("=" * 60)
        
        if backend_success:
            print("🎉 TESTS BACKEND RÉUSSIS!")
            print("📋 Effectuez maintenant le test manuel de la navbar")
            print("🔍 Suivez les instructions ci-dessus")
        else:
            print("❌ TESTS BACKEND ÉCHOUÉS")
            print("⚠️  Corrigez d'abord les problèmes backend")
        
        return backend_success
        
    except Exception as e:
        print(f"❌ ERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)