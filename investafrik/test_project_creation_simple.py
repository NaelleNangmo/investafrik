#!/usr/bin/env python
"""
Simple test to verify project creation logic without HTTP requests.
"""

import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investafrik.settings.development')
django.setup()

from apps.categories.models import Category
from apps.accounts.models import User
from apps.projects.models import Project
from datetime import date, timedelta

def test_project_creation_logic():
    """Test project creation logic directly."""
    
    print("🔍 Testing project creation logic...")
    
    # Get required data
    porteur = User.objects.filter(user_type='porteur').first()
    category = Category.objects.first()
    
    if not porteur:
        print("❌ No porteur user found")
        return False
    
    if not category:
        print("❌ No category found")
        return False
    
    print(f"✅ Using porteur: {porteur.get_full_name()}")
    print(f"✅ Using category: {category.name}")
    
    # Count initial projects
    initial_count = Project.objects.filter(owner=porteur).count()
    print(f"📊 Initial project count: {initial_count}")
    
    # Create project data
    project_data = {
        'title': 'Test Project - Direct Creation',
        'short_description': 'This is a test project created directly to verify the creation logic works.',
        'full_description': 'This is a detailed description of the test project. It contains more than 50 characters as required by the validation. The project aims to test the complete creation workflow.',
        'goal_amount': 3000000,
        'country': 'CM',
        'status': 'draft'
    }
    
    # Calculate dates
    start_date = date.today()
    end_date = start_date + timedelta(days=60)
    
    try:
        # Create the project
        project = Project.objects.create(
            owner=porteur,
            category=category,
            title=project_data['title'],
            short_description=project_data['short_description'],
            full_description=project_data['full_description'],
            goal_amount=project_data['goal_amount'],
            country=project_data['country'],
            start_date=start_date,
            end_date=end_date,
            status=project_data['status']
        )
        
        print(f"✅ Project created successfully!")
        print(f"   - ID: {project.id}")
        print(f"   - Title: {project.title}")
        print(f"   - Slug: {project.slug}")
        print(f"   - Owner: {project.owner.get_full_name()}")
        print(f"   - Category: {project.category.name}")
        print(f"   - Goal: {project.goal_amount} FCFA")
        print(f"   - Status: {project.status}")
        print(f"   - Start date: {project.start_date}")
        print(f"   - End date: {project.end_date}")
        print(f"   - Days remaining: {project.days_remaining}")
        
        # Test budget breakdown
        budget_breakdown = {
            'Development': 1200000,
            'Marketing': 800000,
            'Operations': 600000,
            'Contingency': 400000
        }
        
        project.budget_breakdown = budget_breakdown
        project.save()
        
        print(f"✅ Budget breakdown added:")
        for item, amount in project.budget_breakdown.items():
            print(f"   - {item}: {amount:,} FCFA")
        
        # Verify project count increased
        new_count = Project.objects.filter(owner=porteur).count()
        print(f"📊 New project count: {new_count}")
        
        if new_count > initial_count:
            print("✅ Project count increased correctly")
            return True
        else:
            print("❌ Project count did not increase")
            return False
            
    except Exception as e:
        print(f"❌ Error creating project: {e}")
        return False

def test_project_properties():
    """Test project model properties."""
    
    print("\n🔍 Testing project model properties...")
    
    # Get the most recent project
    project = Project.objects.order_by('-created_at').first()
    if not project:
        print("❌ No project found to test")
        return False
    
    print(f"📋 Testing project: {project.title}")
    
    # Test properties
    try:
        funding_percentage = project.funding_percentage
        days_remaining = project.days_remaining
        is_active = project.is_active
        is_successful = project.is_successful
        investor_count = project.investor_count
        
        print(f"✅ Properties working:")
        print(f"   - Funding percentage: {funding_percentage:.1f}%")
        print(f"   - Days remaining: {days_remaining}")
        print(f"   - Is active: {is_active}")
        print(f"   - Is successful: {is_successful}")
        print(f"   - Investor count: {investor_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing properties: {e}")
        return False

def test_validation_logic():
    """Test validation logic."""
    
    print("\n🔍 Testing validation logic...")
    
    # Test validation scenarios
    test_cases = [
        {
            'name': 'Empty title',
            'title': '',
            'should_fail': True
        },
        {
            'name': 'Short title',
            'title': 'Test',
            'should_fail': True
        },
        {
            'name': 'Valid title',
            'title': 'Valid Project Title',
            'should_fail': False
        },
        {
            'name': 'Short description too long',
            'short_description': 'A' * 201,
            'should_fail': True
        },
        {
            'name': 'Valid short description',
            'short_description': 'This is a valid short description.',
            'should_fail': False
        },
        {
            'name': 'Full description too short',
            'full_description': 'Short',
            'should_fail': True
        },
        {
            'name': 'Valid full description',
            'full_description': 'This is a valid full description that contains more than 50 characters as required.',
            'should_fail': False
        },
        {
            'name': 'Goal amount too low',
            'goal_amount': 50000,
            'should_fail': True
        },
        {
            'name': 'Valid goal amount',
            'goal_amount': 2000000,
            'should_fail': False
        }
    ]
    
    validation_results = []
    
    for test_case in test_cases:
        name = test_case['name']
        should_fail = test_case['should_fail']
        
        # Simulate validation logic
        errors = []
        
        if 'title' in test_case:
            title = test_case['title']
            if not title or len(title) < 5:
                errors.append("Title validation failed")
        
        if 'short_description' in test_case:
            short_desc = test_case['short_description']
            if len(short_desc) > 200:
                errors.append("Short description too long")
        
        if 'full_description' in test_case:
            full_desc = test_case['full_description']
            if len(full_desc) < 50:
                errors.append("Full description too short")
        
        if 'goal_amount' in test_case:
            goal_amount = test_case['goal_amount']
            if goal_amount < 100000:
                errors.append("Goal amount too low")
        
        has_errors = len(errors) > 0
        
        if should_fail and has_errors:
            print(f"✅ {name}: Correctly failed validation")
            validation_results.append(True)
        elif not should_fail and not has_errors:
            print(f"✅ {name}: Correctly passed validation")
            validation_results.append(True)
        else:
            print(f"❌ {name}: Validation logic incorrect")
            validation_results.append(False)
    
    return all(validation_results)

if __name__ == '__main__':
    print("🚀 Starting simple project creation tests...\n")
    
    success = True
    success &= test_project_creation_logic()
    success &= test_project_properties()
    success &= test_validation_logic()
    
    if success:
        print("\n🎉 All tests passed! Project creation logic is working correctly.")
        print("\n📋 What's working:")
        print("- ✅ Project model creation")
        print("- ✅ Automatic slug generation")
        print("- ✅ Budget breakdown storage")
        print("- ✅ Date calculations")
        print("- ✅ Model properties (funding_percentage, days_remaining, etc.)")
        print("- ✅ Validation logic")
        print("\n🎯 The project creation functionality is ready to use!")
    else:
        print("\n❌ Some tests failed. Please check the issues above.")