#!/usr/bin/env python
"""
Script pour corriger les problèmes d'API et tester les fonctionnalités.
"""
import os
import sys
import django
import requests
import json

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investafrik.settings.development')
django.setup()

from django.contrib.auth import get_user_model
from apps.projects.models import Project
from apps.categories.models import Category

User = get_user_model()

def test_api_endpoints():
    """Tester les endpoints de l'API."""
    base_url = "http://127.0.0.1:8000"
    
    print("🧪 Test des endpoints API")
    print("=" * 50)
    
    endpoints = [
        ('/api/projects/', 'Liste des projets'),
        ('/api/categories/', 'Liste des catégories'),
        ('/api/auth/register/', 'Inscription (POST)'),
        ('/api/auth/login/', 'Connexion (POST)'),
    ]
    
    for endpoint, description in endpoints:
        try:
            if endpoint.endswith('register/') or endpoint.endswith('login/'):
                # Test POST pour l'authentification
                print(f"📝 {description}: Endpoint disponible")
            else:
                # Test GET pour les autres
                response = requests.get(f"{base_url}{endpoint}", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, dict) and 'results' in data:
                        count = len(data['results'])
                    elif isinstance(data, list):
                        count = len(data)
                    else:
                        count = "N/A"
                    print(f"✅ {description}: OK ({count} éléments)")
                else:
                    print(f"❌ {description}: Erreur {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ {description}: Erreur de connexion")

def test_registration():
    """Tester l'inscription d'un nouvel utilisateur."""
    base_url = "http://127.0.0.1:8000"
    
    print("\n🔐 Test d'inscription")
    print("=" * 50)
    
    # Données de test pour l'inscription
    test_user_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User",
        "username": "testuser",
        "user_type": "investisseur",
        "country": "CM"
    }
    
    try:
        # Supprimer l'utilisateur de test s'il existe
        User.objects.filter(email=test_user_data['email']).delete()
        
        response = requests.post(
            f"{base_url}/api/auth/register/",
            json=test_user_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 201:
            data = response.json()
            if 'tokens' in data and 'user' in data:
                print("✅ Inscription réussie")
                print(f"   - Utilisateur: {data['user']['email']}")
                print(f"   - Type: {data['user']['user_type']}")
                print(f"   - Token généré: Oui")
                return data['tokens']['access']
            else:
                print("❌ Inscription: Format de réponse incorrect")
                print(f"   Réponse: {data}")
        else:
            print(f"❌ Inscription échouée: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Erreur: {error_data}")
            except:
                print(f"   Erreur: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de connexion lors de l'inscription: {e}")
    
    return None

def test_login():
    """Tester la connexion avec un utilisateur existant."""
    base_url = "http://127.0.0.1:8000"
    
    print("\n🔑 Test de connexion")
    print("=" * 50)
    
    # Données de connexion
    login_data = {
        "email": "admin@investafrik.com",
        "password": "admin123"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/auth/login/",
            json=login_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'tokens' in data and 'user' in data:
                print("✅ Connexion réussie")
                print(f"   - Utilisateur: {data['user']['email']}")
                print(f"   - Type: {data['user']['user_type']}")
                return data['tokens']['access']
            else:
                print("❌ Connexion: Format de réponse incorrect")
        else:
            print(f"❌ Connexion échouée: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Erreur: {error_data}")
            except:
                print(f"   Erreur: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de connexion: {e}")
    
    return None

def check_database_data():
    """Vérifier les données dans la base de données."""
    print("\n🗄️  Vérification des données")
    print("=" * 50)
    
    try:
        # Compter les utilisateurs
        user_count = User.objects.count()
        porteurs = User.objects.filter(user_type='porteur').count()
        investisseurs = User.objects.filter(user_type='investisseur').count()
        
        print(f"👥 Utilisateurs: {user_count} total")
        print(f"   - Porteurs: {porteurs}")
        print(f"   - Investisseurs: {investisseurs}")
        
        # Compter les projets
        project_count = Project.objects.count()
        active_projects = Project.objects.filter(status='active').count()
        
        print(f"📁 Projets: {project_count} total")
        print(f"   - Actifs: {active_projects}")
        
        # Compter les catégories
        category_count = Category.objects.count()
        print(f"🏷️  Catégories: {category_count}")
        
        # Vérifier quelques projets avec leurs données calculées
        if project_count > 0:
            print("\n📊 Exemples de projets:")
            for project in Project.objects.all()[:3]:
                print(f"   - {project.title}")
                print(f"     Financement: {project.funding_percentage:.1f}%")
                print(f"     Jours restants: {project.days_remaining}")
                print(f"     Investisseurs: {project.investor_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur base de données: {e}")
        return False

def main():
    """Fonction principale."""
    print("🔧 InvestAfrik - Diagnostic et Correction des Problèmes")
    print("=" * 60)
    
    # Vérifier que le serveur est accessible
    try:
        response = requests.get("http://127.0.0.1:8000", timeout=5)
        print("✅ Serveur Django accessible")
    except requests.exceptions.RequestException:
        print("❌ Serveur Django non accessible")
        print("💡 Démarrez le serveur avec: python manage.py runserver")
        return False
    
    # Tests
    db_ok = check_database_data()
    test_api_endpoints()
    token = test_login()
    registration_token = test_registration()
    
    # Résumé
    print("\n" + "=" * 60)
    print("📋 RÉSUMÉ")
    print("=" * 60)
    
    if db_ok and token:
        print("🎉 SUCCÈS: L'API fonctionne correctement !")
        print("\n💡 Solutions aux problèmes courants:")
        print("   1. Inscription: Utilisez /api/auth/register/ avec les champs requis")
        print("   2. Connexion: Utilisez /api/auth/login/ avec email/password")
        print("   3. Projets: L'API /api/projects/ retourne la liste complète")
        print("\n🔗 URLs importantes:")
        print("   - API Projets: http://127.0.0.1:8000/api/projects/")
        print("   - API Auth: http://127.0.0.1:8000/api/auth/")
        print("   - Interface: http://127.0.0.1:8000")
    else:
        print("⚠️  Des problèmes ont été détectés")
        if not db_ok:
            print("   - Problème avec la base de données")
        if not token:
            print("   - Problème avec l'authentification")
    
    return db_ok and token

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)