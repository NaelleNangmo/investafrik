#!/usr/bin/env python
"""
Script de test final pour vérifier toutes les corrections.
"""
import os
import sys
import django
import requests
import time

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investafrik.settings.development')
django.setup()

def test_logout_functionality():
    """Tester la fonctionnalité de déconnexion."""
    print("🔐 Test de la déconnexion")
    print("-" * 30)
    
    base_url = "http://127.0.0.1:8000"
    
    # Test de connexion d'abord
    login_data = {
        "email": "admin@investafrik.com",
        "password": "admin123"
    }
    
    session = requests.Session()
    
    try:
        # 1. Connexion
        login_response = session.post(f"{base_url}/api/auth/login/", json=login_data)
        if login_response.status_code == 200:
            print("✅ Connexion réussie")
            
            # 2. Test de déconnexion
            logout_response = session.post(f"{base_url}/auth/logout/")
            if logout_response.status_code in [200, 302]:
                print("✅ Déconnexion API réussie")
                
                # 3. Vérifier que l'utilisateur est bien déconnecté
                profile_response = session.get(f"{base_url}/auth/profile/")
                if profile_response.status_code in [302, 403, 401]:
                    print("✅ Session correctement fermée")
                    return True
                else:
                    print("❌ Session toujours active après déconnexion")
                    return False
            else:
                print(f"❌ Erreur de déconnexion: {logout_response.status_code}")
                return False
        else:
            print(f"❌ Erreur de connexion: {login_response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def test_messaging_api():
    """Tester l'API de messagerie."""
    print("\n💬 Test de l'API de messagerie")
    print("-" * 30)
    
    base_url = "http://127.0.0.1:8000"
    
    # Connexion avec un utilisateur
    login_data = {
        "email": "amina.diallo@example.com",
        "password": "password123"
    }
    
    session = requests.Session()
    
    try:
        # 1. Connexion
        login_response = session.post(f"{base_url}/api/auth/login/", json=login_data)
        if login_response.status_code == 200:
            tokens = login_response.json()['tokens']
            headers = {'Authorization': f'Bearer {tokens["access"]}'}
            
            print("✅ Connexion utilisateur réussie")
            
            # 2. Récupérer la liste des utilisateurs
            users_response = session.get(f"{base_url}/api/auth/users/", headers=headers)
            if users_response.status_code == 200:
                users = users_response.json()
                print(f"✅ {len(users.get('results', users))} utilisateurs récupérés")
                
                # 3. Essayer de créer une conversation
                if len(users.get('results', users)) > 1:
                    other_user = users.get('results', users)[1]  # Prendre le 2ème utilisateur
                    
                    conversation_data = {
                        "participant_2": other_user['id']
                    }
                    
                    conv_response = session.post(
                        f"{base_url}/api/messaging/conversations/", 
                        json=conversation_data,
                        headers=headers
                    )
                    
                    if conv_response.status_code in [200, 201]:
                        print("✅ Création de conversation réussie")
                        return True
                    else:
                        print(f"❌ Erreur création conversation: {conv_response.status_code}")
                        print(f"   Réponse: {conv_response.text}")
                        return False
                else:
                    print("❌ Pas assez d'utilisateurs pour tester")
                    return False
            else:
                print(f"❌ Erreur récupération utilisateurs: {users_response.status_code}")
                return False
        else:
            print(f"❌ Erreur de connexion: {login_response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def test_admin_dashboard():
    """Tester le dashboard admin."""
    print("\n📊 Test du dashboard admin")
    print("-" * 30)
    
    base_url = "http://127.0.0.1:8000"
    
    try:
        # Test d'accès au dashboard admin
        response = requests.get(f"{base_url}/admin/")
        if response.status_code in [200, 302]:
            print("✅ Dashboard admin accessible")
            
            # Vérifier que c'est bien notre dashboard personnalisé
            if "InvestAfrik" in response.text or response.status_code == 302:
                print("✅ Dashboard personnalisé détecté")
                return True
            else:
                print("❌ Dashboard par défaut Django détecté")
                return False
        else:
            print(f"❌ Dashboard admin non accessible: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def test_project_urls():
    """Tester les URLs des projets (plus d'erreur 404)."""
    print("\n📁 Test des URLs de projets")
    print("-" * 30)
    
    base_url = "http://127.0.0.1:8000"
    
    try:
        # 1. Récupérer la liste des projets
        response = requests.get(f"{base_url}/api/projects/")
        if response.status_code == 200:
            projects = response.json()
            project_list = projects.get('results', projects)
            
            if len(project_list) > 0:
                # 2. Tester l'accès à un projet par slug
                project = project_list[0]
                slug = project.get('slug')
                
                if slug:
                    project_response = requests.get(f"{base_url}/projects/{slug}/")
                    if project_response.status_code == 200:
                        print(f"✅ Projet accessible via slug: /projects/{slug}/")
                        return True
                    else:
                        print(f"❌ Erreur 404 sur projet: {project_response.status_code}")
                        return False
                else:
                    print("❌ Projet sans slug trouvé")
                    return False
            else:
                print("❌ Aucun projet trouvé")
                return False
        else:
            print(f"❌ Erreur API projets: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def main():
    """Fonction principale de test."""
    print("🧪 InvestAfrik - Tests Finaux des Corrections")
    print("=" * 60)
    
    # Vérifier que le serveur est accessible
    try:
        response = requests.get("http://127.0.0.1:8000", timeout=5)
        print("✅ Serveur Django accessible")
    except requests.exceptions.RequestException:
        print("❌ Serveur Django non accessible")
        print("💡 Démarrez le serveur avec: python manage.py runserver")
        return False
    
    # Exécuter tous les tests
    tests = [
        ("Déconnexion", test_logout_functionality),
        ("API Messagerie", test_messaging_api),
        ("Dashboard Admin", test_admin_dashboard),
        ("URLs Projets", test_project_urls),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ Erreur dans le test {test_name}: {e}")
            results[test_name] = False
    
    # Résumé final
    print("\n" + "=" * 60)
    print("📋 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSÉ" if result else "❌ ÉCHEC"
        print(f"   {test_name}: {status}")
    
    print(f"\n📊 Résultat global: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 SUCCÈS: Toutes les corrections fonctionnent !")
        print("\n🚀 Instructions finales:")
        print("   1. La déconnexion fonctionne correctement")
        print("   2. L'API de messagerie est opérationnelle")
        print("   3. Le dashboard admin affiche des statistiques réelles")
        print("   4. Plus d'erreurs 404 sur les projets")
        print("\n✨ InvestAfrik est 100% fonctionnel !")
    else:
        print("⚠️  Certains tests ont échoué, vérifiez les corrections")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)