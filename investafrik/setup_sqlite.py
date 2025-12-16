#!/usr/bin/env python
"""
Script de setup rapide avec SQLite pour InvestAfrik
Idéal pour le développement et les tests
"""

import os
import sys
import subprocess
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

def setup_sqlite_settings():
    """Configure Django pour utiliser SQLite"""
    print("\n🗄️  Configuration SQLite...")
    
    # Créer un fichier de settings pour SQLite
    sqlite_settings = """
# SQLite settings for development
from .base import *

# Override database to use SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Disable channels for SQLite (use in-memory)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

print("Utilisation de SQLite pour le développement")
"""
    
    settings_file = Path('investafrik/settings/sqlite.py')
    with open(settings_file, 'w', encoding='utf-8') as f:
        f.write(sqlite_settings)
    
    print("✅ Configuration SQLite créée")
    return True

def main():
    """Fonction principale"""
    print("🚀 SETUP RAPIDE INVESTAFRIK (SQLite)")
    print("=" * 50)
    
    # Vérifier qu'on est dans le bon répertoire
    if not Path('manage.py').exists():
        print("❌ Erreur: manage.py non trouvé")
        print("   Exécutez ce script depuis le répertoire investafrik/")
        sys.exit(1)
    
    # 1. Configuration SQLite
    setup_sqlite_settings()
    
    # 2. Définir l'environnement SQLite
    os.environ['DJANGO_SETTINGS_MODULE'] = 'investafrik.settings.sqlite'
    
    # 3. Migrations
    if not run_command("python manage.py makemigrations", "Création des migrations", ignore_errors=True):
        print("   Continuons...")
    
    if not run_command("python manage.py migrate", "Application des migrations"):
        print("❌ Erreur lors des migrations")
        return False
    
    # 4. Collecte des fichiers statiques
    run_command("python manage.py collectstatic --noinput", "Collecte fichiers statiques", ignore_errors=True)
    
    # 5. Installation Node.js (optionnel)
    if Path('package.json').exists():
        run_command("npm install", "Installation dépendances Node.js", ignore_errors=True)
        run_command("npm run build", "Compilation Tailwind CSS", ignore_errors=True)
    
    # 6. Chargement des données de test
    if not run_command("python manage.py seed_data", "Chargement données de test"):
        print("   Continuons sans données de test...")
    
    # 7. Création du superutilisateur
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
    
    # 8. Test rapide
    print("\n🧪 Test rapide...")
    try:
        import django
        django.setup()
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user_count = User.objects.count()
        print(f"✅ Django fonctionne - {user_count} utilisateurs en base")
    except Exception as e:
        print(f"❌ Erreur de test: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 SETUP TERMINÉ AVEC SUCCÈS !")
    
    print("\n📋 PROCHAINES ÉTAPES:")
    print("   1. Démarrer le serveur:")
    print("      python manage.py runserver --settings=investafrik.settings.sqlite")
    print("   2. Ouvrir: http://localhost:8000")
    print("   3. Admin: http://localhost:8000/admin")
    print("   4. API: http://localhost:8000/api")
    
    print("\n🔑 CONNEXION ADMIN:")
    print("   Email: admin@investafrik.com")
    print("   Mot de passe: admin123")
    
    print("\n📝 NOTES:")
    print("   - Utilise SQLite pour le développement")
    print("   - Pour PostgreSQL, utilisez deploy_complete.py")
    print("   - Base de données: db.sqlite3")

if __name__ == '__main__':
    main()