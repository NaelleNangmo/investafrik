#!/usr/bin/env python
"""
Test final de la déconnexion avec vérification de la navbar.
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

def test_logout_functionality():
    """Test final de la déconnexion."""
    print("🔍 TEST FINAL - DÉCONNEXION NAVBAR")
    print("=" * 50)
    
    client = Client()
    
    # 1. Créer un utilisateur de test
    print("1️⃣ Création d'un utilisateur de test...")
    try:
        user = User.objects.create_user(
            email='test_final@investafrik.com',
            password='testpass123',
            first_name='Test',
            last_name='Final',
            user_type='porteur',
            country='CM'
        )
        print(f"   ✅ Utilisateur créé: {user.email}")
    except Exception as e:
        print(f"   ❌ Erreur création utilisateur: {e}")
        return False
    
    # 2. Test de connexion
    print("\n2️⃣ Test de connexion...")
    try:
        login_success = client.login(email='test_final@investafrik.com', password='testpass123')
        print(f"   ✅ Connexion: {'Réussie' if login_success else '❌ Échouée'}")
        
        if not login_success:
            user.delete()
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur connexion: {e}")
        user.delete()
        return False
    
    # 3. Test de déconnexion POST
    print("\n3️⃣ Test de déconnexion POST...")
    try:
        response = client.post('/auth/logout/')
        print(f"   ✅ Déconnexion POST: Status {response.status_code}")
        
        # Vérifier le type de réponse
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   ✅ Réponse JSON: {data}")
            except:
                print("   ⚠️  Réponse non-JSON (redirection possible)")
        elif response.status_code in [301, 302]:
            print(f"   ✅ Redirection vers: {response.url}")
        
    except Exception as e:
        print(f"   ❌ Erreur déconnexion: {e}")
    
    # 4. Vérifier que l'utilisateur est déconnecté
    print("\n4️⃣ Vérification de la déconnexion...")
    
    protected_urls = [
        ('/auth/dashboard/', 'Dashboard'),
        ('/auth/profile/', 'Profil'),
        ('/projects/my-projects/', 'Mes Projets'),
    ]
    
    all_protected = True
    for url, name in protected_urls:
        try:
            response = client.get(url)
            is_protected = response.status_code in [302, 301, 403]
            status_text = 'Protégé' if is_protected else 'Accessible'
            icon = '✅' if is_protected else '❌'
            print(f"   {icon} {name}: {status_text}")
            
            if not is_protected:
                all_protected = False
                
        except Exception as e:
            print(f"   ⚠️  {name}: Erreur - {e}")
    
    # 5. Test de reconnexion
    print("\n5️⃣ Test de reconnexion...")
    try:
        reconnect_success = client.login(email='test_final@investafrik.com', password='testpass123')
        print(f"   ✅ Reconnexion: {'Possible' if reconnect_success else 'Impossible'}")
    except Exception as e:
        print(f"   ❌ Erreur reconnexion: {e}")
        reconnect_success = False
    
    # 6. Nettoyage
    print("\n6️⃣ Nettoyage...")
    try:
        user.delete()
        print("   ✅ Utilisateur de test supprimé")
    except Exception as e:
        print(f"   ⚠️  Erreur nettoyage: {e}")
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DU TEST")
    print("=" * 50)
    
    success = login_success and all_protected and reconnect_success
    
    if success:
        print("🎉 TOUS LES TESTS BACKEND SONT RÉUSSIS!")
        print("✅ La déconnexion backend fonctionne")
        print("✅ Les sessions sont supprimées")
        print("✅ Les pages sont protégées")
        print("✅ La reconnexion est possible")
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        print("⚠️  Vérifiez les détails ci-dessus")
    
    return success

def print_manual_instructions():
    """Instructions pour le test manuel."""
    print("\n" + "=" * 50)
    print("📋 INSTRUCTIONS POUR TEST MANUEL")
    print("=" * 50)
    
    print("\n🎯 OBJECTIF:")
    print("Vérifier que la navbar se réinitialise IMMÉDIATEMENT au clic sur déconnexion")
    
    print("\n🔧 ÉTAPES:")
    print("1. Ouvrez http://127.0.0.1:8000/ dans votre navigateur")
    print("2. Connectez-vous avec n'importe quel compte")
    print("3. Ouvrez la console du navigateur (F12)")
    print("4. Cliquez sur votre nom → 'Déconnexion'")
    
    print("\n✅ RÉSULTAT ATTENDU (IMMÉDIAT):")
    print("- Menu utilisateur disparaît")
    print("- Boutons 'Connexion' et 'Inscription' apparaissent")
    print("- Liens 'Mes Projets', 'Messages' disparaissent")
    print("- Message 'Déconnexion réussie' s'affiche")
    print("- Console montre les messages de debug 🔄")
    
    print("\n🔍 MESSAGES DE DEBUG ATTENDUS:")
    print("🔄 DÉBUT - Déconnexion initiée...")
    print("📝 Remplacement du conteneur d'authentification...")
    print("✅ Boutons Connexion/Inscription affichés dans le header")
    print("🔒 Lien desktop masqué: Mes Projets")
    print("🔒 Lien desktop masqué: Messages")
    print("✅ FIN - Interface utilisateur complètement réinitialisée")
    print("🎉 SUCCÈS - Boutons guest visibles!")
    
    print("\n❌ SI ÇA NE MARCHE PAS:")
    print("- Vérifiez les erreurs JavaScript dans la console")
    print("- Rechargez la page (Ctrl+F5)")
    print("- Testez en navigation privée")
    print("- Ouvrez test_logout_simple.html pour comparer")

def main():
    """Fonction principale."""
    print("🚀 TEST FINAL DE DÉCONNEXION INVESTAFRIK")
    print("=" * 60)
    
    try:
        # Test automatique
        backend_success = test_logout_functionality()
        
        # Instructions manuelles
        print_manual_instructions()
        
        print("\n" + "=" * 60)
        print("🏁 CONCLUSION")
        print("=" * 60)
        
        if backend_success:
            print("🎉 TESTS BACKEND RÉUSSIS!")
            print("📋 La déconnexion backend fonctionne parfaitement")
            print("🧪 Effectuez maintenant le test manuel de la navbar")
            print("🔍 Suivez les instructions ci-dessus")
            print("\n💡 RAPPEL: La navbar doit changer IMMÉDIATEMENT au clic!")
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
    print(f"\n{'🎉 SUCCÈS' if success else '❌ ÉCHEC'} - Test terminé")
    sys.exit(0 if success else 1)