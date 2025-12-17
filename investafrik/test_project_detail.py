#!/usr/bin/env python
"""
Test script to verify project detail page functionality.
"""

import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investafrik.settings.development')
django.setup()

from apps.projects.models import Project
from apps.accounts.models import User
from apps.categories.models import Category

def test_project_detail():
    """Test project detail functionality."""
    
    print("🔍 Testing project detail page...")
    
    # Check if we have projects
    projects = Project.objects.all()
    if not projects.exists():
        print("❌ No projects found in database")
        return False
    
    print(f"✅ Found {projects.count()} projects in database")
    
    # Test each project
    for project in projects[:3]:  # Test first 3 projects
        print(f"\n📋 Testing project: {project.title}")
        print(f"   - Slug: {project.slug}")
        print(f"   - Owner: {project.owner.get_full_name()}")
        print(f"   - Category: {project.category.name if project.category else 'None'}")
        print(f"   - Status: {project.status}")
        print(f"   - Goal: {project.goal_amount} FCFA")
        print(f"   - Current: {project.current_amount} FCFA")
        print(f"   - Progress: {project.funding_percentage:.1f}%")
        print(f"   - Days remaining: {project.days_remaining}")
        print(f"   - Investor count: {project.investor_count}")
        
        # Check if project has description
        if project.full_description:
            print(f"   - Description: ✅ ({len(project.full_description)} chars)")
        else:
            print(f"   - Description: ❌ Empty")
        
        # Check if project has featured image
        if project.featured_image:
            print(f"   - Featured image: ✅")
        else:
            print(f"   - Featured image: ❌ None")
        
        # Check budget breakdown
        if project.budget_breakdown:
            print(f"   - Budget breakdown: ✅ ({len(project.budget_breakdown)} items)")
        else:
            print(f"   - Budget breakdown: ❌ Empty")
    
    print(f"\n🎉 Project detail test completed!")
    return True

def check_urls():
    """Check if URLs are working."""
    print("\n🔗 Checking URL configuration...")
    
    from django.urls import reverse
    from django.test import Client
    
    client = Client()
    
    # Test projects list URL
    try:
        url = reverse('projects:list')
        print(f"✅ Projects list URL: {url}")
    except Exception as e:
        print(f"❌ Projects list URL error: {e}")
        return False
    
    # Test project detail URL
    project = Project.objects.first()
    if project:
        try:
            url = reverse('projects:detail', kwargs={'slug': project.slug})
            print(f"✅ Project detail URL: {url}")
            
            # Test the actual view
            response = client.get(url)
            if response.status_code == 200:
                print(f"✅ Project detail view works (status: {response.status_code})")
            else:
                print(f"❌ Project detail view error (status: {response.status_code})")
                return False
                
        except Exception as e:
            print(f"❌ Project detail URL error: {e}")
            return False
    
    return True

if __name__ == '__main__':
    print("🚀 Starting project detail tests...\n")
    
    success = True
    success &= test_project_detail()
    success &= check_urls()
    
    if success:
        print("\n✅ All tests passed! Project detail page should work correctly.")
    else:
        print("\n❌ Some tests failed. Please check the issues above.")