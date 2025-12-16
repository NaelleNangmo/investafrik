"""
API views for categories app.
"""
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category
from .serializers import CategorySerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for categories."""
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active']
    lookup_field = 'slug'
    
    @action(detail=True, methods=['get'])
    def projects(self, request, slug=None):
        """Get projects in this category."""
        category = self.get_object()
        projects = category.projects.filter(status='active')
        
        # Import here to avoid circular imports
        from apps.projects.serializers import ProjectListSerializer
        serializer = ProjectListSerializer(projects, many=True, context={'request': request})
        
        return Response({
            'category': CategorySerializer(category).data,
            'projects': serializer.data,
            'count': projects.count()
        })
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get category statistics."""
        categories = self.get_queryset()
        stats = []
        
        for category in categories:
            stats.append({
                'id': category.id,
                'name': category.name,
                'slug': category.slug,
                'project_count': category.project_count,
                'total_funded': category.total_funded_amount,
                'color': category.color_hex,
                'icon': category.icon_class
            })
        
        return Response(stats)