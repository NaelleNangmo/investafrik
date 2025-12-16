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


class ProjectDetailView(DetailView):
    """Détail d'un projet."""
    model = Project
    template_name = 'projects/detail.html'
    context_object_name = 'project'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class ProjectCreateView(LoginRequiredMixin, TemplateView):
    """Création d'un projet."""
    template_name = 'projects/create.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_porteur:
            messages.error(request, "Seuls les porteurs de projets peuvent créer des projets.")
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)


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