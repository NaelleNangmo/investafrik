"""
URLs pour les vues d'administration personnalisées.
"""
from django.urls import path
from . import admin_views

urlpatterns = [
    path('', admin_views.admin_dashboard, name='admin_dashboard'),
]