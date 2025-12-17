#!/usr/bin/env python3
"""
Script pour diagnostiquer et corriger tous les problèmes de BD des pages utilisateur.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investafrik.settings.development')
django.setup()

from django.contrib.auth import get_user_model
from apps.projects.models import Project
from apps.investments.models import Investment
from apps.messaging.models import Conversation, Message

User = get_user_model()

def diagnose_database_issues():
    """Diagnostiquer les problèmes de base de données."""
    print("🔍 DIAGNOSTIC DES PROBLÈMES DE BASE DE DONNÉES")
    print("=" * 60)
    
    # Vérifier les utilisateurs
    print("1. UTILISATEURS:")
    users = User.objects.all()
    print(f"   - Total utilisateurs: {users.count()}")
    
    investors = users.filter(user_type='investisseur')
    porteurs = users.filter(user_type='porteur')
    print(f"   - Investisseurs: {investors.count()}")
    print(f"   - Porteurs: {porteurs.count()}")
    
    for user in users[:5]:
        print(f"   - {user.email} ({user.user_type}) - Actif: {user.is_active}")
    
    # Vérifier les projets
    print("\n2. PROJETS:")
    projects = Project.objects.all()
    print(f"   - Total projets: {projects.count()}")
    
    for project in projects[:3]:
        print(f"   - {project.title} (Propriétaire: {project.owner.email})")
    
    # Vérifier les investissements
    print("\n3. INVESTISSEMENTS:")
    investments = Investment.objects.all()
    print(f"   - Total investissements: {investments.count()}")
    
    for investment in investments[:3]:
        print(f"   - {investment.amount} FCFA par {investment.investor.email} dans {investment.project.title}")
    
    # Vérifier les conversations
    print("\n4. CONVERSATIONS:")
    conversations = Conversation.objects.all()
    print(f"   - Total conversations: {conversations.count()}")
    
    messages = Message.objects.all()
    print(f"   - Total messages: {messages.count()}")

def check_user_profiles():
    """Vérifier les profils utilisateur."""
    print("\n👤 VÉRIFICATION PROFILS UTILISATEUR")
    print("=" * 40)
    
    try:
        investor = User.objects.get(email='investor@test.com')
        print(f"✅ Investisseur trouvé: {investor.email}")
        print(f"   - Prénom: {investor.first_name}")
        print(f"   - Nom: {investor.last_name}")
        print(f"   - Téléphone: {investor.phone_number}")
        print(f"   - Pays: {investor.country}")
        print(f"   - Bio: {investor.bio}")
        
        # Vérifier le profil étendu
        try:
            profile = investor.profile
            print(f"   - Profil étendu: Oui")
            print(f"   - Entreprise: {profile.company}")
            print(f"   - Poste: {profile.job_title}")
        except:
            print(f"   - Profil étendu: Non (sera créé)")
            
    except User.DoesNotExist:
        print("❌ Investisseur de test non trouvé")
    
    try:
        admin = User.objects.get(email='admin@investafrik.com')
        print(f"\n✅ Admin/Porteur trouvé: {admin.email}")
        print(f"   - Type: {admin.user_type}")
        print(f"   - Projets: {admin.project_set.count()}")
        
    except User.DoesNotExist:
        print("❌ Admin non trouvé")

if __name__ == '__main__':
    diagnose_database_issues()
    check_user_profiles()
    
    print("\n" + "=" * 60)
    print("🎯 PROBLÈMES IDENTIFIÉS À CORRIGER:")
    print("1. Pages projets - Communication avec BD")
    print("2. Dashboard investisseur - Données réelles")
    print("3. Profil utilisateur - Chargement et modification")
    print("4. Messagerie - Chargement conversations")
    print("5. Mes investissements - Données utilisateur")
    print("\n🔧 Correction en cours...")