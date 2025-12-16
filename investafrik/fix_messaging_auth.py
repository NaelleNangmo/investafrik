#!/usr/bin/env python
"""
Script pour corriger l'authentification dans la messagerie.
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investafrik.settings.development')
django.setup()

from django.contrib.auth import get_user_model
from apps.messaging.models import Conversation, Message

User = get_user_model()

def create_test_conversation():
    """Créer une conversation de test pour vérifier l'API."""
    print("💬 Création d'une conversation de test...")
    
    try:
        # Récupérer deux utilisateurs différents
        users = User.objects.all()[:2]
        
        if len(users) < 2:
            print("❌ Pas assez d'utilisateurs pour créer une conversation")
            return False
        
        user1, user2 = users[0], users[1]
        
        # Créer une conversation
        conversation, created = Conversation.get_or_create_conversation(user1, user2)
        
        if created:
            print(f"✅ Conversation créée entre {user1.email} et {user2.email}")
            
            # Ajouter un message de test
            Message.objects.create(
                conversation=conversation,
                sender=user1,
                content="Message de test pour vérifier l'API"
            )
            
            print("✅ Message de test ajouté")
        else:
            print(f"✅ Conversation existante trouvée entre {user1.email} et {user2.email}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
        return False

def check_messaging_permissions():
    """Vérifier les permissions de l'API messagerie."""
    print("\n🔐 Vérification des permissions...")
    
    from apps.messaging.views import ConversationViewSet
    from rest_framework.permissions import IsAuthenticated
    
    # Vérifier que les permissions sont correctes
    viewset = ConversationViewSet()
    permissions = viewset.permission_classes
    
    if IsAuthenticated in permissions:
        print("✅ Permission IsAuthenticated configurée")
        return True
    else:
        print("❌ Permission IsAuthenticated manquante")
        return False

def main():
    """Fonction principale."""
    print("🔧 Correction de l'authentification messagerie")
    print("=" * 50)
    
    # Tests
    permissions_ok = check_messaging_permissions()
    conversation_ok = create_test_conversation()
    
    if permissions_ok and conversation_ok:
        print("\n🎉 SUCCÈS: L'API de messagerie est correctement configurée")
        print("\n💡 Instructions pour tester:")
        print("   1. Connectez-vous sur le site")
        print("   2. Allez dans Messages")
        print("   3. Cliquez sur 'Nouvelle Conversation'")
        print("   4. Recherchez et sélectionnez un utilisateur")
        print("   5. La conversation devrait se créer sans erreur 403")
        return True
    else:
        print("\n❌ Des problèmes persistent avec l'API de messagerie")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)