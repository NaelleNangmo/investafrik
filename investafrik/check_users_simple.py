#!/usr/bin/env python3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investafrik.settings.development')
django.setup()

from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

print("=== VÉRIFICATION DES UTILISATEURS ===")

# Lister tous les utilisateurs
users = User.objects.all()
print(f"Nombre d'utilisateurs: {users.count()}")

for user in users:
    print(f"- Email: {user.email}")
    print(f"  Username: {user.username}")
    print(f"  Active: {user.is_active}")
    print(f"  Staff: {user.is_staff}")
    print(f"  Type: {user.user_type}")
    print()

# Tester l'authentification
print("=== TEST D'AUTHENTIFICATION ===")
test_user = authenticate(email='admin@investafrik.com', password='admin123')
if test_user:
    print("✅ Authentification réussie!")
else:
    print("❌ Échec de l'authentification")
    
    # Essayer de créer/réinitialiser l'utilisateur admin
    try:
        admin = User.objects.get(email='admin@investafrik.com')
        admin.set_password('admin123')
        admin.is_active = True
        admin.save()
        print("✅ Mot de passe admin réinitialisé")
        
        # Tester à nouveau
        test_user = authenticate(email='admin@investafrik.com', password='admin123')
        if test_user:
            print("✅ Authentification réussie après réinitialisation!")
        else:
            print("❌ Échec persistant")
    except User.DoesNotExist:
        print("❌ Utilisateur admin non trouvé")