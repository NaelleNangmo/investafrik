"""
Project models for InvestAfrik platform.
"""
import uuid
from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from datetime import timedelta


class Project(models.Model):
    """Main project model."""
    
    STATUS_CHOICES = [
        ('draft', 'Brouillon'),
        ('pending', 'En attente de validation'),
        ('active', 'Actif'),
        ('successful', 'Financé avec succès'),
        ('failed', 'Échec'),
        ('cancelled', 'Annulé'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        'accounts.User', 
        on_delete=models.CASCADE, 
        related_name='projects'
    )
    category = models.ForeignKey(
        'categories.Category', 
        on_delete=models.CASCADE, 
        related_name='projects'
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    short_description = models.CharField(max_length=200)
    full_description = RichTextUploadingField()
    
    # Financial information
    goal_amount = models.DecimalField(
        max_digits=15, 
        decimal_places=2,
        validators=[MinValueValidator(100000)],  # Minimum 100k FCFA
        help_text="Objectif de financement en FCFA"
    )
    current_amount = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        default=0,
        help_text="Montant actuellement levé en FCFA"
    )
    currency = models.CharField(max_length=10, default='FCFA')
    
    # Location and timing
    country = models.CharField(max_length=2, choices=models.TextChoices('Country', 
        'CM SN CI BJ TG BF ML NE GN CD CG GA TD CF RW BI KE TZ UG NG GH MG MU').choices)
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Status and visibility
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    
    # Media
    featured_image = models.ImageField(upload_to='projects/featured/', blank=True, null=True)
    video_url = models.URLField(blank=True, help_text="URL YouTube ou Vimeo")
    
    # Additional data
    budget_breakdown = models.JSONField(
        default=dict,
        help_text="Répartition détaillée du budget"
    )
    
    # Metrics
    views_count = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'projects_project'
        verbose_name = 'Projet'
        verbose_name_plural = 'Projets'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    @property
    def funding_percentage(self):
        """Calculate funding percentage."""
        if self.goal_amount > 0:
            return min((self.current_amount / self.goal_amount) * 100, 100)
        return 0
    
    @property
    def days_remaining(self):
        """Calculate days remaining for funding."""
        if self.end_date:
            remaining = (self.end_date - timezone.now().date()).days
            return max(remaining, 0)
        return 0
    
    @property
    def is_active(self):
        """Check if project is currently active for funding."""
        return (
            self.status == 'active' and 
            self.start_date <= timezone.now().date() <= self.end_date
        )
    
    @property
    def is_successful(self):
        """Check if project reached its funding goal."""
        return self.current_amount >= self.goal_amount
    
    @property
    def investor_count(self):
        """Get number of unique investors."""
        return self.investments.filter(payment_status='completed').values('investor').distinct().count()
    
    def update_current_amount(self):
        """Update current amount based on successful investments."""
        from django.db.models import Sum
        total = self.investments.filter(payment_status='completed').aggregate(
            total=Sum('amount')
        )['total'] or 0
        self.current_amount = total
        self.save(update_fields=['current_amount'])


class ProjectImage(models.Model):
    """Additional images for projects."""
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'projects_projectimage'
        verbose_name = 'Image de projet'
        verbose_name_plural = 'Images de projets'
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"Image {self.order} - {self.project.title}"


class ProjectUpdate(models.Model):
    """Project updates/news from project owners."""
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='updates')
    title = models.CharField(max_length=200)
    content = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'projects_projectupdate'
        verbose_name = 'Mise à jour de projet'
        verbose_name_plural = 'Mises à jour de projets'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.project.title} - {self.title}"


class ProjectComment(models.Model):
    """Comments on projects."""
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    content = models.TextField()
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'projects_projectcomment'
        verbose_name = 'Commentaire'
        verbose_name_plural = 'Commentaires'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Commentaire de {self.user.get_full_name()} sur {self.project.title}"


class SavedProject(models.Model):
    """User's saved/bookmarked projects (wishlist)."""
    
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='saved_projects')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'projects_savedproject'
        verbose_name = 'Projet sauvegardé'
        verbose_name_plural = 'Projets sauvegardés'
        unique_together = ('user', 'project')
        ordering = ['-saved_at']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.project.title}"