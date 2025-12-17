#!/usr/bin/env python3
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investafrik.settings.development')
django.setup()

from django.test import Client
from django.contrib.auth import authenticate

print("=== TEST D'AUTHENTIFICATION API ===")

# Test 1: Authentification directe
print("1. Test d'authentification directe:")
user = authenticate(email='admin@investafrik.com', password='admin123')
if user:
    print(f"✅ Authentification directe réussie: {user.email}")
else:
    print("❌ Échec de l'authentification directe")

# Test 2: API de login
print("\n2. Test de l'API de login:")
client = Client()

login_data = {
    'email': 'admin@investafrik.com',
    'password': 'admin123'
}

response = client.post(
    '/api/auth/login/',
    data=json.dumps(login_data),
    content_type='application/json'
)

print(f"Status code: {response.status_code}")
print(f"Response content: {response.content.decode()}")

if response.status_code == 200:
    print("✅ API de login fonctionne!")
    try:
        data = json.loads(response.content.decode())
        print(f"User ID: {data.get('user', {}).get('id')}")
        print(f"Access token présent: {'tokens' in data and 'access' in data['tokens']}")
    except json.JSONDecodeError:
        print("⚠️ Réponse n'est pas du JSON valide")
else:
    print("❌ Problème avec l'API de login")

# Test 3: Avec des mauvaises credentials
print("\n3. Test avec de mauvaises credentials:")
bad_login_data = {
    'email': 'admin@investafrik.com',
    'password': 'wrongpassword'
}

response = client.post(
    '/api/auth/login/',
    data=json.dumps(bad_login_data),
    content_type='application/json'
)

print(f"Status code: {response.status_code}")
print(f"Response: {response.content.decode()}")

if response.status_code == 401:
    print("✅ Rejet correct des mauvaises credentials")
else:
    print("⚠️ Comportement inattendu pour les mauvaises credentials")

print("\n=== FIN DES TESTS ===")