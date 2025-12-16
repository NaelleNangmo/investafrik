#!/usr/bin/env python
"""
Script de test complet pour vérifier que toutes les pages d'InvestAfrik fonctionnent.
"""
import os
import sys
import django
import requests
from django.core.management import execute_from_command_line

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investafrik.settings.development')
django.setup()

def test_pages():
    """Test toutes les pages principales de l'application."""
    base_url = "http://127.0.0.1:8000"
    
    pages_to_test = [
        # Pages publiques
        ('/', 'Page d\'accueil'),
        ('/projects/', 'Liste des projets'),
        ('/how-it-works/', 'Comment ça marche'),
        ('/about/', 'À propos'),
        ('/auth/login/', 'Page de connexion'),
        ('/auth/register/', 'Page d\'inscription'),
        
        # API endpoints (sans authentification)
        ('/api/projects/', 'API Projets'),
        ('/api/categories/', 'API Catégories'),
        
        # Admin
        ('/admin/', 'Interface d\'administration'),
    ]
    
    print("🧪 Test des pages InvestAfrik")
    print("=" * 50)
    
    success_count = 0
    total_count = len(pages_to_test)
    
    for url, description in pages_to_test:
        try:
            response = requests.get(f"{base_url}{url}", timeout=10)
            if response.status_code == 200:
                print(f"✅ {description}: OK ({response.status_code})")
                success_count += 1
            elif response.status_code == 302:
                print(f"🔄 {description}: Redirection ({response.status_code})")
                success_count += 1
            else:
                print(f"❌ {description}: Erreur {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ {description}: Erreur de connexion - {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Résultats: {success_count}/{total_count} pages fonctionnelles")
    
    if success_count == total_count:
        print("🎉 Toutes les pages fonctionnent parfaitement !")
    else:
        print(f"⚠️  {total_count - success_count} page(s) nécessitent une attention")
    
    return success_count == total_count

def check_database():
    """Vérifie la connexion à la base de données et les données."""
    from apps.accounts.models import User
    from apps.projects.models import Project
    from apps.categories.models import Category
    
    print("\n🗄️  Vérification de la base de données")
    print("=" * 50)
    
    try:
        # Compter les utilisateurs
        user_count = User.objects.count()
        print(f"👥 Utilisateurs: {user_count}")
        
        # Compter les projets
        project_count = Project.objects.count()
        print(f"📁 Projets: {project_count}")
        
        # Compter les catégories
        category_count = Category.objects.count()
        print(f"🏷️  Catégories: {category_count}")
        
        # Vérifier les types d'utilisateurs
        porteurs = User.objects.filter(user_type='porteur').count()
        investisseurs = User.objects.filter(user_type='investisseur').count()
        print(f"🚀 Porteurs de projets: {porteurs}")
        print(f"💰 Investisseurs: {investisseurs}")
        
        print("✅ Base de données opérationnelle")
        return True
        
    except Exception as e:
        print(f"❌ Erreur base de données: {e}")
        return False

def check_authentication():
    """Teste l'authentification via l'API."""
    print("\n🔐 Test de l'authentification")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:8000"
    
    # Test de connexion avec un utilisateur existant
    login_data = {
        "email": "admin@investafrik.com",
        "password": "admin123"
    }
    
    try:
        response = requests.post(f"{base_url}/api/auth/login/", json=login_data, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'tokens' in data and 'access' in data['tokens']:
                print("✅ Authentification JWT fonctionnelle")
                return True
            else:
                print("❌ Format de réponse d'authentification incorrect")
                return False
        else:
            print(f"❌ Erreur d'authentification: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de connexion API: {e}")
        return False

def main():
    """Fonction principale de test."""
    print("🚀 InvestAfrik - Test Complet de l'Application")
    print("=" * 60)
    
    # Vérifier que le serveur est démarré
    try:
        response = requests.get("http://127.0.0.1:8000", timeout=5)
        print("✅ Serveur Django démarré et accessible")
    except requests.exceptions.RequestException:
        print("❌ Serveur Django non accessible")
        print("💡 Assurez-vous que le serveur est démarré avec: python manage.py runserver")
        return False
    
    # Tests
    db_ok = check_database()
    auth_ok = check_authentication()
    pages_ok = test_pages()
    
    # Résumé final
    print("\n" + "=" * 60)
    print("📋 RÉSUMÉ FINAL")
    print("=" * 60)
    
    if db_ok and auth_ok and pages_ok:
        print("🎉 SUCCÈS: InvestAfrik est 100% fonctionnel !")
        print("\n📍 Accès à l'application:")
        print("   🏠 Site web: http://127.0.0.1:8000")
        print("   🔧 Admin: http://127.0.0.1:8000/admin")
        print("   📚 API: http://127.0.0.1:8000/api")
        print("\n🔑 Comptes de test:")
        print("   Admin: admin@investafrik.com / admin123")
        print("   Porteur: amina.diallo@example.com / password123")
        print("   Investisseur: jean.dupont@example.com / password123")
        return True
    else:
        print("⚠️  ATTENTION: Certains composants nécessitent une vérification")
        if not db_ok:
            print("   - Base de données")
        if not auth_ok:
            print("   - Authentification")
        if not pages_ok:
            print("   - Pages web")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)