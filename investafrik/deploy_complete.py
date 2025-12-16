#!/usr/bin/env python
"""
Script de déploiement complet pour InvestAfrik
Ce script configure tout l'environnement de A à Z
"""

import os
import sys
import subprocess
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from pathlib import Path

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investafrik.settings.development')

def run_command(command, description, ignore_errors=False):
    """Exécute une commande et affiche le résultat"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Succès")
        if result.stdout.strip():
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        if ignore_errors:
            print(f"⚠️  {description} - Ignoré")
            if e.stderr:
                print(f"   Warning: {e.stderr.strip()}")
            return True
        else:
            print(f"❌ {description} - Erreur")
            if e.stderr:
                print(f"   Error: {e.stderr.strip()}")
            return False

def setup_postgres():
    """Configure PostgreSQL"""
    print("\n🗄️  Configuration PostgreSQL...")
    
    try:
        # Tenter de se connecter
        conn = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='noutong1',
            port='5432'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Créer la base de données
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'invest_afbd'")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute('CREATE DATABASE invest_afbd')
            print("✅ Base de données 'invest_afbd' créée")
        else:
            print("✅ Base de données 'invest_afbd' existe déjà")
            
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur PostgreSQL: {e}")
        print("   Solutions possibles:")
        print("   1. Installer PostgreSQL: https://www.postgresql.org/download/")
        print("   2. Démarrer le service PostgreSQL")
        print("   3. Configurer l'utilisateur postgres avec le mot de passe 'noutong1'")
        print("   4. Ou utiliser SQLite en modifiant settings/development.py")
        return False

def setup_environment():
    """Configure l'environnement"""
    print("\n⚙️  Configuration de l'environnement...")
    
    # Le fichier .env existe déjà, on le vérifie
    env_file = Path('.env')
    if env_file.exists():
        print("✅ Fichier .env existe")
        return True
    else:
        print("❌ Fichier .env manquant")
        return False

def install_dependencies():
    """Installe toutes les dépendances"""
    print("\n📦 Installation des dépendances...")
    
    # Python dependencies
    if not run_command("pip install -r requirements.txt", "Installation dépendances Python"):
        return False
    
    # Node.js dependencies (optionnel)
    if Path('package.json').exists():
        run_command("npm install", "Installation dépendances Node.js", ignore_errors=True)
        run_command("npm run build", "Compilation Tailwind CSS", ignore_errors=True)
    
    return True

def setup_django():
    """Configure Django"""
    print("\n🐍 Configuration Django...")
    
    # Migrations
    if not run_command("python manage.py makemigrations", "Création des migrations", ignore_errors=True):
        print("   Continuons...")
    
    if not run_command("python manage.py migrate", "Application des migrations"):
        return False
    
    # Collecte des fichiers statiques
    run_command("python manage.py collectstatic --noinput", "Collecte fichiers statiques", ignore_errors=True)
    
    return True

def load_data():
    """Charge les données de test"""
    print("\n📊 Chargement des données...")
    
    # Données de test
    if not run_command("python manage.py seed_data", "Chargement données de test"):
        print("   Continuons sans données de test...")
    
    # Superutilisateur
    create_superuser_cmd = (
        "python manage.py shell -c \""
        "from django.contrib.auth import get_user_model; "
        "User = get_user_model(); "
        "User.objects.filter(email='admin@investafrik.com').exists() or "
        "User.objects.create_superuser('admin', 'admin@investafrik.com', 'admin123', "
        "first_name='Admin', last_name='InvestAfrik', user_type='porteur', country='CM')\""
    )
    
    if run_command(create_superuser_cmd, "Création superutilisateur"):
        print("   📧 Email: admin@investafrik.com")
        print("   🔑 Mot de passe: admin123")
    
    return True

def verify_installation():
    """Vérifie que l'installation est correcte"""
    print("\n🔍 Vérification de l'installation...")
    
    # Test de l'importation Django
    try:
        import django
        django.setup()
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user_count = User.objects.count()
        print(f"✅ Django fonctionne - {user_count} utilisateurs en base")
        
        from apps.categories.models import Category
        cat_count = Category.objects.count()
        print(f"✅ Modèles OK - {cat_count} catégories en base")
        
        from apps.projects.models import Project
        project_count = Project.objects.count()
        print(f"✅ Projets OK - {project_count} projets en base")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur de vérification: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 DÉPLOIEMENT COMPLET D'INVESTAFRIK")
    print("=" * 60)
    
    # Vérifier qu'on est dans le bon répertoire
    if not Path('manage.py').exists():
        print("❌ Erreur: manage.py non trouvé")
        print("   Exécutez ce script depuis le répertoire investafrik/")
        sys.exit(1)
    
    steps = [
        ("Configuration environnement", setup_environment),
        ("Configuration PostgreSQL", setup_postgres),
        ("Installation dépendances", install_dependencies),
        ("Configuration Django", setup_django),
        ("Chargement données", load_data),
        ("Vérification installation", verify_installation),
    ]
    
    failed_steps = []
    
    for step_name, step_func in steps:
        print(f"\n{'='*20} {step_name} {'='*20}")
        if not step_func():
            failed_steps.append(step_name)
            print(f"❌ Échec: {step_name}")
        else:
            print(f"✅ Succès: {step_name}")
    
    print("\n" + "=" * 60)
    
    if failed_steps:
        print("⚠️  DÉPLOIEMENT PARTIEL")
        print("Étapes échouées:")
        for step in failed_steps:
            print(f"   - {step}")
        print("\nVous pouvez continuer manuellement ou corriger les erreurs.")
    else:
        print("🎉 DÉPLOIEMENT RÉUSSI !")
    
    print("\n📋 PROCHAINES ÉTAPES:")
    print("   1. Démarrer le serveur: python manage.py runserver")
    print("   2. Ouvrir: http://localhost:8000")
    print("   3. Admin: http://localhost:8000/admin")
    print("   4. API: http://localhost:8000/api")
    
    print("\n🔑 CONNEXION ADMIN:")
    print("   Email: admin@investafrik.com")
    print("   Mot de passe: admin123")
    
    print("\n📚 DOCUMENTATION:")
    print("   - README.md")
    print("   - docs/API_DOCUMENTATION.md")
    print("   - docs/USER_GUIDE.md")

if __name__ == '__main__':
    main()