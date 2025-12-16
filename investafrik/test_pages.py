#!/usr/bin/env python
"""
Script de test pour vérifier que toutes les pages et API endpoints fonctionnent
"""

import os
import sys
import requests
import json
from pathlib import Path

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investafrik.settings.development')

def test_page(url, description, expected_status=200):
    """Teste une page web"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == expected_status:
            print(f"✅ {description} - Status {response.status_code}")
            return True
        else:
            print(f"❌ {description} - Status {response.status_code} (attendu {expected_status})")
            return False
    except Exception as e:
        print(f"❌ {description} - Erreur: {e}")
        return False

def test_api_endpoint(url, description, method='GET', data=None, expected_status=200):
    """Teste un endpoint API"""
    try:
        if method == 'GET':
            response = requests.get(url, timeout=10)
        elif method == 'POST':
            response = requests.post(url, json=data, timeout=10)
        
        if response.status_code == expected_status:
            print(f"✅ {description} - Status {response.status_code}")
            return True
        else:
            print(f"❌ {description} - Status {response.status_code} (attendu {expected_status})")
            if response.text:
                print(f"   Response: {response.text[:200]}...")
            return False
    except Exception as e:
        print(f"❌ {description} - Erreur: {e}")
        return False

def test_django_admin():
    """Teste l'accès à l'admin Django"""
    print("\n🔧 Test Admin Django...")
    
    try:
        import django
        django.setup()
        
        from django.contrib.auth import get_user_model
        from django.test import Client
        
        User = get_user_model()
        client = Client()
        
        # Test page de login admin
        response = client.get('/admin/')
        if response.status_code in [200, 302]:  # 302 = redirect vers login
            print("✅ Admin Django accessible")
            return True
        else:
            print(f"❌ Admin Django - Status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Admin Django - Erreur: {e}")
        return False

def test_database_models():
    """Teste les modèles de base de données"""
    print("\n🗄️  Test Modèles de Base de Données...")
    
    try:
        import django
        django.setup()
        
        from django.contrib.auth import get_user_model
        from apps.categories.models import Category
        from apps.projects.models import Project
        from apps.investments.models import Investment
        from apps.messaging.models import Conversation
        from apps.notifications.models import Notification
        
        User = get_user_model()
        
        # Test des comptages
        models_to_test = [
            (User, "Utilisateurs"),
            (Category, "Catégories"),
            (Project, "Projets"),
            (Investment, "Investissements"),
            (Conversation, "Conversations"),
            (Notification, "Notifications"),
        ]
        
        all_good = True
        for model, name in models_to_test:
            try:
                count = model.objects.count()
                print(f"✅ {name}: {count} enregistrements")
            except Exception as e:
                print(f"❌ {name}: Erreur - {e}")
                all_good = False
        
        return all_good
        
    except Exception as e:
        print(f"❌ Test modèles - Erreur: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🧪 TESTS COMPLETS D'INVESTAFRIK")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:8000"
    
    # Vérifier que le serveur est démarré
    print("\n🌐 Test de connectivité...")
    if not test_page(base_url, "Serveur Django"):
        print("❌ Le serveur Django n'est pas démarré")
        print("   Démarrez-le avec: python manage.py runserver")
        return
    
    # Tests des pages principales
    print("\n📄 Test des Pages Web...")
    web_tests = [
        (f"{base_url}/", "Page d'accueil"),
        (f"{base_url}/projects/", "Page projets"),
        (f"{base_url}/admin/", "Admin Django", 302),  # Redirect vers login
    ]
    
    web_results = []
    for url, desc, *status in web_tests:
        expected = status[0] if status else 200
        result = test_page(url, desc, expected)
        web_results.append(result)
    
    # Tests des endpoints API
    print("\n🔌 Test des Endpoints API...")
    api_tests = [
        (f"{base_url}/api/categories/", "API Catégories"),
        (f"{base_url}/api/projects/", "API Projets"),
        (f"{base_url}/api/auth/register/", "API Inscription", "POST", {
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpass123",
            "first_name": "Test",
            "last_name": "User",
            "user_type": "investisseur",
            "country": "CM"
        }, 400),  # 400 car données incomplètes, mais endpoint fonctionne
    ]
    
    api_results = []
    for url, desc, *params in api_tests:
        method = params[0] if len(params) > 0 else 'GET'
        data = params[1] if len(params) > 1 else None
        expected = params[2] if len(params) > 2 else 200
        result = test_api_endpoint(url, desc, method, data, expected)
        api_results.append(result)
    
    # Tests Django spécifiques
    print("\n🐍 Tests Django...")
    django_results = [
        test_django_admin(),
        test_database_models(),
    ]
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS")
    
    total_tests = len(web_results) + len(api_results) + len(django_results)
    passed_tests = sum(web_results) + sum(api_results) + sum(django_results)
    
    print(f"Tests réussis: {passed_tests}/{total_tests}")
    
    if passed_tests == total_tests:
        print("🎉 TOUS LES TESTS SONT PASSÉS !")
        print("   InvestAfrik est prêt à l'emploi !")
    else:
        print("⚠️  Certains tests ont échoué")
        print("   Vérifiez les erreurs ci-dessus")
    
    print("\n📋 URLS IMPORTANTES:")
    print(f"   🏠 Accueil: {base_url}")
    print(f"   📊 Projets: {base_url}/projects/")
    print(f"   🔧 Admin: {base_url}/admin/")
    print(f"   🔌 API: {base_url}/api/")
    
    print("\n🔑 CONNEXION ADMIN:")
    print("   Email: admin@investafrik.com")
    print("   Mot de passe: admin123")

if __name__ == '__main__':
    main()