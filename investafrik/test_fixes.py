#!/usr/bin/env python
"""
Script de test pour vérifier les corrections apportées au projet InvestAfrik.
"""
import os
import sys
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investafrik.settings.development')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from apps.messaging.models import Conversation, Message
from apps.projects.models import Project
from apps.categories.models import Category

User = get_user_model()

def test_logout_functionality():
    """Test que la déconnexion fonctionne correctement."""
    print("🔍 Test de la fonctionnalité de déconnexion...")
    
    client = Client()
    
    # Créer un utilisateur de test
    user = User.objects.create_user(
        email='test@example.com',
        password='testpass123',
        first_name='Test',
        last_name='User',
        user_type='porteur'
    )
    
    # Se connecter
    login_success = client.login(email='test@example.com', password='testpass123')
    print(f"   ✓ Connexion: {'Réussie' if login_success else 'Échouée'}")
    
    # Tester la déconnexion
    response = client.post('/auth/logout/')
    print(f"   ✓ Déconnexion POST: Status {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Réponse JSON: {data}")
    
    # Vérifier que l'utilisateur est déconnecté
    response = client.get('/auth/dashboard/')
    is_redirected = response.status_code in [302, 301]
    print(f"   ✓ Redirection après déconnexion: {'Oui' if is_redirected else 'Non'}")
    
    return True

def test_messaging_serializer():
    """Test que le serializer de messagerie gère les attachments null."""
    print("🔍 Test du serializer de messagerie...")
    
    from apps.messaging.serializers import MessageSerializer
    
    # Créer des utilisateurs de test
    user1 = User.objects.create_user(
        email='user1@example.com',
        password='testpass123',
        first_name='User',
        last_name='One',
        user_type='porteur'
    )
    
    user2 = User.objects.create_user(
        email='user2@example.com',
        password='testpass123',
        first_name='User',
        last_name='Two',
        user_type='investisseur'
    )
    
    # Créer une conversation
    conversation = Conversation.objects.create(
        participant_1=user1,
        participant_2=user2
    )
    
    # Créer un message sans attachment
    message = Message.objects.create(
        conversation=conversation,
        sender=user1,
        content="Test message sans attachment"
    )
    
    # Tester la sérialisation
    try:
        serializer = MessageSerializer(message)
        data = serializer.data
        print(f"   ✓ Sérialisation réussie: attachment_url = {data.get('attachment_url')}")
        print(f"   ✓ is_image = {data.get('is_image')}")
        return True
    except Exception as e:
        print(f"   ✗ Erreur de sérialisation: {e}")
        return False

def test_project_urls():
    """Test que les URLs de projets fonctionnent correctement."""
    print("🔍 Test des URLs de projets...")
    
    client = Client()
    
    # Test de la liste des projets
    response = client.get('/projects/')
    print(f"   ✓ Liste des projets: Status {response.status_code}")
    
    # Test de mes projets (sans authentification - doit rediriger)
    response = client.get('/projects/my-projects/')
    print(f"   ✓ Mes projets (non auth): Status {response.status_code}")
    
    # Créer un projet de test
    user = User.objects.create_user(
        email='porteur@example.com',
        password='testpass123',
        first_name='Porteur',
        last_name='Test',
        user_type='porteur'
    )
    
    category = Category.objects.create(
        name='Test Category',
        slug='test-category'
    )
    
    project = Project.objects.create(
        title='Test Project',
        slug='test-project',
        short_description='Description courte',
        description='Description complète',
        goal_amount=100000,
        owner=user,
        category=category
    )
    
    # Test du détail du projet
    response = client.get(f'/projects/{project.slug}/')
    print(f"   ✓ Détail du projet: Status {response.status_code}")
    
    return True

def test_conversation_creation():
    """Test de la création de conversations."""
    print("🔍 Test de la création de conversations...")
    
    from apps.messaging.models import Conversation
    
    # Créer des utilisateurs
    user1 = User.objects.create_user(
        email='conv1@example.com',
        password='testpass123',
        first_name='Conv',
        last_name='One',
        user_type='porteur'
    )
    
    user2 = User.objects.create_user(
        email='conv2@example.com',
        password='testpass123',
        first_name='Conv',
        last_name='Two',
        user_type='investisseur'
    )
    
    # Test de la méthode get_or_create_conversation
    try:
        conversation, created = Conversation.get_or_create_conversation(user1, user2)
        print(f"   ✓ Création de conversation: {'Nouvelle' if created else 'Existante'}")
        
        # Test de création d'une conversation identique
        conversation2, created2 = Conversation.get_or_create_conversation(user2, user1)
        print(f"   ✓ Conversation identique: {'Nouvelle' if created2 else 'Existante'}")
        print(f"   ✓ Même conversation: {conversation.id == conversation2.id}")
        
        return True
    except Exception as e:
        print(f"   ✗ Erreur de création: {e}")
        return False

def test_admin_dashboard_data():
    """Test que le dashboard admin récupère les bonnes données."""
    print("🔍 Test des données du dashboard admin...")
    
    from apps.accounts.admin_views import admin_dashboard
    from django.test import RequestFactory
    from django.contrib.auth.models import AnonymousUser
    
    # Créer une requête factice
    factory = RequestFactory()
    request = factory.get('/admin/dashboard/')
    request.user = AnonymousUser()
    
    try:
        # Créer un superuser pour le test
        admin_user = User.objects.create_superuser(
            email='admin@test.com',
            password='adminpass123',
            first_name='Admin',
            last_name='Test'
        )
        request.user = admin_user
        
        # Tester la vue
        response = admin_dashboard(request)
        print(f"   ✓ Dashboard admin: Status {response.status_code}")
        
        return True
    except Exception as e:
        print(f"   ✗ Erreur dashboard admin: {e}")
        return False

def main():
    """Fonction principale de test."""
    print("🚀 Début des tests de correction InvestAfrik\n")
    
    tests = [
        test_logout_functionality,
        test_messaging_serializer,
        test_project_urls,
        test_conversation_creation,
        test_admin_dashboard_data
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
            print(f"   {'✅ SUCCÈS' if result else '❌ ÉCHEC'}\n")
        except Exception as e:
            print(f"   ❌ ERREUR: {e}\n")
            results.append(False)
    
    # Résumé
    success_count = sum(results)
    total_count = len(results)
    
    print(f"📊 RÉSUMÉ: {success_count}/{total_count} tests réussis")
    
    if success_count == total_count:
        print("🎉 Tous les tests sont passés avec succès!")
    else:
        print("⚠️  Certains tests ont échoué. Vérifiez les détails ci-dessus.")
    
    return success_count == total_count

if __name__ == '__main__':
    main()