#!/usr/bin/env python
"""
Script d'initialisation PostgreSQL pour InvestAfrik
"""

import os
import sys
import subprocess
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    """Crée la base de données INVESTAFRIKDB"""
    print("🗄️  Initialisation de la base de données PostgreSQL...")
    
    try:
        # Connexion à PostgreSQL
        conn = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='noutong1',
            port='5432',
            database='postgres'  # Se connecter à la base par défaut
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Vérifier si la base existe
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'INVESTAFRIKDB'")
        exists = cursor.fetchone()
        
        if exists:
            print("✅ Base de données 'INVESTAFRIKDB' existe déjà")
            # Supprimer et recréer pour un fresh start
            cursor.execute("DROP DATABASE IF EXISTS \"INVESTAFRIKDB\"")
            print("🗑️  Ancienne base supprimée")
        
        # Créer la base avec l'encodage UTF-8
        cursor.execute("CREATE DATABASE \"INVESTAFRIKDB\" WITH ENCODING 'UTF8' LC_COLLATE='C' LC_CTYPE='C' TEMPLATE=template0")
        print("✅ Base de données 'INVESTAFRIKDB' créée avec succès")
            
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création de la base de données: {e}")
        return False

def run_command(command, description):
    """Exécute une commande Django"""
    print(f"\n🔄 {description}...")
    try:
        # Définir l'encodage pour éviter les problèmes
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True,
            env=env,
            encoding='utf-8'
        )
        print(f"✅ {description} - Succès")
        if result.stdout.strip():
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Erreur")
        if e.stderr:
            print(f"   Error: {e.stderr.strip()}")
        return False

def main():
    """Fonction principale"""
    print("🐘 INITIALISATION POSTGRESQL POUR INVESTAFRIK")
    print("=" * 60)
    
    # 1. Créer la base de données
    if not create_database():
        print("❌ Impossible de créer la base de données")
        sys.exit(1)
    
    # 2. Migrations
    if not run_command("python manage.py makemigrations", "Création des migrations"):
        print("⚠️  Continuons...")
    
    if not run_command("python manage.py migrate", "Application des migrations"):
        print("❌ Erreur lors des migrations")
        sys.exit(1)
    
    # 3. Chargement des données
    if not run_command("python manage.py seed_data", "Chargement des données de test"):
        print("⚠️  Continuons sans données de test...")
    
    # 4. Superutilisateur
    create_superuser_cmd = (
        "python manage.py shell -c \""
        "from django.contrib.auth import get_user_model; "
        "User = get_user_model(); "
        "User.objects.filter(email='admin@investafrik.com').exists() or "
        "User.objects.create_superuser('admin', 'admin@investafrik.com', 'admin123', "
        "first_name='Admin', last_name='InvestAfrik', user_type='porteur', country='CM')\""
    )
    
    if run_command(create_superuser_cmd, "Création du superutilisateur"):
        print("   📧 Email: admin@investafrik.com")
        print("   🔑 Mot de passe: admin123")
    
    # 5. Collecte des fichiers statiques
    run_command("python manage.py collectstatic --noinput", "Collecte des fichiers statiques")
    
    print("\n" + "=" * 60)
    print("🎉 POSTGRESQL INITIALISÉ AVEC SUCCÈS !")
    
    print("\n📋 PROCHAINES ÉTAPES:")
    print("   1. python manage.py runserver")
    print("   2. Ouvrir: http://127.0.0.1:8000")
    print("   3. Admin: http://127.0.0.1:8000/admin")
    
    print("\n🔑 CONNEXION ADMIN:")
    print("   Email: admin@investafrik.com")
    print("   Mot de passe: admin123")

if __name__ == '__main__':
    main()