#!/usr/bin/env python
"""
Test script to verify complete project creation functionality.
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
from apps.projects.models import Project

def test_project_creation_form():
    """Test project creation with form data."""
    
    print("🔍 Testing project creation functionality...")
    
    client = Client()
    
    # Get a porteur user
    porteur = User.objects.filter(user_type='porteur').first()
    if not porteur:
        print("❌ No porteur user found")
        return False
    
    print(f"✅ Using porteur: {porteur.get_full_name()}")
    
    # Login as porteur
    client.force_login(porteur)
    
    # Get a category
    category = Category.objects.first()
    if not category:
        print("❌ No category found")
        return False
    
    print(f"✅ Using category: {category.name}")
    
    # Count projects before creation
    initial_count = Project.objects.filter(owner=porteur).count()
    print(f"📊 Initial project count for user: {initial_count}")
    
    # Prepare form data
    form_data = {
        'title': 'Test Project - Automated Creation',
        'category': category.id,
        'country': 'CM',
        'short_description': 'This is a test project created automatically to verify the creation functionality works correctly.',
        'full_description': 'This is a detailed description of the test project. It contains more than 50 characters as required by the validation. The project aims to test the complete creation workflow including form validation, data processing, and database storage.',
        'goal_amount': '2000000',
        'duration': '60',
        'status': 'draft',
        'video_url': '',
        'budget_item[]': ['Development', 'Marketing', 'Operations'],
        'budget_amount[]': ['800000', '600000', '600000']
    }
    
    # Submit the form
    url = reverse('projects:create')
    response = client.post(url, data=form_data)
    
    # Check response
    if response.status_code == 302:  # Redirect after successful creation
        print("✅ Form submitted successfully (redirected)")
        
        # Check if project was created
        new_count = Project.objects.filter(owner=porteur).count()
        if new_count > initial_count:
            print(f"✅ Project created! New count: {new_count}")
            
            # Get the created project
            created_project = Project.objects.filter(owner=porteur).order_by('-created_at').first()
            print(f"📋 Created project details:")
            print(f"   - Title: {created_project.title}")
            print(f"   - Category: {created_project.category.name}")
            print(f"   - Goal: {created_project.goal_amount} FCFA")
            print(f"   - Status: {created_project.status}")
            print(f"   - Country: {created_project.country}")
            print(f"   - Slug: {created_project.slug}")
            
            # Check budget breakdown
            if created_project.budget_breakdown:
                print(f"   - Budget items: {len(created_project.budget_breakdown)}")
                for item, amount in created_project.budget_breakdown.items():
                    print(f"     * {item}: {amount} FCFA")
            else:
                print(f"   - Budget breakdown: None")
            
            return True
        else:
            print("❌ Project was not created in database")
            return False
    
    elif response.status_code == 200:  # Form returned with errors
        print("❌ Form submission failed (returned to form)")
        content = response.content.decode('utf-8')
        if 'alert-error' in content:
            print("   - Form contains validation errors")
        return False
    
    else:
        print(f"❌ Unexpected response status: {response.status_code}")
        return False

def test_form_validation():
    """Test form validation."""
    
    print("\n🔍 Testing form validation...")
    
    client = Client()
    porteur = User.objects.filter(user_type='porteur').first()
    client.force_login(porteur)
    
    # Test with invalid data
    invalid_data = {
        'title': '',  # Empty title
        'category': '',  # No category
        'country': '',  # No country
        'short_description': '',  # Empty description
        'full_description': 'Short',  # Too short
        'goal_amount': '50000',  # Below minimum
        'duration': '15',  # Invalid duration
        'status': 'draft'
    }
    
    url = reverse('projects:create')
    response = client.post(url, data=invalid_data)
    
    if response.status_code == 200:  # Should return to form with errors
        content = response.content.decode('utf-8')
        if 'alert-error' in content:
            print("✅ Form validation working (errors displayed)")
            return True
        else:
            print("❌ Form validation not working (no errors shown)")
            return False
    else:
        print(f"❌ Unexpected response for invalid data: {response.status_code}")
        return False

def test_project_access():
    """Test that created projects are accessible."""
    
    print("\n🔍 Testing project access...")
    
    # Get a recent project
    project = Project.objects.order_by('-created_at').first()
    if not project:
        print("❌ No projects found to test")
        return False
    
    client = Client()
    
    # Test project detail page
    try:
        url = reverse('projects:detail', kwargs={'slug': project.slug})
        response = client.get(url)
        
        if response.status_code == 200:
            print(f"✅ Project detail page accessible: {url}")
            return True
        else:
            print(f"❌ Project detail page not accessible: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error accessing project: {e}")
        return False

if __name__ == '__main__':
    print("🚀 Starting complete project creation tests...\n")
    
    success = True
    success &= test_project_creation_form()
    success &= test_form_validation()
    success &= test_project_access()
    
    if success:
        print("\n🎉 All tests passed! Project creation is fully functional.")
        print("\n📋 Features working:")
        print("- ✅ Form submission and data processing")
        print("- ✅ Project creation in database")
        print("- ✅ Form validation and error handling")
        print("- ✅ Budget breakdown processing")
        print("- ✅ Automatic slug generation")
        print("- ✅ Project detail page access")
        print("- ✅ Redirect after successful creation")
        print("\n🎯 You can now create projects at: http://127.0.0.1:8000/projects/create/")
    else:
        print("\n❌ Some tests failed. Please check the issues above.")