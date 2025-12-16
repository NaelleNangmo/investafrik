"""
Admin configuration for projects app.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Project, ProjectImage, ProjectUpdate, ProjectComment, SavedProject


class ProjectImageInline(admin.TabularInline):
    """Inline admin for ProjectImage."""
    model = ProjectImage
    extra = 1
    fields = ['image', 'caption', 'order']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Admin for Project model."""
    inlines = [ProjectImageInline]
    
    list_display = [
        'title', 'owner', 'category', 'status', 'goal_amount',
        'current_amount', 'funding_percentage_display', 'end_date'
    ]
    list_filter = ['status', 'category', 'country', 'is_featured', 'created_at']
    search_fields = ['title', 'owner__email', 'owner__first_name', 'owner__last_name']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('title', 'slug', 'owner', 'category', 'short_description')
        }),
        ('Description complète', {
            'fields': ('full_description',)
        }),
        ('Financement', {
            'fields': ('goal_amount', 'current_amount', 'currency', 'budget_breakdown')
        }),
        ('Localisation et timing', {
            'fields': ('country', 'start_date', 'end_date')
        }),
        ('Médias', {
            'fields': ('featured_image', 'video_url')
        }),
        ('Statut', {
            'fields': ('status', 'is_featured')
        }),
        ('Statistiques', {
            'fields': ('views_count',),
            'classes': ('collapse',)
        }),
    )
    
    def funding_percentage_display(self, obj):
        percentage = obj.funding_percentage
        color = 'green' if percentage >= 100 else 'orange' if percentage >= 50 else 'red'
        return format_html(
            '<span style="color: {};">{:.1f}%</span>',
            color, percentage
        )
    funding_percentage_display.short_description = 'Financement'


@admin.register(ProjectUpdate)
class ProjectUpdateAdmin(admin.ModelAdmin):
    """Admin for ProjectUpdate model."""
    list_display = ['title', 'project', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'project__title']


@admin.register(ProjectComment)
class ProjectCommentAdmin(admin.ModelAdmin):
    """Admin for ProjectComment model."""
    list_display = ['user', 'project', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['user__email', 'project__title', 'content']
    actions = ['approve_comments', 'reject_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = "Approuver les commentaires sélectionnés"
    
    def reject_comments(self, request, queryset):
        queryset.update(is_approved=False)
    reject_comments.short_description = "Rejeter les commentaires sélectionnés"


@admin.register(SavedProject)
class SavedProjectAdmin(admin.ModelAdmin):
    """Admin for SavedProject model."""
    list_display = ['user', 'project', 'saved_at']
    list_filter = ['saved_at']
    search_fields = ['user__email', 'project__title']