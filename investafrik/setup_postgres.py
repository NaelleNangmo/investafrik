#!/usr/bin/env python
"""
Script pour configurer PostgreSQL en production
"""

import os
import sys
import subprocess
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from pathlib import Path

def create_postgres_settings():
    """Crée un fichier de settings pour PostgreSQL"""
    print("🗄️  Configuration PostgreSQL...")
    
    postgres_settings = """
# PostgreSQL settings for production
from .base import *

# Override database to use PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='invest_afbd'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD', default='noutong1'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Redis for Channels in production
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [config('REDIS_URL', default='redis://localhost:6379/0')],
        },
    },
}

# Production cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': config('REDIS_URL', default='redis://localhost:6379/1'),
    }
}

print("🗄️  Utilisation de PostgreSQL pour la production")
"""
    
    settings_file = Path('investafrik/settings/postgres.py')
    with open(settings_file, 'w', encoding='utf-8') as f:
        f.write(postgres_settings)
    
    print("✅ Configuration PostgreSQL créée")
    return True

def setup_postgres_db():
    """Configure la base de données PostgreSQL"""
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
        print("   Solutions:")
        print("   1. Installer PostgreSQL: https://www.postgresql.org/download/")
        print("   2. Démarrer le service PostgreSQL")
        print("   3. Configurer l'utilisateur 'postgres' avec le mot de passe 'noutong1'")
        return False

def run_command(command, description):
    """Exécute une commande"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Succès")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Erreur")
        if e.stderr:
            print(f"   Error: {e.stderr.strip()}")
        return False

def main():
    """Fonction principale"""
    print("🐘 CONFIGURATION POSTGRESQL POUR INVESTAFRIK")
    print("=" * 60)
    
    # Vérifier qu'on est dans le bon répertoire
    if not Path('manage.py').exists():
        print("❌ Erreur: manage.py non trouvé")
        print("   Exécutez ce script depuis le répertoire investafrik/")
        sys.exit(1)
    
    # 1. Créer les settings PostgreSQL
    create_postgres_settings()
    
    # 2. Configurer la base de données
    if not setup_postgres_db():
        print("\n❌ Impossible de configurer PostgreSQL")
        print("   Utilisez SQLite avec: python manage.py runserver")
        sys.exit(1)
    
    # 3. Définir l'environnement PostgreSQL
    os.environ['DJANGO_SETTINGS_MODULE'] = 'investafrik.settings.postgres'
    
    # 4. Migrations
    if not run_command("python manage.py migrate --settings=investafrik.settings.postgres", 
                      "Application des migrations PostgreSQL"):
        sys.exit(1)
    
    # 5. Chargement des données
    run_command("python manage.py seed_data --settings=investafrik.settings.postgres", 
               "Chargement des données de test")
    
    # 6. Superutilisateur
    create_superuser_cmd = (
        "python manage.py shell --settings=investafrik.settings.postgres -c \""
        "from django.contrib.auth import get_user_model; "
        "User = get_user_model(); "
        "User.objects.filter(email='admin@investafrik.com').exists() or "
        "User.objects.create_superuser('admin', 'admin@investafrik.com', 'admin123', "
        "first_name='Admin', last_name='InvestAfrik', user_type='porteur', country='CM')\""
    )
    
    if run_command(create_superuser_cmd, "Création superutilisateur PostgreSQL"):
        print("   📧 Email: admin@investafrik.com")
        print("   🔑 Mot de passe: admin123")
    
    print("\n" + "=" * 60)
    print("🎉 POSTGRESQL CONFIGURÉ AVEC SUCCÈS !")
    
    print("\n📋 POUR UTILISER POSTGRESQL:")
    print("   python manage.py runserver --settings=investafrik.settings.postgres")
    
    print("\n📝 NOTES:")
    print("   - Base de données: invest_afbd")
    print("   - Utilisateur: postgres")
    print("   - Mot de passe: noutong1")
    print("   - Pour revenir à SQLite: python manage.py runserver")

if __name__ == '__main__':
    main()