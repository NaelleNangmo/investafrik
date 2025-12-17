#!/usr/bin/env python
"""
Simple test to verify database connectivity and data.
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investafrik.settings.development')
django.setup()

from django.contrib.auth import get_user_model
from apps.projects.models import Project
from apps.investments.models import Investment
from apps.categories.models import Category

User = get_user_model()

def test_database():
    """Test database connectivity and data."""
    print("🔍 Testing Database Connectivity")
    print("=" * 50)
    
    # Test 1: Users
    print("\n1. Testing Users...")
    users = User.objects.all()
    print(f"   Total users: {users.count()}")
    
    investisseurs = User.objects.filter(user_type='investisseur')
    porteurs = User.objects.filter(user_type='porteur')
    print(f"   Investisseurs: {investisseurs.count()}")
    print(f"   Porteurs: {porteurs.count()}")
    
    # Test 2: Projects
    print("\n2. Testing Projects...")
    projects = Project.objects.all()
    print(f"   Total projects: {projects.count()}")
    
    active_projects = Project.objects.filter(status='active')
    print(f"   Active projects: {active_projects.count()}")
    
    # Test 3: Categories
    print("\n3. Testing Categories...")
    categories = Category.objects.all()
    print(f"   Total categories: {categories.count()}")
    
    # Test 4: Investments
    print("\n4. Testing Investments...")
    investments = Investment.objects.all()
    print(f"   Total investments: {investments.count()}")
    
    completed_investments = Investment.objects.filter(payment_status='completed')
    print(f"   Completed investments: {completed_investments.count()}")
    
    # Test 5: Test specific users
    print("\n5. Testing Specific Users...")
    try:
        admin_user = User.objects.get(email='admin@investafrik.com')
        print(f"   ✅ Admin user found: {admin_user.email} ({admin_user.user_type})")
        
        # Admin's projects
        admin_projects = Project.objects.filter(owner=admin_user)
        print(f"   Admin's projects: {admin_projects.count()}")
        
    except User.DoesNotExist:
        print("   ❌ Admin user not found")
    
    try:
        investor_user = User.objects.get(email='investor@test.com')
        print(f"   ✅ Investor user found: {investor_user.email} ({investor_user.user_type})")
        
        # Investor's investments
        investor_investments = Investment.objects.filter(investor=investor_user)
        print(f"   Investor's investments: {investor_investments.count()}")
        
    except User.DoesNotExist:
        print("   ❌ Investor user not found")
    
    print("\n" + "=" * 50)
    print("🎯 Database test completed!")

if __name__ == '__main__':
    test_database()