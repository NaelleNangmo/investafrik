"""
Admin configuration for accounts app.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect
from .models import User, UserProfile
from . import admin_views


class UserProfileInline(admin.StackedInline):
    """Inline admin for UserProfile."""
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profil'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin for User model."""
    inlines = (UserProfileInline,)
    
    list_display = [
        'email', 'get_full_name', 'user_type', 'country', 
        'is_verified', 'is_active', 'date_joined'
    ]
    list_filter = [
        'user_type', 'country', 'is_verified', 'is_active', 
        'date_joined'
    ]
    search_fields = ['email', 'first_name', 'last_name', 'username']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informations personnelles', {
            'fields': ('first_name', 'last_name', 'username', 'phone_number', 'bio')
        }),
        ('Type et localisation', {
            'fields': ('user_type', 'country', 'profile_picture')
        }),
        ('Investissement', {
            'fields': ('available_budget', 'investment_interests'),
            'classes': ('collapse',)
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Dates importantes', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'user_type', 'country'),
        }),
    )
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Nom complet'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin for UserProfile model."""
    list_display = ['user', 'company', 'job_title', 'profile_visibility']
    list_filter = ['profile_visibility', 'email_notifications', 'push_notifications']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'company']
    
    fieldsets = (
        ('Utilisateur', {'fields': ('user',)}),
        ('Informations professionnelles', {
            'fields': ('company', 'job_title', 'experience_years', 'website')
        }),
        ('Réseaux sociaux', {
            'fields': ('linkedin', 'twitter', 'facebook'),
            'classes': ('collapse',)
        }),
        ('Préférences de notification', {
            'fields': ('email_notifications', 'sms_notifications', 'push_notifications')
        }),
        ('Confidentialité', {
            'fields': ('profile_visibility',)
        }),
    )


# Personnalisation de l'admin site
class InvestAfrikAdminSite(admin.AdminSite):
    """Site d'administration personnalisé pour InvestAfrik."""
    site_header = "InvestAfrik Administration"
    site_title = "InvestAfrik Admin"
    index_title = "Tableau de bord InvestAfrik"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', admin_views.admin_dashboard, name='index'),
        ]
        return custom_urls + urls


# Remplacer le site admin par défaut
admin_site = InvestAfrikAdminSite(name='investafrik_admin')

# Réenregistrer tous les modèles sur le nouveau site
admin_site.register(User, UserAdmin)
admin_site.register(UserProfile, UserProfileAdmin)