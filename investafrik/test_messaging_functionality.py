#!/usr/bin/env python
"""
Test script pour vérifier la fonctionnalité de messagerie.
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

def test_messaging():
    """Test de la fonctionnalité de messagerie."""
    print("💬 Testing Messaging Functionality")
    print("=" * 50)
    
    from django.test.utils import override_settings
    
    with override_settings(ALLOWED_HOSTS=['testserver', 'localhost', '127.0.0.1']):
        client = Client()
        
        # Test 1: Page des conversations (investisseur)
        print("\n1. Testing Conversations Page (Investisseur)...")
        try:
            investor = User.objects.get(email='investor@test.com')
            client.force_login(investor)
            
            response = client.get('/messaging/conversations/')
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print("   ✅ Conversations page loads successfully")
                if 'conversations' in response.context:
                    conversations = response.context['conversations']
                    print(f"   📊 Conversations count: {len(conversations)}")
                if 'all_users' in response.context:
                    users = response.context['all_users']
                    print(f"   👥 Available users: {len(users)}")
            else:
                print("   ❌ Conversations page failed to load")
                
        except User.DoesNotExist:
            print("   ❌ Investor user not found")
        
        # Test 2: Créer une nouvelle conversation
        print("\n2. Testing New Conversation Creation...")
        try:
            porteur = User.objects.get(email='admin@investafrik.com')
            
            # Créer une conversation entre investisseur et porteur
            response = client.post('/messaging/new/', {
                'participant_2': porteur.id
            })
            print(f"   Status: {response.status_code}")
            if response.status_code == 302:  # Redirect après création
                print("   ✅ Conversation created successfully")
                print(f"   🔄 Redirected to: {response.url}")
            else:
                print("   ❌ Failed to create conversation")
                
        except User.DoesNotExist:
            print("   ❌ Porteur user not found")
        
        # Test 3: Vérifier les conversations après création
        print("\n3. Testing Conversations After Creation...")
        response = client.get('/messaging/conversations/')
        if response.status_code == 200 and 'conversations' in response.context:
            conversations = response.context['conversations']
            print(f"   📊 Conversations after creation: {len(conversations)}")
            
            if conversations:
                # Test d'accès à une conversation spécifique
                first_conversation = conversations[0]
                print(f"\n4. Testing Conversation Detail...")
                response = client.get(f'/messaging/conversations/{first_conversation.id}/')
                print(f"   Status: {response.status_code}")
                if response.status_code == 200:
                    print("   ✅ Conversation detail loads successfully")
                    if 'messages' in response.context:
                        messages = response.context['messages']
                        print(f"   💬 Messages count: {len(messages)}")
                else:
                    print("   ❌ Conversation detail failed to load")
                
                # Test d'envoi de message
                print(f"\n5. Testing Message Sending...")
                response = client.post(f'/messaging/conversations/{first_conversation.id}/', {
                    'content': 'Test message from automated test'
                })
                print(f"   Status: {response.status_code}")
                if response.status_code == 302:  # Redirect après envoi
                    print("   ✅ Message sent successfully")
                    
                    # Vérifier que le message a été ajouté
                    response = client.get(f'/messaging/conversations/{first_conversation.id}/')
                    if response.status_code == 200 and 'messages' in response.context:
                        messages = response.context['messages']
                        print(f"   💬 Messages after sending: {len(messages)}")
                        if messages:
                            last_message = messages.last()
                            print(f"   📝 Last message: {last_message.content[:50]}...")
                else:
                    print("   ❌ Failed to send message")
        
        # Test 4: Test avec porteur
        print("\n6. Testing Porteur Messaging...")
        try:
            porteur = User.objects.get(email='admin@investafrik.com')
            client.force_login(porteur)
            
            response = client.get('/messaging/conversations/')
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print("   ✅ Porteur conversations page loads successfully")
                if 'conversations' in response.context:
                    conversations = response.context['conversations']
                    print(f"   📊 Porteur conversations count: {len(conversations)}")
            else:
                print("   ❌ Porteur conversations page failed to load")
                
        except User.DoesNotExist:
            print("   ❌ Porteur user not found")
    
    print("\n" + "=" * 50)
    print("🎯 Messaging functionality test completed!")

if __name__ == '__main__':
    test_messaging()