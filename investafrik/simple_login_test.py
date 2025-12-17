#!/usr/bin/env python3
import os
import django
import requests
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investafrik.settings.development')
django.setup()

print("=== TEST SIMPLE DE L'API LOGIN ===")

# Test avec requests (comme un vrai client)
url = 'http://127.0.0.1:8000/api/auth/login/'
data = {
    'email': 'admin@investafrik.com',
    'password': 'admin123'
}

try:
    response = requests.post(url, json=data, timeout=10)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ LOGIN RÉUSSI!")
        result = response.json()
        print(f"User ID: {result.get('user', {}).get('id')}")
        print(f"Email: {result.get('user', {}).get('email')}")
        print(f"Token présent: {'tokens' in result}")
    else:
        print(f"❌ Échec du login: {response.text}")
        
except requests.exceptions.ConnectionError:
    print("❌ Serveur non accessible. Assurez-vous que le serveur Django tourne sur http://127.0.0.1:8000")
except Exception as e:
    print(f"❌ Erreur: {e}")

print("\n=== INSTRUCTIONS ===")
print("1. Assurez-vous que le serveur Django tourne: python manage.py runserver")
print("2. Testez manuellement sur http://127.0.0.1:8000/auth/login/")
print("3. Utilisez admin@investafrik.com / admin123")