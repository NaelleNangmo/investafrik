"""
API URLs for accounts app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    # Authentication
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Password reset
    path('password/reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password/reset/confirm/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    # Profile
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('me/', views.ProfileView.as_view(), name='me'),
    path('me/update/', views.ProfileUpdateView.as_view(), name='me_update'),
    
    # Router URLs
    path('', include(router.urls)),
]