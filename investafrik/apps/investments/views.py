"""
API views for investments app.
"""
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Investment
from .serializers import InvestmentSerializer


class InvestmentViewSet(viewsets.ModelViewSet):
    """ViewSet for investments."""
    queryset = Investment.objects.all()
    serializer_class = InvestmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['payment_status', 'payment_method']
    
    def perform_create(self, serializer):
        serializer.save(investor=self.request.user)


class MyInvestmentsView(generics.ListAPIView):
    """List current user's investments."""
    serializer_class = InvestmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Investment.objects.filter(investor=self.request.user)


# Frontend Views
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages


class MyInvestmentsPageView(LoginRequiredMixin, TemplateView):
    """Page mes investissements."""
    template_name = 'investments/my_investments.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_investisseur:
            messages.error(request, "Cette page est réservée aux investisseurs.")
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Récupérer les investissements de l'utilisateur
        user_investments = Investment.objects.filter(
            investor=self.request.user
        ).select_related('project', 'project__owner').order_by('-invested_at')
        
        # Statistiques
        from django.db.models import Sum, Count
        
        total_invested = user_investments.filter(
            payment_status='completed'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        total_projects = user_investments.filter(
            payment_status='completed'
        ).values('project').distinct().count()
        
        pending_investments = user_investments.filter(
            payment_status='pending'
        ).count()
        
        # Investissements par statut
        completed_investments = user_investments.filter(payment_status='completed')
        pending_investments_list = user_investments.filter(payment_status='pending')
        
        context.update({
            'investments': user_investments,
            'completed_investments': completed_investments,
            'pending_investments': pending_investments_list,
            'total_invested': total_invested,
            'total_projects': total_projects,
            'pending_count': pending_investments,
        })
        
        return context