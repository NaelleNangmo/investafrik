#!/usr/bin/env python
"""
Test script to verify project creation page functionality.
"""

import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investafrik.settings.development')
django.setup()

from django.test import Client
from django.urls import reverse
from apps.categories.models import Category
from apps.accounts.models import User

def test_categories_loading():
    """Test if categories are loaded correctly."""
    
    print("🔍 Testing categories loading...")
    
    # Check if categories exist in database
    categories = Category.objects.all()
    if not categories.exists():
        print("❌ No categories found in database")
        return False
    
    print(f"✅ Found {categories.count()} categories in database:")
    for category in categories:
        print(f"   - {category.name}")
    
    return True

def test_project_create_page():
    """Test project creation page."""
    
    print("\n🔍 Testing project creation page...")
    
    client = Client()
    
    # Create a test porteur user
    try:
        porteur = User.objects.filter(user_type='porteur').first()
        if not porteur:
            print("❌ No porteur user found in database")
            return False
        
        print(f"✅ Found porteur user: {porteur.get_full_name()}")
        
        # Login as porteur
        client.force_login(porteur)
        
        # Test the create URL
        url = reverse('projects:create')
        print(f"✅ Create URL: {url}")
        
        # Make request
        response = client.get(url)
        
        if response.status_code == 200:
            print(f"✅ Page loads successfully (status: {response.status_code})")
            
            # Check if categories are in the response
            content = response.content.decode('utf-8')
            
            categories = Category.objects.all()
            categories_found = 0
            
            for category in categories:
                if category.name in content:
                    categories_found += 1
                    print(f"   ✅ Category '{category.name}' found in page")
                else:
                    print(f"   ❌ Category '{category.name}' NOT found in page")
            
            if categories_found == categories.count():
                print(f"✅ All {categories_found} categories are loaded correctly!")
                return True
            else:
                print(f"❌ Only {categories_found}/{categories.count()} categories found")
                return False
            
        else:
            print(f"❌ Page failed to load (status: {response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ Error testing create page: {e}")
        return False

def test_category_select_html():
    """Test if the category select HTML is correct."""
    
    print("\n🔍 Testing category select HTML structure...")
    
    client = Client()
    
    try:
        porteur = User.objects.filter(user_type='porteur').first()
        if not porteur:
            print("❌ No porteur user found")
            return False
        
        client.force_login(porteur)
        url = reverse('projects:create')
        response = client.get(url)
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            
            # Check for select element
            if 'id="category"' in content:
                print("✅ Category select element found")
            else:
                print("❌ Category select element not found")
                return False
            
            # Check for option elements
            if '<option value="">Sélectionnez une catégorie</option>' in content:
                print("✅ Default option found")
            else:
                print("❌ Default option not found")
                return False
            
            # Check for category options
            categories = Category.objects.all()
            for category in categories:
                option_html = f'<option value="{category.id}">{category.name}</option>'
                if option_html in content:
                    print(f"✅ Option for '{category.name}' found")
                else:
                    print(f"❌ Option for '{category.name}' not found")
                    return False
            
            print("✅ All category options are correctly formatted!")
            return True
        
        return False
        
    except Exception as e:
        print(f"❌ Error testing HTML structure: {e}")
        return False

if __name__ == '__main__':
    print("🚀 Starting project creation tests...\n")
    
    success = True
    success &= test_categories_loading()
    success &= test_project_create_page()
    success &= test_category_select_html()
    
    if success:
        print("\n🎉 All tests passed! Categories are now loading correctly in the project creation form.")
        print("\n📋 What's working:")
        print("- ✅ Categories are loaded from database")
        print("- ✅ Project creation page loads without errors")
        print("- ✅ Category select dropdown is populated")
        print("- ✅ All category options are available for selection")
        print("\n🎯 You can now visit: http://127.0.0.1:8000/projects/create/")
    else:
        print("\n❌ Some tests failed. Please check the issues above.")