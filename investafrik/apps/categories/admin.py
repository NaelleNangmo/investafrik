"""
Admin configuration for categories app.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin for Category model."""
    list_display = [
        'name', 'slug', 'color_preview', 'icon_preview', 
        'project_count', 'is_active', 'order'
    ]
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']
    
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description')
        }),
        ('Apparence', {
            'fields': ('icon_class', 'color_hex', 'order')
        }),
        ('Statut', {
            'fields': ('is_active',)
        }),
    )
    
    def color_preview(self, obj):
        """Display color preview."""
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border-radius: 3px;"></div>',
            obj.color_hex
        )
    color_preview.short_description = 'Couleur'
    
    def icon_preview(self, obj):
        """Display icon preview."""
        return format_html(
            '<i class="{}" style="font-size: 18px; color: {};"></i>',
            obj.icon_class,
            obj.color_hex
        )
    icon_preview.short_description = 'Icône'
    
    def project_count(self, obj):
        """Display project count."""
        return obj.project_count
    project_count.short_description = 'Projets'