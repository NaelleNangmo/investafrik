"""
API views for projects app.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Project, ProjectComment, SavedProject
from .serializers import ProjectSerializer, ProjectListSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    """ViewSet for projects."""
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'status', 'country']
    search_fields = ['title', 'short_description', 'owner__first_name', 'owner__last_name']
    ordering_fields = ['created_at', 'goal_amount', 'current_amount', 'end_date']
    ordering = ['-created_at']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectListSerializer
        return ProjectSerializer
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    @action(detail=True, methods=['post'])
    def invest(self, request, pk=None):
        """Invest in a project."""
        # TODO: Implement investment logic
        return Response({'message': 'Investment functionality not implemented yet'})
    
    @action(detail=True, methods=['post', 'delete'])
    def save(self, request, pk=None):
        """Save/unsave a project."""
        project = self.get_object()
        
        if request.method == 'POST':
            saved_project, created = SavedProject.objects.get_or_create(
                user=request.user,
                project=project
            )
            if created:
                return Response({'message': 'Projet sauvegardé'})
            return Response({'message': 'Projet déjà sauvegardé'})
        
        elif request.method == 'DELETE':
            SavedProject.objects.filter(
                user=request.user,
                project=project
            ).delete()
            return Response({'message': 'Projet retiré des favoris'})
    
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """Get project comments."""
        project = self.get_object()
        comments = project.comments.filter(is_approved=True, parent=None)
        # TODO: Implement comment serializer
        return Response({'comments': []})
    
    @action(detail=True, methods=['post'])
    def comment(self, request, pk=None):
        """Add a comment to project."""
        # TODO: Implement comment creation
        return Response({'message': 'Comment functionality not implemented yet'})

# Frontend Views
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages


class ProjectListView(TemplateView):
    """Liste des projets."""
    template_name = 'pages/projects.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Récupérer tous les projets actifs
        projects = Project.objects.filter(status='active').select_related('owner', 'category').order_by('-created_at')
        
        # Pagination simple
        from django.core.paginator import Paginator
        paginator = Paginator(projects, 12)  # 12 projets par page
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Catégories pour le filtre
        from apps.categories.models import Category
        categories = Category.objects.all()
        
        context.update({
            'projects': page_obj,
            'categories': categories,
            'total_projects': projects.count(),
        })
        
        return context


class ProjectDetailView(DetailView):
    """Détail d'un projet."""
    model = Project
    template_name = 'projects/detail.html'
    context_object_name = 'project'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        
        # Projets similaires (même catégorie, excluant le projet actuel)
        similar_projects = Project.objects.filter(
            category=project.category,
            status='active'
        ).exclude(id=project.id).select_related('category')[:3]
        
        context['similar_projects'] = similar_projects
        return context


class ProjectCreateView(LoginRequiredMixin, TemplateView):
    """Création d'un projet."""
    template_name = 'projects/create.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_porteur:
            messages.error(request, "Seuls les porteurs de projets peuvent créer des projets.")
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Récupérer toutes les catégories
        from apps.categories.models import Category
        categories = Category.objects.all().order_by('name')
        context['categories'] = categories
        
        return context
    
    def post(self, request, *args, **kwargs):
        """Gérer la création du projet."""
        try:
            # Récupérer les données du formulaire
            title = request.POST.get('title', '').strip()
            category_id = request.POST.get('category')
            country = request.POST.get('country')
            short_description = request.POST.get('short_description', '').strip()
            full_description = request.POST.get('full_description', '').strip()
            goal_amount = request.POST.get('goal_amount')
            duration = request.POST.get('duration')
            status = request.POST.get('status', 'draft')
            video_url = request.POST.get('video_url', '').strip()
            
            # Validation des champs requis
            errors = []
            
            if not title:
                errors.append("Le titre est requis.")
            elif len(title) < 5:
                errors.append("Le titre doit contenir au moins 5 caractères.")
            
            if not category_id:
                errors.append("La catégorie est requise.")
            
            if not country:
                errors.append("Le pays est requis.")
            
            if not short_description:
                errors.append("La description courte est requise.")
            elif len(short_description) > 200:
                errors.append("La description courte ne peut pas dépasser 200 caractères.")
            
            if not full_description:
                errors.append("La description complète est requise.")
            elif len(full_description) < 50:
                errors.append("La description complète doit contenir au moins 50 caractères.")
            
            if not goal_amount:
                errors.append("L'objectif de financement est requis.")
            else:
                try:
                    goal_amount = float(goal_amount)
                    if goal_amount < 100000:
                        errors.append("L'objectif minimum est de 100,000 FCFA.")
                except ValueError:
                    errors.append("L'objectif de financement doit être un nombre valide.")
            
            if not duration:
                errors.append("La durée de la campagne est requise.")
            else:
                try:
                    duration = int(duration)
                    if duration not in [30, 45, 60, 90]:
                        errors.append("La durée doit être de 30, 45, 60 ou 90 jours.")
                except ValueError:
                    errors.append("La durée doit être un nombre valide.")
            
            # Vérifier que la catégorie existe
            from apps.categories.models import Category
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                errors.append("La catégorie sélectionnée n'existe pas.")
            
            # Si il y a des erreurs, retourner le formulaire avec les erreurs
            if errors:
                for error in errors:
                    messages.error(request, error)
                return self.get(request, *args, **kwargs)
            
            # Calculer les dates
            from datetime import date, timedelta
            start_date = date.today()
            end_date = start_date + timedelta(days=duration)
            
            # Créer le projet
            project = Project.objects.create(
                owner=request.user,
                category=category,
                title=title,
                short_description=short_description,
                full_description=full_description,
                goal_amount=goal_amount,
                country=country,
                start_date=start_date,
                end_date=end_date,
                status=status,
                video_url=video_url if video_url else None
            )
            
            # Gérer l'image si elle est fournie
            if 'featured_image' in request.FILES:
                project.featured_image = request.FILES['featured_image']
                project.save()
            
            # Gérer la répartition du budget
            budget_breakdown = {}
            budget_items = request.POST.getlist('budget_item[]')
            budget_amounts = request.POST.getlist('budget_amount[]')
            
            for i, item in enumerate(budget_items):
                if item.strip() and i < len(budget_amounts) and budget_amounts[i].strip():
                    try:
                        amount = float(budget_amounts[i])
                        if amount > 0:
                            budget_breakdown[item.strip()] = amount
                    except ValueError:
                        pass
            
            if budget_breakdown:
                project.budget_breakdown = budget_breakdown
                project.save()
            
            messages.success(request, f"Projet '{project.title}' créé avec succès !")
            
            # Rediriger vers la page de détail du projet
            return redirect('projects:detail', slug=project.slug)
            
        except Exception as e:
            messages.error(request, f"Erreur lors de la création du projet : {str(e)}")
            return self.get(request, *args, **kwargs)


class ProjectEditView(LoginRequiredMixin, TemplateView):
    """Édition d'un projet."""
    template_name = 'projects/edit.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = get_object_or_404(Project, slug=kwargs['slug'], owner=self.request.user)
        context['project'] = project
        return context


class MyProjectsView(LoginRequiredMixin, TemplateView):
    """Mes projets."""
    template_name = 'projects/my_projects.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_porteur:
            messages.error(request, "Cette page est réservée aux porteurs de projets.")
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Récupérer les projets de l'utilisateur
        user_projects = Project.objects.filter(owner=self.request.user).select_related('category').order_by('-created_at')
        
        # Statistiques
        from apps.investments.models import Investment
        from django.db.models import Sum, Count
        
        total_projects = user_projects.count()
        active_projects = user_projects.filter(status='active').count()
        draft_projects = user_projects.filter(status='draft').count()
        
        # Montant total levé
        total_raised = Investment.objects.filter(
            project__owner=self.request.user,
            payment_status='completed'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        context.update({
            'projects': user_projects,
            'total_projects': total_projects,
            'active_projects': active_projects,
            'draft_projects': draft_projects,
            'total_raised': total_raised,
        })
        
        return context