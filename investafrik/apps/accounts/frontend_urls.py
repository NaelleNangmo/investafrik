"""
Frontend URLs for accounts app.
"""
from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.LoginPageView.as_view(), name='login'),
    path('register/', views.RegisterPageView.as_view(), name='register'),
    path('logout/', views.LogoutPageView.as_view(), name='logout'),
    path('profile/', views.ProfilePageView.as_view(), name='profile'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('dashboard/porteur/', views.DashboardPorteurView.as_view(), name='dashboard_porteur'),
    path('dashboard/investisseur/', views.DashboardInvestisseurView.as_view(), name='dashboard_investisseur'),
]