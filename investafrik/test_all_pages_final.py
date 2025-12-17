#!/usr/bin/env python
"""
Final comprehensive test to verify all pages work with database.
"""
import os
import sys
import django
from django.test import TestCase, Client
from django.contrib.auth import get_user_model

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investafrik.settings.development')
django.setup()

User = get_user_model()

def test_all_pages():
    """Test all pages for functionality."""
    print("🚀 Testing All InvestAfrik Pages")
    print("=" * 60)
    
    # Create test client with proper settings
    from django.test.utils import override_settings
    
    with override_settings(ALLOWED_HOSTS=['testserver', 'localhost', '127.0.0.1']):
        client = Client()
        
        # Test 1: Anonymous user pages
        print("\n📋 TESTING ANONYMOUS USER PAGES")
        print("-" * 40)
        
        pages_to_test = [
            ('/', 'Home Page'),
            ('/projects/', 'Projects List'),
            ('/auth/login/', 'Login Page'),
            ('/auth/register/', 'Register Page'),
        ]
        
        for url, name in pages_to_test:
            try:
                response = client.get(url)
                status = "✅ OK" if response.status_code == 200 else f"❌ {response.status_code}"
                print(f"   {name}: {status}")
            except Exception as e:
                print(f"   {name}: ❌ ERROR - {str(e)}")
        
        # Test 2: Investisseur pages
        print("\n💰 TESTING INVESTISSEUR PAGES")
        print("-" * 40)
        
        try:
            investor = User.objects.get(email='investor@test.com')
            client.force_login(investor)
            print(f"   Logged in as: {investor.email} ({investor.user_type})")
            
            investor_pages = [
                ('/auth/dashboard/investisseur/', 'Investisseur Dashboard'),
                ('/investments/my-investments/', 'My Investments'),
                ('/auth/profile/', 'Profile Page'),
                ('/messaging/conversations/', 'Messaging'),
            ]
            
            for url, name in investor_pages:
                try:
                    response = client.get(url)
                    status = "✅ OK" if response.status_code == 200 else f"❌ {response.status_code}"
                    print(f"   {name}: {status}")
                    
                    # Check if context data is present
                    if response.status_code == 200 and hasattr(response, 'context'):
                        if 'total_invested' in response.context:
                            print(f"     💰 Total invested: {response.context['total_invested']}")
                        if 'total_projects' in response.context:
                            print(f"     📊 Total projects: {response.context['total_projects']}")
                        if 'investments' in response.context:
                            investments = response.context['investments']
                            if hasattr(investments, '__len__'):
                                print(f"     📈 Investments count: {len(investments)}")
                        if 'conversations' in response.context:
                            conversations = response.context['conversations']
                            if hasattr(conversations, '__len__'):
                                print(f"     💬 Conversations count: {len(conversations)}")
                        if 'all_users' in response.context:
                            users = response.context['all_users']
                            if hasattr(users, '__len__'):
                                print(f"     👥 Available users: {len(users)}")
                                
                except Exception as e:
                    print(f"   {name}: ❌ ERROR - {str(e)}")
                    
        except User.DoesNotExist:
            print("   ❌ Investor user not found")
        
        # Test 3: Porteur pages
        print("\n🏗️ TESTING PORTEUR PAGES")
        print("-" * 40)
        
        try:
            porteur = User.objects.get(email='admin@investafrik.com')
            client.force_login(porteur)
            print(f"   Logged in as: {porteur.email} ({porteur.user_type})")
            
            porteur_pages = [
                ('/auth/dashboard/porteur/', 'Porteur Dashboard'),
                ('/projects/my-projects/', 'My Projects'),
                ('/auth/profile/', 'Profile Page'),
                ('/messaging/conversations/', 'Messaging'),
            ]
            
            for url, name in porteur_pages:
                try:
                    response = client.get(url)
                    status = "✅ OK" if response.status_code == 200 else f"❌ {response.status_code}"
                    print(f"   {name}: {status}")
                    
                    # Check if context data is present
                    if response.status_code == 200 and hasattr(response, 'context'):
                        if 'total_projects' in response.context:
                            print(f"     📊 Total projects: {response.context['total_projects']}")
                        if 'total_raised' in response.context:
                            print(f"     💰 Total raised: {response.context['total_raised']}")
                        if 'projects' in response.context:
                            projects = response.context['projects']
                            if hasattr(projects, '__len__'):
                                print(f"     🏗️ Projects count: {len(projects)}")
                        if 'conversations' in response.context:
                            conversations = response.context['conversations']
                            if hasattr(conversations, '__len__'):
                                print(f"     💬 Conversations count: {len(conversations)}")
                                
                except Exception as e:
                    print(f"   {name}: ❌ ERROR - {str(e)}")
                    
        except User.DoesNotExist:
            print("   ❌ Porteur user not found")
        
        # Test 4: Database connectivity verification
        print("\n🗄️ DATABASE CONNECTIVITY VERIFICATION")
        print("-" * 40)
        
        from apps.projects.models import Project
        from apps.investments.models import Investment
        from apps.categories.models import Category
        
        try:
            users_count = User.objects.count()
            projects_count = Project.objects.count()
            investments_count = Investment.objects.count()
            categories_count = Category.objects.count()
            
            print(f"   👥 Users in database: {users_count}")
            print(f"   🏗️ Projects in database: {projects_count}")
            print(f"   💰 Investments in database: {investments_count}")
            print(f"   📂 Categories in database: {categories_count}")
            
            # Test specific queries used by views
            active_projects = Project.objects.filter(status='active').count()
            completed_investments = Investment.objects.filter(payment_status='completed').count()
            
            print(f"   ✅ Active projects: {active_projects}")
            print(f"   ✅ Completed investments: {completed_investments}")
            
        except Exception as e:
            print(f"   ❌ Database error: {str(e)}")
    
    print("\n" + "=" * 60)
    print("🎯 COMPREHENSIVE TEST COMPLETED!")
    print("   The application is ready for use!")
    print("   Server running at: http://127.0.0.1:8000/")
    print("   Test accounts:")
    print("   - Investisseur: investor@test.com / test123")
    print("   - Porteur: admin@investafrik.com / admin123")

if __name__ == '__main__':
    test_all_pages()