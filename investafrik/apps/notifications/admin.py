"""
Admin configuration for notifications app.
"""
from django.contrib import admin
from .models import Notification, NotificationPreference


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Admin for Notification model."""
    list_display = [
        'user', 'notification_type', 'title', 'is_read',
        'priority', 'created_at'
    ]
    list_filter = [
        'notification_type', 'is_read', 'priority', 'created_at'
    ]
    search_fields = ['user__email', 'title', 'message']
    readonly_fields = ['created_at', 'read_at']
    
    fieldsets = (
        ('Notification', {
            'fields': ('user', 'notification_type', 'title', 'message', 'link')
        }),
        ('Objets liés', {
            'fields': ('project', 'investment'),
            'classes': ('collapse',)
        }),
        ('Statut', {
            'fields': ('is_read', 'priority')
        }),
        ('Livraison', {
            'fields': (
                'email_sent', 'email_sent_at',
                'push_sent', 'push_sent_at'
            ),
            'classes': ('collapse',)
        }),
        ('Dates', {
            'fields': ('created_at', 'read_at')
        }),
    )


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    """Admin for NotificationPreference model."""
    list_display = ['user', 'email_new_investment', 'push_new_messages']
    search_fields = ['user__email']