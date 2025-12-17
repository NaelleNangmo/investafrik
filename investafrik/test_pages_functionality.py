#!/usr/bin/env python
"""
Test script to verify all pages are working with database connectivity.
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

def test_pages():
    """Test all main pages for database connectivity."""
    client = Client()
    
    print("🔍 Testing InvestAfrik Pages Database Connectivity")
    print("=" * 60)
    
    # Test 1: Home page (anonymous)
    print("\n1. Testing Home Page (Anonymous)...")
    response = client.get('/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print("   ✅ Home page loads successfully")
    else:
        print("   ❌ Home page failed to load")
    
    # Test 2: Projects page (anonymous)
    print("\n2. Testing Projects Page (Anonymous)...")
    response = client.get('/projects/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print("   ✅ Projects page loads successfully")
        # Check if projects are loaded from database
        if 'projects' in response.context:
            projects_count = len(response.context['projects'])
            print(f"   📊 Found {projects_count} projects in database")
        else:
            print("   ⚠️  No projects context found")
    else:
        print("   ❌ Projects page failed to load")
    
    # Test 3: Login as investisseur
    print("\n3. Testing Login as Investisseur...")
    try:
        user = User.objects.get(email='investor@test.com')
        client.force_login(user)
        print("   ✅ Successfully logged in as investisseur")
        
        # Test dashboard
        print("   Testing Investisseur Dashboard...")
        response = client.get('/auth/dashboard/investisseur/')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Dashboard loads successfully")
            if hasattr(response, 'context') and response.context:
                stats = response.context
                print(f"   📊 Total invested: {stats.get('total_invested', 'N/A')}")
                print(f"   📊 Total projects: {stats.get('total_projects', 'N/A')}")
        else:
            print("   ❌ Dashboard failed to load")
        
        # Test my investments page
        print("   Testing My Investments Page...")
        response = client.get('/investments/my-investments/')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ My Investments page loads successfully")
        else:
            print("   ❌ My Investments page failed to load")
        
        # Test profile page
        print("   Testing Profile Page...")
        response = client.get('/auth/profile/')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Profile page loads successfully")
        else:
            print("   ❌ Profile page failed to load")
        
        # Test messaging page
        print("   Testing Messaging Page...")
        response = client.get('/messaging/conversations/')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Messaging page loads successfully")
        else:
            print("   ❌ Messaging page failed to load")
        
    except User.DoesNotExist:
        print("   ❌ Investisseur test user not found")
    
    # Test 4: Login as porteur
    print("\n4. Testing Login as Porteur...")
    try:
        user = User.objects.get(email='admin@investafrik.com')
        client.force_login(user)
        print("   ✅ Successfully logged in as porteur")
        
        # Test dashboard
        print("   Testing Porteur Dashboard...")
        response = client.get('/auth/dashboard/porteur/')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Dashboard loads successfully")
            if hasattr(response, 'context') and response.context:
                stats = response.context
                print(f"   📊 Total projects: {stats.get('total_projects', 'N/A')}")
                print(f"   📊 Total raised: {stats.get('total_raised', 'N/A')}")
        else:
            print("   ❌ Dashboard failed to load")
        
        # Test my projects page
        print("   Testing My Projects Page...")
        response = client.get('/projects/my-projects/')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ My Projects page loads successfully")
        else:
            print("   ❌ My Projects page failed to load")
        
    except User.DoesNotExist:
        print("   ❌ Porteur test user not found")
    
    print("\n" + "=" * 60)
    print("🎯 Test completed!")

if __name__ == '__main__':
    test_pages()