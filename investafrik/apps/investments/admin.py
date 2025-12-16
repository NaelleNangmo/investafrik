"""
Admin configuration for investments app.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Investment, InvestmentReward, InvestmentRewardChoice


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    """Admin for Investment model."""
    list_display = [
        'transaction_id', 'investor', 'project', 'amount',
        'payment_status', 'payment_method', 'invested_at'
    ]
    list_filter = ['payment_status', 'payment_method', 'invested_at']
    search_fields = [
        'transaction_id', 'investor__email', 'project__title',
        'payment_reference'
    ]
    readonly_fields = ['transaction_id', 'invested_at']
    
    fieldsets = (
        ('Investissement', {
            'fields': ('investor', 'project', 'amount', 'message')
        }),
        ('Paiement', {
            'fields': (
                'payment_method', 'payment_status', 'transaction_id',
                'payment_reference', 'payment_provider'
            )
        }),
        ('Dates', {
            'fields': ('invested_at', 'payment_completed_at', 'refunded_at')
        }),
        ('Métadonnées', {
            'fields': ('ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
    )


@admin.register(InvestmentReward)
class InvestmentRewardAdmin(admin.ModelAdmin):
    """Admin for InvestmentReward model."""
    list_display = [
        'title', 'project', 'minimum_amount', 'quantity_available',
        'quantity_claimed', 'is_active'
    ]
    list_filter = ['is_active', 'is_limited', 'created_at']
    search_fields = ['title', 'project__title']


@admin.register(InvestmentRewardChoice)
class InvestmentRewardChoiceAdmin(admin.ModelAdmin):
    """Admin for InvestmentRewardChoice model."""
    list_display = ['investment', 'reward', 'is_delivered']
    list_filter = ['is_delivered']
    search_fields = ['investment__transaction_id', 'reward__title']