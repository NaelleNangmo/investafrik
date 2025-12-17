"""
Management command to seed the database with test data.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.categories.models import Category
from apps.projects.models import Project
from decimal import Decimal
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed database with test data'
    
    def handle(self, *args, **options):
        self.stdout.write('Starting data seeding...')
        
        # Create categories
        self.create_categories()
        
        # Create users
        self.create_users()
        
        # Create projects
        self.create_projects()
        
        self.stdout.write(
            self.style.SUCCESS('Successfully seeded database!')
        )
    
    def create_categories(self):
        """Create project categories."""
        categories_data = [
            {
                'name': 'Agriculture & Agrobusiness',
                'description': 'Projets agricoles, élevage, transformation agricole',
                'icon_class': 'fas fa-seedling',
                'color_hex': '#4CAF50',
                'order': 1
            },
            {
                'name': 'Technologies & Innovation',
                'description': 'Startups tech, applications mobiles, solutions digitales',
                'icon_class': 'fas fa-laptop-code',
                'color_hex': '#2196F3',
                'order': 2
            },
            {
                'name': 'Éducation & Formation',
                'description': 'Écoles, centres de formation, e-learning',
                'icon_class': 'fas fa-graduation-cap',
                'color_hex': '#FF9800',
                'order': 3
            },
            {
                'name': 'Santé & Bien-être',
                'description': 'Cliniques, pharmacies, équipements médicaux',
                'icon_class': 'fas fa-heartbeat',
                'color_hex': '#E91E63',
                'order': 4
            },
            {
                'name': 'Commerce & Services',
                'description': 'Boutiques, restaurants, services divers',
                'icon_class': 'fas fa-store',
                'color_hex': '#9C27B0',
                'order': 5
            },
            {
                'name': 'Énergies Renouvelables',
                'description': 'Solaire, éolien, biogaz',
                'icon_class': 'fas fa-solar-panel',
                'color_hex': '#FFEB3B',
                'order': 6
            },
            {
                'name': 'Artisanat & Culture',
                'description': 'Artisanat local, événements culturels, mode africaine',
                'icon_class': 'fas fa-palette',
                'color_hex': '#795548',
                'order': 7
            },
            {
                'name': 'Immobilier & Construction',
                'description': 'Logements, infrastructures',
                'icon_class': 'fas fa-building',
                'color_hex': '#607D8B',
                'order': 8
            },
            {
                'name': 'Transport & Logistique',
                'description': 'Services de transport, livraison',
                'icon_class': 'fas fa-truck',
                'color_hex': '#FF5722',
                'order': 9
            },
            {
                'name': 'Environnement & Recyclage',
                'description': 'Gestion des déchets, projets écologiques',
                'icon_class': 'fas fa-recycle',
                'color_hex': '#4CAF50',
                'order': 10
            }
        ]
        
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')
    
    def create_users(self):
        """Create test users."""
        # Create superuser if not exists
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                email='admin@investafrik.com',
                username='admin',
                password='admin123',
                first_name='Admin',
                last_name='InvestAfrik',
                user_type='porteur',
                country='CM'
            )
            self.stdout.write('Created superuser')
        
        # Create test users
        users_data = [
            # Porteurs de projets
            {'email': 'amina.diallo@example.com', 'username': 'amina_diallo', 'first_name': 'Amina', 'last_name': 'Diallo', 'user_type': 'porteur', 'country': 'SN', 'bio': 'Entrepreneure passionnée par l\'agriculture durable au Sénégal.'},
            {'email': 'kwame.asante@example.com', 'username': 'kwame_asante', 'first_name': 'Kwame', 'last_name': 'Asante', 'user_type': 'porteur', 'country': 'GH', 'bio': 'Développeur et fondateur de startup tech à Accra.'},
            {'email': 'fatou.ba@example.com', 'username': 'fatou_ba', 'first_name': 'Fatou', 'last_name': 'Ba', 'user_type': 'porteur', 'country': 'CM', 'bio': 'Éducatrice et directrice d\'école numérique à Yaoundé.'},
            {'email': 'ibrahim.kone@example.com', 'username': 'ibrahim_kone', 'first_name': 'Ibrahim', 'last_name': 'Koné', 'user_type': 'porteur', 'country': 'CI', 'bio': 'Ingénieur en énergies renouvelables, spécialiste du solaire.'},
            {'email': 'aisha.mwangi@example.com', 'username': 'aisha_mwangi', 'first_name': 'Aisha', 'last_name': 'Mwangi', 'user_type': 'porteur', 'country': 'KE', 'bio': 'Designer et artisane, créatrice de mode africaine moderne.'},
            
            # Investisseurs
            {'email': 'jean.dupont@example.com', 'username': 'jean_dupont', 'first_name': 'Jean', 'last_name': 'Dupont', 'user_type': 'investisseur', 'country': 'CM', 'bio': 'Investisseur privé passionné par l\'innovation africaine.', 'budget': 50000000},
            {'email': 'marie.martin@example.com', 'username': 'marie_martin', 'first_name': 'Marie', 'last_name': 'Martin', 'user_type': 'investisseur', 'country': 'SN', 'bio': 'Angel investor spécialisée dans les startups tech.', 'budget': 25000000},
            {'email': 'paul.bernard@example.com', 'username': 'paul_bernard', 'first_name': 'Paul', 'last_name': 'Bernard', 'user_type': 'investisseur', 'country': 'CI', 'bio': 'Entrepreneur et investisseur dans l\'éducation.', 'budget': 30000000},
            {'email': 'sophie.leroy@example.com', 'username': 'sophie_leroy', 'first_name': 'Sophie', 'last_name': 'Leroy', 'user_type': 'investisseur', 'country': 'BJ', 'bio': 'Investisseuse impact, focus développement durable.', 'budget': 40000000},
            {'email': 'david.moreau@example.com', 'username': 'david_moreau', 'first_name': 'David', 'last_name': 'Moreau', 'user_type': 'investisseur', 'country': 'TG', 'bio': 'Business angel, ancien dirigeant de startup.', 'budget': 35000000},
        ]
        
        for user_data in users_data:
            if not User.objects.filter(email=user_data['email']).exists():
                budget = user_data.pop('budget', None)
                user = User.objects.create_user(
                    password='password123',
                    **user_data
                )
                if budget:
                    user.available_budget = budget
                    user.save()
                self.stdout.write(f'Created user: {user.get_full_name()}')
        
        self.stdout.write('Created test users')
    
    def create_projects(self):
        """Create test projects."""
        from apps.projects.models import Project
        from datetime import date, timedelta
        
        # Get categories and users
        categories = Category.objects.all()
        porteurs = User.objects.filter(user_type='porteur')
        
        if not categories.exists() or not porteurs.exists():
            self.stdout.write('No categories or porteurs found, skipping projects creation')
            return
        
        projects_data = [
            # Agriculture & Agrobusiness
            {
                'title': 'FarmTech Solutions - Agriculture Intelligente',
                'short_description': 'Application mobile pour optimiser la gestion des exploitations agricoles au Cameroun',
                'full_description': '<p>FarmTech Solutions révolutionne l\'agriculture camerounaise avec une application mobile innovante qui aide les agriculteurs à optimiser leurs rendements, gérer leurs ressources et accéder aux marchés.</p><p>Notre solution comprend des fonctionnalités de suivi des cultures, prévisions météo, conseils personnalisés et marketplace intégrée.</p>',
                'goal_amount': 5000000,
                'current_amount': 1250000,
                'country': 'CM',
                'start_date': date.today() - timedelta(days=15),
                'end_date': date.today() + timedelta(days=45),
                'status': 'active',
                'category_name': 'Agriculture & Agrobusiness'
            },
            {
                'title': 'Ferme Aquaponique Moderne',
                'short_description': 'Système d\'aquaponie pour production durable de poissons et légumes au Sénégal',
                'full_description': '<p>Création d\'une ferme aquaponique moderne utilisant des techniques innovantes pour produire simultanément poissons et légumes avec 90% moins d\'eau.</p><p>Formation des jeunes agriculteurs aux nouvelles technologies agricoles durables.</p>',
                'goal_amount': 8000000,
                'current_amount': 3200000,
                'country': 'SN',
                'start_date': date.today() - timedelta(days=30),
                'end_date': date.today() + timedelta(days=30),
                'status': 'active',
                'category_name': 'Agriculture & Agrobusiness',
                'featured_image': 'https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=800&h=600&fit=crop'
            },
            
            # Technologies & Innovation
            {
                'title': 'AfriPay - Solution de Paiement Mobile',
                'short_description': 'Plateforme de paiement mobile unifiée pour l\'Afrique de l\'Ouest',
                'full_description': '<p>AfriPay simplifie les transactions financières en Afrique de l\'Ouest en connectant tous les services de mobile money dans une seule application.</p><p>API ouverte pour les commerçants, transferts internationaux facilités, et inclusion financière renforcée.</p>',
                'goal_amount': 25000000,
                'current_amount': 18750000,
                'country': 'GH',
                'start_date': date.today() - timedelta(days=45),
                'end_date': date.today() + timedelta(days=15),
                'status': 'active',
                'category_name': 'Technologies & Innovation',
                'featured_image': 'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=800&h=600&fit=crop'
            },
            {
                'title': 'HealthTech AI Diagnostic',
                'short_description': 'IA pour diagnostic médical précoce dans les zones rurales',
                'full_description': '<p>Système d\'intelligence artificielle pour aider les agents de santé communautaires à diagnostiquer rapidement les maladies courantes.</p><p>Réduction de 70% du temps de diagnostic et amélioration de l\'accès aux soins dans les zones reculées.</p>',
                'goal_amount': 12000000,
                'current_amount': 4800000,
                'country': 'KE',
                'start_date': date.today() - timedelta(days=20),
                'end_date': date.today() + timedelta(days=40),
                'status': 'active',
                'category_name': 'Technologies & Innovation',
                'featured_image': 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=800&h=600&fit=crop'
            },
            
            # Éducation & Formation
            {
                'title': 'École Numérique de Yaoundé',
                'short_description': 'Centre de formation en programmation pour jeunes défavorisés',
                'full_description': '<p>L\'École Numérique de Yaoundé vise à former 200 jeunes défavorisés aux métiers du numérique chaque année.</p><p>Programme complet incluant développement web, mobile, design et entrepreneuriat digital avec garantie d\'emploi.</p>',
                'goal_amount': 15000000,
                'current_amount': 12000000,
                'country': 'CM',
                'start_date': date.today() - timedelta(days=60),
                'end_date': date.today() + timedelta(days=30),
                'status': 'active',
                'category_name': 'Éducation & Formation',
                'featured_image': 'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=800&h=600&fit=crop'
            },
            {
                'title': 'Bibliothèque Numérique Africaine',
                'short_description': 'Plateforme d\'apprentissage en ligne avec contenu africain',
                'full_description': '<p>Création d\'une vaste bibliothèque numérique avec des contenus éducatifs adaptés au contexte africain, disponible hors ligne.</p><p>Partenariats avec les écoles rurales pour démocratiser l\'accès à l\'éducation de qualité.</p>',
                'goal_amount': 20000000,
                'current_amount': 8000000,
                'country': 'BF',
                'start_date': date.today() - timedelta(days=10),
                'end_date': date.today() + timedelta(days=80),
                'status': 'active',
                'category_name': 'Éducation & Formation',
                'featured_image': 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=800&h=600&fit=crop'
            },
            
            # Énergies Renouvelables
            {
                'title': 'GreenEnergy Côte d\'Ivoire',
                'short_description': 'Kits solaires pour électrification rurale',
                'full_description': '<p>Projet d\'électrification de 50 villages ruraux en Côte d\'Ivoire avec des kits solaires abordables et durables.</p><p>Impact direct sur 10,000 personnes avec amélioration de l\'éducation, santé et activités économiques.</p>',
                'goal_amount': 50000000,
                'current_amount': 35000000,
                'country': 'CI',
                'start_date': date.today() - timedelta(days=75),
                'end_date': date.today() + timedelta(days=45),
                'status': 'active',
                'category_name': 'Énergies Renouvelables',
                'featured_image': 'https://images.unsplash.com/photo-1509391366360-2e959784a276?w=800&h=600&fit=crop'
            },
            {
                'title': 'Mini-Réseaux Solaires Intelligents',
                'short_description': 'Réseaux électriques autonomes pour communautés isolées',
                'full_description': '<p>Déploiement de mini-réseaux solaires intelligents avec stockage par batteries pour alimenter des communautés entières.</p><p>Système de paiement mobile intégré et maintenance prédictive par IoT.</p>',
                'goal_amount': 75000000,
                'current_amount': 22500000,
                'country': 'ML',
                'start_date': date.today() - timedelta(days=5),
                'end_date': date.today() + timedelta(days=115),
                'status': 'active',
                'category_name': 'Énergies Renouvelables',
                'featured_image': 'https://images.unsplash.com/photo-1466611653911-95081537e5b7?w=800&h=600&fit=crop'
            },
            
            # Santé & Bien-être
            {
                'title': 'Clinique Mobile Connectée',
                'short_description': 'Unités médicales mobiles avec télémédecine pour zones rurales',
                'full_description': '<p>Déploiement de cliniques mobiles équipées de technologies de télémédecine pour apporter des soins spécialisés dans les zones reculées.</p><p>Connexion satellite pour consultations à distance avec des spécialistes urbains.</p>',
                'goal_amount': 30000000,
                'current_amount': 15000000,
                'country': 'NE',
                'start_date': date.today() - timedelta(days=25),
                'end_date': date.today() + timedelta(days=65),
                'status': 'active',
                'category_name': 'Santé & Bien-être',
                'featured_image': 'https://images.unsplash.com/photo-1559757175-0eb30cd8c063?w=800&h=600&fit=crop'
            },
            
            # Artisanat & Culture
            {
                'title': 'Afro Fashion Hub',
                'short_description': 'Marketplace en ligne pour créateurs de mode africaine',
                'full_description': '<p>Plateforme e-commerce dédiée aux créateurs de mode africaine avec outils de design, production et distribution internationale.</p><p>Formation des artisans aux techniques modernes et accès aux marchés globaux.</p>',
                'goal_amount': 3000000,
                'current_amount': 2700000,
                'country': 'KE',
                'start_date': date.today() - timedelta(days=50),
                'end_date': date.today() + timedelta(days=10),
                'status': 'active',
                'category_name': 'Artisanat & Culture',
                'featured_image': 'https://images.unsplash.com/photo-1445205170230-053b83016050?w=800&h=600&fit=crop'
            }
        ]
        
        for project_data in projects_data:
            category_name = project_data.pop('category_name')
            category = Category.objects.get(name=category_name)
            
            # Assign to appropriate owner based on user type
            porteur_users = User.objects.filter(user_type='porteur')
            if porteur_users.exists():
                owner = porteur_users[random.randint(0, porteur_users.count()-1)]
            else:
                continue
            
            project, created = Project.objects.get_or_create(
                title=project_data['title'],
                defaults={
                    **project_data,
                    'owner': owner,
                    'category': category
                }
            )
            
            if created:
                self.stdout.write(f'Created project: {project.title}')