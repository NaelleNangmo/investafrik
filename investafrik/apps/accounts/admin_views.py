"""
Vues personnalisées pour l'administration Django.
"""
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from apps.accounts.models import User
from apps.projects.models import Project
from apps.investments.models import Investment
from apps.messaging.models import Conversation, Message
from apps.categories.models import Category


@staff_member_required
def admin_dashboard(request):
    """Dashboard administrateur avec statistiques en temps réel."""
    
    # Statistiques générales
    total_users = User.objects.count()
    total_porteurs = User.objects.filter(user_type='porteur').count()
    total_investisseurs = User.objects.filter(user_type='investisseur').count()
    
    total_projects = Project.objects.count()
    active_projects = Project.objects.filter(status='active').count()
    successful_projects = Project.objects.filter(status='successful').count()
    
    total_investments = Investment.objects.count()
    completed_investments = Investment.objects.filter(payment_status='completed').count()
    
    # Montants financiers
    total_amount_raised = Investment.objects.filter(
        payment_status='completed'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    total_goal_amount = Project.objects.aggregate(
        total=Sum('goal_amount')
    )['total'] or 0
    
    # Statistiques par période
    now = timezone.now()
    last_30_days = now - timedelta(days=30)
    last_7_days = now - timedelta(days=7)
    
    new_users_30d = User.objects.filter(date_joined__gte=last_30_days).count()
    new_projects_30d = Project.objects.filter(created_at__gte=last_30_days).count()
    new_investments_30d = Investment.objects.filter(created_at__gte=last_30_days).count()
    
    new_users_7d = User.objects.filter(date_joined__gte=last_7_days).count()
    new_projects_7d = Project.objects.filter(created_at__gte=last_7_days).count()
    new_investments_7d = Investment.objects.filter(created_at__gte=last_7_days).count()
    
    # Projets par catégorie
    projects_by_category = Category.objects.annotate(
        project_count=Count('projects'),
        total_raised=Sum('projects__investments__amount', 
                        filter=Q(projects__investments__payment_status='completed'))
    ).order_by('-project_count')
    
    # Top projets par montant levé
    top_projects = Project.objects.annotate(
        total_raised=Sum('investments__amount', 
                        filter=Q(investments__payment_status='completed'))
    ).order_by('-total_raised')[:5]
    
    # Top investisseurs
    top_investors = User.objects.filter(user_type='investisseur').annotate(
        total_invested=Sum('investments__amount', 
                          filter=Q(investments__payment_status='completed')),
        investment_count=Count('investments', 
                              filter=Q(investments__payment_status='completed'))
    ).order_by('-total_invested')[:5]
    
    # Activité récente
    recent_projects = Project.objects.order_by('-created_at')[:5]
    recent_investments = Investment.objects.filter(
        payment_status='completed'
    ).order_by('-created_at')[:5]
    recent_users = User.objects.order_by('-date_joined')[:5]
    
    # Données pour les graphiques
    # Évolution des inscriptions (30 derniers jours)
    user_registrations = []
    for i in range(30):
        date = now - timedelta(days=i)
        count = User.objects.filter(
            date_joined__date=date.date()
        ).count()
        user_registrations.append({
            'date': date.strftime('%Y-%m-%d'),
            'count': count
        })
    user_registrations.reverse()
    
    # Évolution des investissements (30 derniers jours)
    investment_evolution = []
    for i in range(30):
        date = now - timedelta(days=i)
        amount = Investment.objects.filter(
            created_at__date=date.date(),
            payment_status='completed'
        ).aggregate(total=Sum('amount'))['total'] or 0
        investment_evolution.append({
            'date': date.strftime('%Y-%m-%d'),
            'amount': float(amount)
        })
    investment_evolution.reverse()
    
    # Répartition des utilisateurs par pays
    users_by_country = User.objects.values('country').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    # Taux de conversion
    conversion_rate = 0
    if total_users > 0:
        active_users = User.objects.filter(
            Q(projects__isnull=False) | Q(investments__isnull=False)
        ).distinct().count()
        conversion_rate = (active_users / total_users) * 100
    
    # Taux de succès des projets
    success_rate = 0
    if total_projects > 0:
        success_rate = (successful_projects / total_projects) * 100
    
    context = {
        # Statistiques générales
        'total_users': total_users,
        'total_porteurs': total_porteurs,
        'total_investisseurs': total_investisseurs,
        'total_projects': total_projects,
        'active_projects': active_projects,
        'successful_projects': successful_projects,
        'total_investments': total_investments,
        'completed_investments': completed_investments,
        
        # Montants
        'total_amount_raised': total_amount_raised,
        'total_goal_amount': total_goal_amount,
        'funding_percentage': (total_amount_raised / total_goal_amount * 100) if total_goal_amount > 0 else 0,
        
        # Croissance
        'new_users_30d': new_users_30d,
        'new_projects_30d': new_projects_30d,
        'new_investments_30d': new_investments_30d,
        'new_users_7d': new_users_7d,
        'new_projects_7d': new_projects_7d,
        'new_investments_7d': new_investments_7d,
        
        # Taux
        'conversion_rate': conversion_rate,
        'success_rate': success_rate,
        
        # Listes
        'projects_by_category': projects_by_category,
        'top_projects': top_projects,
        'top_investors': top_investors,
        'recent_projects': recent_projects,
        'recent_investments': recent_investments,
        'recent_users': recent_users,
        'users_by_country': users_by_country,
        
        # Données pour graphiques
        'user_registrations': user_registrations,
        'investment_evolution': investment_evolution,
    }
    
    return render(request, 'admin/dashboard.html', context)