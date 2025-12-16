#!/usr/bin/env python
"""
Script de démonstration d'InvestAfrik
Montre toutes les fonctionnalités principales
"""

import os
import sys
from pathlib import Path

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investafrik.settings.development')

def demo_users():
    """Démonstration des utilisateurs"""
    print("👥 UTILISATEURS")
    print("-" * 30)
    
    try:
        import django
        django.setup()
        
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Porteurs de projets
        porteurs = User.objects.filter(user_type='porteur')[:5]
        print("🚀 Porteurs de projets:")
        for user in porteurs:
            print(f"   • {user.get_full_name()} ({user.get_country_display_name()})")
        
        # Investisseurs
        investisseurs = User.objects.filter(user_type='investisseur')[:5]
        print("\n💰 Investisseurs:")
        for user in investisseurs:
            budget = f"{user.available_budget:,.0f} FCFA" if user.available_budget else "N/A"
            print(f"   • {user.get_full_name()} - Budget: {budget}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def demo_categories():
    """Démonstration des catégories"""
    print("\n📂 CATÉGORIES DE PROJETS")
    print("-" * 30)
    
    try:
        from apps.categories.models import Category
        
        categories = Category.objects.all()[:8]
        for cat in categories:
            print(f"   {cat.icon_class} {cat.name}")
            print(f"      {cat.description[:60]}...")
            print(f"      Projets: {cat.project_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def demo_projects():
    """Démonstration des projets"""
    print("\n🚀 PROJETS PHARES")
    print("-" * 30)
    
    try:
        from apps.projects.models import Project
        
        projects = Project.objects.all()[:5]
        for project in projects:
            print(f"\n📊 {project.title}")
            print(f"   Porteur: {project.owner.get_full_name()}")
            print(f"   Catégorie: {project.category.name}")
            print(f"   Pays: {project.get_country_display()}")
            print(f"   Objectif: {project.goal_amount:,.0f} FCFA")
            print(f"   Levé: {project.current_amount:,.0f} FCFA ({project.funding_percentage:.1f}%)")
            print(f"   Jours restants: {project.days_remaining}")
            print(f"   Statut: {project.get_status_display()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def demo_api_endpoints():
    """Démonstration des endpoints API"""
    print("\n🔌 ENDPOINTS API DISPONIBLES")
    print("-" * 30)
    
    endpoints = [
        ("POST /api/auth/register/", "Inscription utilisateur"),
        ("POST /api/auth/login/", "Connexion utilisateur"),
        ("GET /api/auth/profile/", "Profil utilisateur"),
        ("GET /api/categories/", "Liste des catégories"),
        ("GET /api/projects/", "Liste des projets"),
        ("POST /api/projects/", "Créer un projet"),
        ("GET /api/projects/{id}/", "Détail d'un projet"),
        ("POST /api/investments/", "Investir dans un projet"),
        ("GET /api/investments/", "Mes investissements"),
        ("GET /api/messaging/conversations/", "Mes conversations"),
        ("POST /api/messaging/messages/", "Envoyer un message"),
        ("GET /api/notifications/", "Mes notifications"),
    ]
    
    for endpoint, description in endpoints:
        print(f"   {endpoint:<35} {description}")
    
    return True

def demo_features():
    """Démonstration des fonctionnalités"""
    print("\n⚡ FONCTIONNALITÉS PRINCIPALES")
    print("-" * 30)
    
    features = [
        ("🔐 Authentification", "JWT, profils utilisateurs, types d'utilisateurs"),
        ("📊 Gestion de projets", "CRUD complet, catégories, médias, statuts"),
        ("💰 Investissements", "Paiements sécurisés, suivi, récompenses"),
        ("💬 Messagerie", "Chat temps réel, conversations privées"),
        ("🔔 Notifications", "Système complet, préférences utilisateur"),
        ("🎨 Interface", "Responsive, Tailwind CSS, design africain"),
        ("🔧 Administration", "Django admin, modération, statistiques"),
        ("🌍 Multi-pays", "23 pays africains supportés"),
        ("💱 Devises", "FCFA, calculs automatiques"),
        ("📱 Mobile-ready", "PWA-ready, responsive design"),
    ]
    
    for feature, description in features:
        print(f"   {feature:<20} {description}")
    
    return True

def demo_stats():
    """Démonstration des statistiques"""
    print("\n📈 STATISTIQUES PLATEFORME")
    print("-" * 30)
    
    try:
        from django.contrib.auth import get_user_model
        from apps.categories.models import Category
        from apps.projects.models import Project
        from apps.investments.models import Investment
        from apps.messaging.models import Conversation
        from apps.notifications.models import Notification
        
        User = get_user_model()
        
        stats = {
            "Utilisateurs totaux": User.objects.count(),
            "Porteurs de projets": User.objects.filter(user_type='porteur').count(),
            "Investisseurs": User.objects.filter(user_type='investisseur').count(),
            "Catégories": Category.objects.count(),
            "Projets": Project.objects.count(),
            "Projets actifs": Project.objects.filter(status='active').count(),
            "Investissements": Investment.objects.count(),
            "Conversations": Conversation.objects.count(),
            "Notifications": Notification.objects.count(),
        }
        
        for stat, value in stats.items():
            print(f"   {stat:<20} {value:>8}")
        
        # Calculs avancés
        total_goal = Project.objects.aggregate(
            total=models.Sum('goal_amount')
        )['total'] or 0
        
        total_raised = Project.objects.aggregate(
            total=models.Sum('current_amount')
        )['total'] or 0
        
        print(f"\n💰 FINANCEMENTS")
        print(f"   Objectifs totaux:    {total_goal:>12,.0f} FCFA")
        print(f"   Montants levés:      {total_raised:>12,.0f} FCFA")
        if total_goal > 0:
            print(f"   Taux de réussite:    {(total_raised/total_goal)*100:>11.1f}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def main():
    """Fonction principale de démonstration"""
    print("🎬 DÉMONSTRATION INVESTAFRIK")
    print("=" * 50)
    print("Plateforme de Crowdfunding Africaine")
    print("=" * 50)
    
    # Vérifier qu'on est dans le bon répertoire
    if not Path('manage.py').exists():
        print("❌ Erreur: manage.py non trouvé")
        print("   Exécutez ce script depuis le répertoire investafrik/")
        sys.exit(1)
    
    # Démonstrations
    demos = [
        ("Utilisateurs", demo_users),
        ("Catégories", demo_categories),
        ("Projets", demo_projects),
        ("API", demo_api_endpoints),
        ("Fonctionnalités", demo_features),
        ("Statistiques", demo_stats),
    ]
    
    for name, demo_func in demos:
        try:
            demo_func()
        except Exception as e:
            print(f"❌ Erreur dans {name}: {e}")
    
    print("\n" + "=" * 50)
    print("🌐 ACCÈS À LA PLATEFORME")
    print("=" * 50)
    print("🏠 Site web:     http://127.0.0.1:8000")
    print("🔧 Admin:        http://127.0.0.1:8000/admin")
    print("🔌 API:          http://127.0.0.1:8000/api")
    
    print("\n🔑 CONNEXION ADMIN:")
    print("   Email:        admin@investafrik.com")
    print("   Mot de passe: admin123")
    
    print("\n👤 UTILISATEURS TEST:")
    print("   Porteur:      amina.diallo@example.com / password123")
    print("   Investisseur: jean.dupont@example.com / password123")
    
    print("\n🚀 COMMANDES UTILES:")
    print("   Démarrer:     python manage.py runserver")
    print("   Tests:        python final_check.py")
    print("   PostgreSQL:   python setup_postgres.py")
    
    print("\n🎉 InvestAfrik est prêt à transformer l'écosystème entrepreneurial africain !")

if __name__ == '__main__':
    main()