"""
Category models for InvestAfrik platform.
"""
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """Project categories model."""
    
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField()
    icon_class = models.CharField(
        max_length=50, 
        help_text="Classe CSS pour l'icône (ex: 'fas fa-seedling')"
    )
    color_hex = models.CharField(
        max_length=7, 
        help_text="Couleur hexadécimale (ex: '#4CAF50')"
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Ordre d'affichage")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'categories_category'
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    @property
    def project_count(self):
        """Get the number of active projects in this category."""
        return self.projects.filter(status='active').count()
    
    @property
    def total_funded_amount(self):
        """Get total amount funded in this category."""
        from django.db.models import Sum
        result = self.projects.filter(status='successful').aggregate(
            total=Sum('current_amount')
        )
        return result['total'] or 0