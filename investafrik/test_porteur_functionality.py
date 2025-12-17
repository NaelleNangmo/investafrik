#!/usr/bin/env python
"""
Test script pour vérifier toutes les fonctionnalités des porteurs de projet.
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

def test_porteur_functionality():
    """Test complet des fonctionnalités porteur."""
    print("🏗️ Testing Porteur de Projet Functionality")
    print("=" * 60)
    
    from django.test.utils import override_settings
    
    with override_settings(ALLOWED_HOSTS=['testserver', 'localhost', '127.0.0.1']):
        client = Client()
        
        # Login as porteur
        print("\n1. Testing Porteur Login...")
        try:
            porteur = User.objects.get(email='admin@investafrik.com')
            client.force_login(porteur)
            print(f"   ✅ Successfully logged in as: {porteur.email} ({porteur.user_type})")
            
            # Test Dashboard Porteur
            print("\n2. Testing Porteur Dashboard...")
            response = client.get('/auth/dashboard/porteur/')
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print("   ✅ Dashboard loads successfully")
                if hasattr(response, 'context') and response.context:
                    stats = response.context
                    print(f"   📊 Total projects: {stats.get('total_projects', 'N/A')}")
                    print(f"   💰 Total raised: {stats.get('total_raised', 'N/A')}")
                    print(f"   👥 Total investors: {stats.get('total_investors', 'N/A')}")
                    print(f"   🎯 Active projects: {stats.get('active_projects', 'N/A')}")
            else:
                print("   ❌ Dashboard failed to load")
            
            # Test My Projects Page
            print("\n3. Testing My Projects Page...")
            response = client.get('/projects/my-projects/')
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print("   ✅ My Projects page loads successfully")
                if 'projects' in response.context:
                    projects = response.context['projects']
                    print(f"   🏗️ Projects count: {len(projects)}")
                    if projects:
                        first_project = projects[0]
                        print(f"   📝 First project: {first_project.title}")
                        print(f"   💰 Goal amount: {first_project.goal_amount}")
                        print(f"   📊 Status: {first_project.status}")
                if 'total_raised' in response.context:
                    print(f"   💰 Total raised: {response.context['total_raised']}")
            else:
                print("   ❌ My Projects page failed to load")
            
            # Test Profile Page
            print("\n4. Testing Profile Page...")
            response = client.get('/auth/profile/')
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print("   ✅ Profile page loads successfully")
                if 'profile' in response.context:
                    profile = response.context['profile']
                    print(f"   👤 Profile loaded for: {porteur.get_full_name()}")
                    print(f"   📧 Email: {porteur.email}")
                    print(f"   🏢 Company: {getattr(profile, 'company', 'N/A')}")
            else:
                print("   ❌ Profile page failed to load")
            
            # Test Profile Update
            print("\n5. Testing Profile Update...")
            response = client.post('/auth/profile/', {
                'first_name': 'Admin',
                'last_name': 'Updated',
                'phone_number': '+237123456789',
                'bio': 'Test bio for porteur',
                'country': 'CM',
                'company': 'Test Company',
                'job_title': 'CEO',
                'email_notifications': 'on',
            })
            print(f"   Status: {response.status_code}")
            if response.status_code == 302:  # Redirect after successful update
                print("   ✅ Profile updated successfully")
                
                # Verify the update
                updated_user = User.objects.get(id=porteur.id)
                print(f"   📝 Updated name: {updated_user.get_full_name()}")
                print(f"   📱 Updated phone: {updated_user.phone_number}")
            else:
                print("   ❌ Profile update failed")
            
            # Test Messaging for Porteur
            print("\n6. Testing Messaging for Porteur...")
            response = client.get('/messaging/conversations/')
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print("   ✅ Messaging page loads successfully")
                if 'conversations' in response.context:
                    conversations = response.context['conversations']
                    print(f"   💬 Conversations count: {len(conversations)}")
                    
                    if conversations:
                        # Test accessing a specific conversation
                        first_conversation = conversations[0]
                        print(f"\n   Testing Conversation Detail...")
                        response = client.get(f'/messaging/conversations/{first_conversation.id}/')
                        print(f"   Status: {response.status_code}")
                        if response.status_code == 200:
                            print("   ✅ Conversation detail loads successfully")
                            if 'messages' in response.context:
                                messages = response.context['messages']
                                print(f"   💬 Messages in conversation: {len(messages)}")
                        else:
                            print("   ❌ Conversation detail failed to load")
                
                if 'all_users' in response.context:
                    users = response.context['all_users']
                    print(f"   👥 Available users for new conversations: {len(users)}")
            else:
                print("   ❌ Messaging page failed to load")
            
            # Test Creating New Conversation
            print("\n7. Testing New Conversation Creation...")
            try:
                # Find an investor to start conversation with
                investor = User.objects.filter(user_type='investisseur').first()
                if investor:
                    response = client.post('/messaging/new/', {
                        'participant_2': investor.id
                    })
                    print(f"   Status: {response.status_code}")
                    if response.status_code == 302:  # Redirect after creation
                        print(f"   ✅ New conversation created with {investor.get_full_name()}")
                        print(f"   🔄 Redirected to: {response.url}")
                    else:
                        print("   ❌ Failed to create new conversation")
                else:
                    print("   ⚠️ No investor found to create conversation with")
            except Exception as e:
                print(f"   ❌ Error creating conversation: {str(e)}")
            
            # Test Project Creation Access (should be available for porteurs)
            print("\n8. Testing Project Creation Access...")
            response = client.get('/projects/create/')
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print("   ✅ Project creation page accessible")
            else:
                print(f"   ⚠️ Project creation page status: {response.status_code}")
            
        except User.DoesNotExist:
            print("   ❌ Porteur user not found")
        
        # Test with another porteur if available
        print("\n9. Testing with Another Porteur...")
        try:
            other_porteurs = User.objects.filter(user_type='porteur').exclude(email='admin@investafrik.com')
            if other_porteurs.exists():
                other_porteur = other_porteurs.first()
                client.force_login(other_porteur)
                print(f"   ✅ Logged in as: {other_porteur.email}")
                
                # Test dashboard for this porteur
                response = client.get('/auth/dashboard/porteur/')
                if response.status_code == 200:
                    print("   ✅ Dashboard works for other porteur")
                    if 'total_projects' in response.context:
                        print(f"   📊 Projects: {response.context['total_projects']}")
                else:
                    print("   ❌ Dashboard failed for other porteur")
            else:
                print("   ⚠️ No other porteur found for testing")
        except Exception as e:
            print(f"   ❌ Error testing other porteur: {str(e)}")
    
    print("\n" + "=" * 60)
    print("🎯 Porteur functionality test completed!")

if __name__ == '__main__':
    test_porteur_functionality()