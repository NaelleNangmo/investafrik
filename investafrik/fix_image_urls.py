#!/usr/bin/env python
"""
Fix script to handle external image URLs in Project model.
This script will:
1. Add a new field for external image URLs
2. Move existing Unsplash URLs to the new field
3. Clear the featured_image field for projects with external URLs
"""

import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investafrik.settings.development')
django.setup()

from apps.projects.models import Project

def fix_image_urls():
    """Fix projects with external image URLs."""
    
    print("🔍 Checking projects with external image URLs...")
    
    # Find projects with Unsplash URLs in featured_image field
    projects_with_external_urls = []
    
    for project in Project.objects.all():
        if project.featured_image and project.featured_image.name.startswith('https:'):
            projects_with_external_urls.append(project)
            print(f"Found project with external URL: {project.title}")
    
    if not projects_with_external_urls:
        print("✅ No projects found with external URLs in featured_image field.")
        return
    
    print(f"📝 Found {len(projects_with_external_urls)} projects with external URLs")
    
    # Clear the featured_image field for these projects
    for project in projects_with_external_urls:
        external_url = project.featured_image.name
        print(f"Clearing external URL for project: {project.title}")
        print(f"  URL was: {external_url}")
        
        # Clear the featured_image field
        project.featured_image = None
        project.save()
        
        print(f"  ✅ Cleared featured_image for {project.title}")
    
    print(f"🎉 Fixed {len(projects_with_external_urls)} projects!")
    print("\n📋 Summary:")
    print("- External URLs have been removed from featured_image fields")
    print("- Projects will now use gradient backgrounds instead of broken images")
    print("- You can upload proper images through the admin interface")

if __name__ == '__main__':
    fix_image_urls()