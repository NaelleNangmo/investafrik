#!/usr/bin/env python
"""
Script pour enregistrer tous les modèles dans l'admin personnalisé.
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investafrik.settings.development')
django.setup()

from django.contrib import admin
from apps.accounts.admin import admin_site
from apps.projects.models import Project, ProjectImage, ProjectUpdate, ProjectComment
from apps.investments.models import Investment
from apps.messaging.models import Conversation, Message
from apps.categories.models import Category
from apps.notifications.models import Notification

# Enregistrer les modèles Projects
@admin.register(Project, site=admin_site)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'category', 'status', 'goal_amount', 'current_amount', 'created_at']
    list_filter = ['status', 'category', 'country', 'created_at']
    search_fields = ['title', 'owner__email', 'owner__first_name', 'owner__last_name']
    readonly_fields = ['slug', 'current_amount', 'views_count']

@admin.register(Investment, site=admin_site)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ['investor', 'project', 'amount', 'payment_status', 'created_at']
    list_filter = ['payment_status', 'payment_method', 'created_at']
    search_fields = ['investor__email', 'project__title']

@admin.register(Category, site=admin_site)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']

@admin.register(Conversation, site=admin_site)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['participant_1', 'participant_2', 'project', 'created_at']
    list_filter = ['created_at']
    search_fields = ['participant_1__email', 'participant_2__email']

@admin.register(Message, site=admin_site)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'conversation', 'content', 'is_read', 'sent_at']
    list_filter = ['is_read', 'message_type', 'sent_at']
    search_fields = ['sender__email', 'content']

print("✅ Tous les modèles ont été enregistrés dans l'admin personnalisé")