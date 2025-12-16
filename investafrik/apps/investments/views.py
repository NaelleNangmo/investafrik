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