"""
API views for accounts app.
"""
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User, UserProfile
from .serializers import (
    UserSerializer, UserRegistrationSerializer, 
    LoginSerializer, ProfileSerializer
)


class RegisterView(generics.CreateAPIView):
    """User registration view."""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    """User login view."""
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        user = authenticate(email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            })
        
        return Response(
            {'error': 'Invalid credentials'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )


class LogoutView(generics.GenericAPIView):
    """User logout view."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveAPIView):
    """Get current user profile."""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class ProfileUpdateView(generics.UpdateAPIView):
    """Update current user profile."""
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class PasswordResetView(generics.GenericAPIView):
    """Password reset request view."""
    permission_classes = [AllowAny]
    
    def post(self, request):
        # TODO: Implement password reset logic
        return Response({'message': 'Password reset email sent'})


class PasswordResetConfirmView(generics.GenericAPIView):
    """Password reset confirmation view."""
    permission_classes = [AllowAny]
    
    def post(self, request):
        # TODO: Implement password reset confirmation logic
        return Response({'message': 'Password reset successful'})


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """User viewset for listing and retrieving users."""
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def dashboard_stats(self, request):
        """Get dashboard statistics for current user."""
        from apps.projects.models import Project
        from apps.investments.models import Investment
        from django.db.models import Sum, Count
        
        user = request.user
        
        if user.user_type == 'porteur':
            # Statistiques pour porteur
            user_projects = Project.objects.filter(owner=user)
            
            total_projects = user_projects.count()
            active_projects = user_projects.filter(status='active').count()
            
            total_raised = Investment.objects.filter(
                project__owner=user,
                payment_status='completed'
            ).aggregate(total=Sum('amount'))['total'] or 0
            
            total_investors = Investment.objects.filter(
                project__owner=user,
                payment_status='completed'
            ).values('investor').distinct().count()
            
            # Projets récents avec leurs statistiques
            recent_projects = []
            for project in user_projects.order_by('-created_at')[:5]:
                project_raised = Investment.objects.filter(
                    project=project,
                    payment_status='completed'
                ).aggregate(total=Sum('amount'))['total'] or 0
                
                recent_projects.append({
                    'id': project.id,
                    'slug': project.slug,
                    'title': project.title,
                    'short_description': project.short_description,
                    'status': project.status,
                    'goal_amount': float(project.goal_amount),
                    'current_amount': float(project_raised),
                    'category': {
                        'name': project.category.name,
                        'slug': project.category.slug
                    } if project.category else None,
                    'featured_image': project.featured_image.url if project.featured_image else None,
                    'created_at': project.created_at.isoformat(),
                    'funding_percentage': (project_raised / project.goal_amount * 100) if project.goal_amount > 0 else 0
                })
            
            return Response({
                'user_type': 'porteur',
                'stats': {
                    'total_projects': total_projects,
                    'active_projects': active_projects,
                    'total_raised': float(total_raised),
                    'total_investors': total_investors
                },
                'recent_projects': recent_projects
            })
            
        elif user.user_type == 'investisseur':
            # Statistiques pour investisseur
            user_investments = Investment.objects.filter(
                investor=user,
                payment_status='completed'
            )
            
            total_invested = user_investments.aggregate(
                total=Sum('amount')
            )['total'] or 0
            
            total_projects = user_investments.values('project').distinct().count()
            
            return Response({
                'user_type': 'investisseur',
                'stats': {
                    'total_invested': float(total_invested),
                    'total_projects': total_projects,
                    'total_investments': user_investments.count()
                }
            })
        
        return Response({'error': 'Type d\'utilisateur non reconnu'}, status=400)
    
    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        """Follow/unfollow a user."""
        # TODO: Implement follow functionality
        return Response({'message': 'Follow functionality not implemented yet'})


# Frontend Views
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect


class LoginPageView(TemplateView):
    """Page de connexion."""
    template_name = 'accounts/login.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:dashboard')
        return super().dispatch(request, *args, **kwargs)


class RegisterPageView(TemplateView):
    """Page d'inscription."""
    template_name = 'accounts/register.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:dashboard')
        return super().dispatch(request, *args, **kwargs)


class ProfilePageView(LoginRequiredMixin, TemplateView):
    """Page de profil utilisateur."""
    template_name = 'accounts/profile.html'


class DashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard view that redirects based on user type."""
    
    def get(self, request, *args, **kwargs):
        if request.user.user_type == 'porteur':
            return redirect('/auth/dashboard/porteur/')
        elif request.user.user_type == 'investisseur':
            return redirect('/auth/dashboard/investisseur/')
        else:
            # Default dashboard for admin or other types
            return redirect('/auth/dashboard/porteur/')


class DashboardPorteurView(LoginRequiredMixin, TemplateView):
    """Dashboard pour les porteurs de projets."""
    template_name = 'accounts/dashboard_porteur.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type != 'porteur':
            return redirect('accounts:dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Récupérer les projets de l'utilisateur
        from apps.projects.models import Project
        from apps.investments.models import Investment
        from django.db.models import Sum, Count
        
        user_projects = Project.objects.filter(owner=self.request.user)
        
        # Statistiques
        total_projects = user_projects.count()
        active_projects = user_projects.filter(status='active').count()
        
        # Montant total levé
        total_raised = Investment.objects.filter(
            project__owner=self.request.user,
            payment_status='completed'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Nombre d'investisseurs uniques
        total_investors = Investment.objects.filter(
            project__owner=self.request.user,
            payment_status='completed'
        ).values('investor').distinct().count()
        
        # Projets récents
        recent_projects = user_projects.order_by('-created_at')[:5]
        
        context.update({
            'total_projects': total_projects,
            'active_projects': active_projects,
            'total_raised': total_raised,
            'total_investors': total_investors,
            'recent_projects': recent_projects,
        })
        
        return context


class DashboardInvestisseurView(LoginRequiredMixin, TemplateView):
    """Dashboard pour les investisseurs."""
    template_name = 'accounts/dashboard_investisseur.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type != 'investisseur':
            return redirect('accounts:dashboard')
        return super().dispatch(request, *args, **kwargs)


class LogoutPageView(TemplateView):
    """Vue de déconnexion."""
    
    def post(self, request, *args, **kwargs):
        from django.contrib.auth import logout
        from django.http import JsonResponse
        from django.contrib.sessions.models import Session
        
        # Clear all user sessions
        if request.user.is_authenticated:
            # Delete all sessions for this user
            user_sessions = Session.objects.all()
            for session in user_sessions:
                session_data = session.get_decoded()
                if session_data.get('_auth_user_id') == str(request.user.id):
                    session.delete()
        
        # Déconnexion Django
        logout(request)
        
        # Clear session completely
        request.session.flush()
        
        # Réponse JSON pour indiquer le succès
        return JsonResponse({
            'success': True, 
            'message': 'Déconnexion réussie',
            'redirect': '/'
        })
    
    def get(self, request, *args, **kwargs):
        from django.contrib.auth import logout
        logout(request)
        request.session.flush()
        return redirect('home')