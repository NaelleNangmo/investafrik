#!/usr/bin/env python
"""
Test direct de la déconnexion sur l'application InvestAfrik en cours d'exécution.
Ce script lance le serveur et teste la déconnexion en temps réel.
"""
import os
import sys
import django
import time
import subprocess
import threading
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investafrik.settings.development')
django.setup()

from django.contrib.auth import get_user_model
from django.core.management import execute_from_command_line

User = get_user_model()

def create_test_user():
    """Créer un utilisateur de test."""
    print("👤 Création d'un utilisateur de test...")
    
    # Supprimer l'utilisateur s'il existe déjà
    User.objects.filter(email='test_deconnexion@investafrik.com').delete()
    
    # Créer un nouvel utilisateur
    user = User.objects.create_user(
        email='test_deconnexion@investafrik.com',
        password='test123',
        first_name='Test',
        last_name='Deconnexion',
        user_type='porteur',
        country='CM'
    )
    
    print(f"✅ Utilisateur créé: {user.email}")
    print(f"🔑 Mot de passe: test123")
    return user

def start_server():
    """Démarrer le serveur Django."""
    print("🚀 Démarrage du serveur Django...")
    try:
        # Utiliser subprocess pour démarrer le serveur
        process = subprocess.Popen([
            sys.executable, 'manage.py', 'runserver', '127.0.0.1:8000',
            '--settings=investafrik.settings.development'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Attendre que le serveur démarre
        time.sleep(3)
        
        print("✅ Serveur démarré sur http://127.0.0.1:8000/")
        return process
    except Exception as e:
        print(f"❌ Erreur démarrage serveur: {e}")
        return None

def print_test_instructions():
    """Afficher les instructions de test."""
    print("\n" + "=" * 60)
    print("🧪 INSTRUCTIONS DE TEST DIRECT")
    print("=" * 60)
    
    print("\n🎯 OBJECTIF:")
    print("Tester la déconnexion sur l'application réelle en cours d'exécution")
    
    print("\n📋 ÉTAPES À SUIVRE:")
    print("1. Ouvrez votre navigateur sur: http://127.0.0.1:8000/")
    print("2. Connectez-vous avec:")
    print("   📧 Email: test_deconnexion@investafrik.com")
    print("   🔑 Mot de passe: test123")
    
    print("\n3. Une fois connecté, vérifiez que vous voyez:")
    print("   ✅ Votre nom 'Test Deconnexion' dans le header")
    print("   ✅ Menu déroulant avec Dashboard, Mon Profil, Déconnexion")
    print("   ✅ Liens 'Mes Projets', 'Messages' dans la navbar")
    print("   ❌ PAS de boutons 'Connexion' ou 'Inscription'")
    
    print("\n4. Ouvrez la console du navigateur (F12)")
    
    print("\n5. Cliquez sur votre nom → 'Déconnexion'")
    
    print("\n✅ RÉSULTAT ATTENDU (IMMÉDIAT):")
    print("   🔄 Menu utilisateur disparaît IMMÉDIATEMENT")
    print("   🔄 Boutons 'Connexion' et 'Inscription' apparaissent IMMÉDIATEMENT")
    print("   🔄 Liens 'Mes Projets', 'Messages' disparaissent IMMÉDIATEMENT")
    print("   💬 Message 'Déconnexion réussie' s'affiche")
    print("   🔄 Redirection vers l'accueil après 1 seconde")
    
    print("\n🔍 MESSAGES DE DEBUG DANS LA CONSOLE:")
    print("   🔄 Début de la déconnexion...")
    print("   🔄 DÉBUT - Réinitialisation de l'interface utilisateur...")
    print("   📝 Remplacement du conteneur d'authentification...")
    print("   ✅ Boutons Connexion/Inscription affichés dans le header")
    print("   🔒 Lien desktop masqué: Mes Projets")
    print("   🔒 Lien desktop masqué: Messages")
    print("   ✅ FIN - Interface utilisateur complètement réinitialisée")
    print("   🎉 SUCCÈS - Boutons guest visibles!")
    
    print("\n❌ SI ÇA NE MARCHE PAS:")
    print("   - Vérifiez les erreurs JavaScript dans la console")
    print("   - Rechargez la page (Ctrl+F5)")
    print("   - Vérifiez que le CSRF token est présent")
    print("   - Testez en navigation privée")
    
    print("\n⚠️  IMPORTANT:")
    print("   La transformation de la navbar doit être IMMÉDIATE")
    print("   AVANT même la redirection vers l'accueil!")

def cleanup_test_user():
    """Nettoyer l'utilisateur de test."""
    print("\n🧹 Nettoyage...")
    try:
        User.objects.filter(email='test_deconnexion@investafrik.com').delete()
        print("✅ Utilisateur de test supprimé")
    except Exception as e:
        print(f"⚠️  Erreur nettoyage: {e}")

def main():
    """Fonction principale."""
    print("🚀 TEST DIRECT DE DÉCONNEXION - INVESTAFRIK")
    print("=" * 60)
    
    try:
        # 1. Créer l'utilisateur de test
        user = create_test_user()
        
        # 2. Afficher les instructions
        print_test_instructions()
        
        # 3. Demander confirmation pour continuer
        print("\n" + "=" * 60)
        print("⏳ PRÊT POUR LE TEST")
        print("=" * 60)
        
        input("\n🔥 Appuyez sur ENTRÉE pour démarrer le serveur et commencer le test...")
        
        # 4. Démarrer le serveur
        server_process = start_server()
        
        if server_process:
            print("\n🎉 SERVEUR DÉMARRÉ AVEC SUCCÈS!")
            print("🌐 Ouvrez maintenant votre navigateur sur: http://127.0.0.1:8000/")
            print("📋 Suivez les instructions ci-dessus pour tester la déconnexion")
            
            # 5. Attendre que l'utilisateur termine le test
            input("\n⏹️  Appuyez sur ENTRÉE quand vous avez terminé le test...")
            
            # 6. Arrêter le serveur
            print("\n🛑 Arrêt du serveur...")
            server_process.terminate()
            server_process.wait()
            print("✅ Serveur arrêté")
        
        # 7. Nettoyage
        cleanup_test_user()
        
        print("\n" + "=" * 60)
        print("🏁 TEST TERMINÉ")
        print("=" * 60)
        print("✅ Si la navbar s'est réinitialisée immédiatement, le test est RÉUSSI!")
        print("❌ Si la navbar n'a pas changé, il y a encore un problème à corriger.")
        
        return True
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrompu par l'utilisateur")
        cleanup_test_user()
        return False
        
    except Exception as e:
        print(f"\n❌ ERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()
        cleanup_test_user()
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)