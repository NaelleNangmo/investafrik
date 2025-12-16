#!/usr/bin/env python
"""
Script pour vérifier et configurer PostgreSQL pour InvestAfrik
"""

import subprocess
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def check_postgres_installed():
    """Vérifie si PostgreSQL est installé"""
    try:
        result = subprocess.run(['psql', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ PostgreSQL installé: {result.stdout.strip()}")
            return True
        else:
            print("❌ PostgreSQL n'est pas installé ou pas dans le PATH")
            return False
    except FileNotFoundError:
        print("❌ PostgreSQL n'est pas installé ou pas dans le PATH")
        return False

def check_postgres_service():
    """Vérifie si le service PostgreSQL est démarré"""
    try:
        # Essayer de se connecter à PostgreSQL
        conn = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='noutong1',
            port='5432'
        )
        conn.close()
        print("✅ Service PostgreSQL démarré et accessible")
        return True
    except Exception as e:
        print(f"❌ Impossible de se connecter à PostgreSQL: {e}")
        print("   Vérifiez que:")
        print("   - Le service PostgreSQL est démarré")
        print("   - L'utilisateur 'postgres' existe avec le mot de passe 'noutong1'")
        print("   - PostgreSQL écoute sur le port 5432")
        return False

def create_database():
    """Crée la base de données si elle n'existe pas"""
    try:
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
            print("✅ Base de données 'invest_afbd' créée")
        else:
            print("✅ Base de données 'invest_afbd' existe déjà")
            
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création de la base: {e}")
        return False

def main():
    print("🔍 Vérification de PostgreSQL pour InvestAfrik")
    print("=" * 50)
    
    # 1. Vérifier l'installation
    if not check_postgres_installed():
        print("\n📥 Installation de PostgreSQL requise:")
        print("   Windows: https://www.postgresql.org/download/windows/")
        print("   Ou via Chocolatey: choco install postgresql")
        sys.exit(1)
    
    # 2. Vérifier le service
    if not check_postgres_service():
        print("\n🔧 Actions requises:")
        print("   1. Démarrer le service PostgreSQL")
        print("   2. Configurer l'utilisateur 'postgres' avec le mot de passe 'noutong1'")
        print("   3. Ou modifier le fichier .env avec vos paramètres")
        sys.exit(1)
    
    # 3. Créer la base de données
    if not create_database():
        sys.exit(1)
    
    print("\n🎉 PostgreSQL est prêt pour InvestAfrik !")
    print("   Vous pouvez maintenant exécuter: python setup_complete.py")

if __name__ == '__main__':
    main()