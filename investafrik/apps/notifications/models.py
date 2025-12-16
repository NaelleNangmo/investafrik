"""
Notification models for InvestAfrik platform.
"""
import uuid
from django.db import models
from django.utils import timezone


class Notification(models.Model):
    """User notifications model."""
    
    NOTIFICATION_TYPES = [
        ('new_investment', 'Nouvel investissement reçu'),
        ('investment_completed', 'Investissement confirmé'),
        ('project_approved', 'Projet approuvé'),
        ('project_rejected', 'Projet rejeté'),
        ('project_funded', 'Projet financé avec succès'),
        ('project_failed', 'Projet non financé'),
        ('new_message', 'Nouveau message'),
        ('project_update', 'Mise à jour de projet'),
        ('new_comment', 'Nouveau commentaire'),
        ('project_deadline', 'Fin de campagne approche'),
        ('welcome', 'Bienvenue'),
        ('system', 'Notification système'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Faible'),
        ('normal', 'Normale'),
        ('high', 'Élevée'),
        ('urgent', 'Urgente'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        'accounts.User', 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    
    # Optional link to redirect user when notification is clicked
    link = models.URLField(blank=True)
    
    # Related objects (optional)
    project = models.ForeignKey(
        'projects.Project', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='notifications'
    )
    investment = models.ForeignKey(
        'investments.Investment', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='notifications'
    )
    
    # Status and priority
    is_read = models.BooleanField(default=False)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Delivery tracking
    email_sent = models.BooleanField(default=False)
    email_sent_at = models.DateTimeField(null=True, blank=True)
    push_sent = models.BooleanField(default=False)
    push_sent_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'notifications_notification'
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['notification_type']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.title}"
    
    def mark_as_read(self):
        """Mark notification as read."""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])
    
    @classmethod
    def create_notification(cls, user, notification_type, title, message, **kwargs):
        """Create a new notification for a user."""
        notification = cls.objects.create(
            user=user,
            notification_type=notification_type,
            title=title,
            message=message,
            **kwargs
        )
        
        # Send email if user has email notifications enabled
        if user.profile.email_notifications:
            notification.send_email()
        
        # Send push notification if user has push notifications enabled
        if user.profile.push_notifications:
            notification.send_push()
        
        return notification
    
    def send_email(self):
        """Send email notification."""
        # TODO: Implement email sending logic
        self.email_sent = True
        self.email_sent_at = timezone.now()
        self.save(update_fields=['email_sent', 'email_sent_at'])
    
    def send_push(self):
        """Send push notification."""
        # TODO: Implement push notification logic
        self.push_sent = True
        self.push_sent_at = timezone.now()
        self.save(update_fields=['push_sent', 'push_sent_at'])


class NotificationPreference(models.Model):
    """User notification preferences."""
    
    user = models.OneToOneField(
        'accounts.User', 
        on_delete=models.CASCADE, 
        related_name='notification_preferences'
    )
    
    # Email preferences
    email_new_investment = models.BooleanField(default=True)
    email_investment_completed = models.BooleanField(default=True)
    email_project_updates = models.BooleanField(default=True)
    email_new_messages = models.BooleanField(default=True)
    email_project_deadline = models.BooleanField(default=True)
    email_marketing = models.BooleanField(default=False)
    
    # Push notification preferences
    push_new_investment = models.BooleanField(default=True)
    push_investment_completed = models.BooleanField(default=True)
    push_project_updates = models.BooleanField(default=False)
    push_new_messages = models.BooleanField(default=True)
    push_project_deadline = models.BooleanField(default=True)
    
    # SMS preferences (if implemented)
    sms_enabled = models.BooleanField(default=False)
    sms_new_investment = models.BooleanField(default=False)
    sms_investment_completed = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'notifications_notificationpreference'
        verbose_name = 'Préférence de notification'
        verbose_name_plural = 'Préférences de notifications'
    
    def __str__(self):
        return f"Préférences de {self.user.get_full_name()}"