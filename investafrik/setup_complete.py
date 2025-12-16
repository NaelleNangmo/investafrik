#!/usr/bin/env python
"""
Script de configuration complète pour InvestAfrik
Ce script configure automatiquement la base de données PostgreSQL,
crée les migrations, charge les données de test et configure l'environnement.
"""

import os
import sys
import subprocess
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from pathlib import Path

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investafrik.settings.development')

def run_command(command, description):
    """Exécute une commande et affiche le résultat"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Succès")
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Erreur")
        print(f"   Error: {e.stderr}")
        return False

def create_database():
    """Crée la base de données PostgreSQL si elle n'existe pas"""
    print("\n🗄️  Configuration de la base de données PostgreSQL...")
    
    try:
        # Connexion à PostgreSQL
        conn = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='noutong1',
            port='5432'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Vérifier si la base existe
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'invest_afbd'")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute('CREATE DATABASE invest_afbd')
            print("✅ Base de données 'invest_afbd' créée avec succès")
        else:
            print("✅ Base de données 'invest_afbd' existe déjà")
            
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création de la base de données: {e}")
        print("   Assurez-vous que PostgreSQL est installé et démarré")
        print("   Et que l'utilisateur 'postgres' avec le mot de passe 'noutong1' existe")
        return False

def setup_environment():
    """Configure le fichier .env"""
    print("\n⚙️  Configuration de l'environnement...")
    
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if not env_file.exists() and env_example.exists():
        # Copier .env.example vers .env
        with open(env_example, 'r') as f:
            content = f.read()
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("✅ Fichier .env créé à partir de .env.example")
    else:
        print("✅ Fichier .env existe déjà")
    
    return True

def main():
    """Fonction principale de setup"""
    print("🚀 Configuration complète d'InvestAfrik")
    print("=" * 50)
    
    # Vérifier que nous sommes dans le bon répertoire
    if not Path('manage.py').exists():
        print("❌ Erreur: manage.py non trouvé. Exécutez ce script depuis le répertoire investafrik/")
        sys.exit(1)
    
    # 1. Configuration de l'environnement
    if not setup_environment():
        sys.exit(1)
    
    # 2. Création de la base de données
    if not create_database():
        print("\n⚠️  Continuons sans créer la base (elle existe peut-être déjà)")
    
    # 3. Installation des dépendances Python
    if not run_command("pip install -r requirements.txt", "Installation des dépendances Python"):
        sys.exit(1)
    
    # 4. Installation des dépendances Node.js
    if not run_command("npm install", "Installation des dépendances Node.js"):
        print("⚠️  Erreur npm - continuons (peut-être que Node.js n'est pas installé)")
    
    # 5. Compilation de Tailwind CSS
    if not run_command("npm run build", "Compilation de Tailwind CSS"):
        print("⚠️  Erreur compilation CSS - continuons")
    
    # 6. Création des migrations
    if not run_command("python manage.py makemigrations", "Création des migrations"):
        print("⚠️  Erreur migrations - continuons")
    
    # 7. Application des migrations
    if not run_command("python manage.py migrate", "Application des migrations"):
        sys.exit(1)
    
    # 8. Collecte des fichiers statiques
    if not run_command("python manage.py collectstatic --noinput", "Collecte des fichiers statiques"):
        print("⚠️  Erreur collectstatic - continuons")
    
    # 9. Chargement des données de test
    if not run_command("python manage.py seed_data", "Chargement des données de test"):
        print("⚠️  Erreur seed_data - la commande n'existe peut-être pas encore")
    
    # 10. Création du superutilisateur
    print("\n👤 Création du superutilisateur...")
    create_superuser_cmd = (
        "python manage.py shell -c \""
        "from django.contrib.auth import get_user_model; "
        "User = get_user_model(); "
        "User.objects.filter(email='admin@investafrik.com').exists() or "
        "User.objects.create_superuser('admin', 'admin@investafrik.com', 'admin123', "
        "first_name='Admin', last_name='InvestAfrik')\""
    )
    
    if run_command(create_superuser_cmd, "Création du superutilisateur"):
        print("   Email: admin@investafrik.com")
        print("   Mot de passe: admin123")
    
    print("\n" + "=" * 50)
    print("🎉 Configuration terminée !")
    print("\n📋 Prochaines étapes:")
    print("   1. Démarrer le serveur: python manage.py runserver")
    print("   2. Accéder à l'app: http://localhost:8000")
    print("   3. Admin Django: http://localhost:8000/admin")
    print("   4. API: http://localhost:8000/api")
    print("\n🔑 Connexion admin:")
    print("   Email: admin@investafrik.com")
    print("   Mot de passe: admin123")

if __name__ == '__main__':
    main()