#!/usr/bin/env python
"""
Test API endpoints to ensure they're working correctly.
"""
import os
import sys
import django
from django.test import Client
from django.contrib.auth import get_user_model

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investafrik.settings.development')
django.setup()

User = get_user_model()

def test_api_endpoints():
    """Test API endpoints."""
    print("🔌 Testing API Endpoints")
    print("=" * 50)
    
    from django.test.utils import override_settings
    
    with override_settings(ALLOWED_HOSTS=['testserver', 'localhost', '127.0.0.1']):
        client = Client()
        
        # Test 1: Projects API (anonymous)
        print("\n1. Testing Projects API (Anonymous)...")
        response = client.get('/api/projects/')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Projects API working - Found {len(data.get('results', []))} projects")
        else:
            print(f"   ❌ Projects API failed")
        
        # Test 2: Categories API
        print("\n2. Testing Categories API...")
        response = client.get('/api/categories/')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Categories API working - Found {len(data)} categories")
        else:
            print(f"   ❌ Categories API failed")
        
        # Test 3: Login API
        print("\n3. Testing Login API...")
        login_data = {
            'email': 'investor@test.com',
            'password': 'test123'
        }
        response = client.post('/api/auth/login/', login_data, content_type='application/json')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Login API working - User: {data.get('user', {}).get('email')}")
            access_token = data.get('tokens', {}).get('access')
            
            # Test authenticated endpoints
            if access_token:
                print("\n4. Testing Authenticated Endpoints...")
                headers = {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
                
                # Test investments API
                response = client.get('/api/investments/', **headers)
                print(f"   Investments API Status: {response.status_code}")
                
                # Test messaging API
                response = client.get('/api/messaging/conversations/', **headers)
                print(f"   Messaging API Status: {response.status_code}")
                
        else:
            print(f"   ❌ Login API failed")
    
    print("\n" + "=" * 50)
    print("🎯 API test completed!")

if __name__ == '__main__':
    test_api_endpoints()