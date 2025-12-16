"""
Investment models for InvestAfrik platform.
"""
import uuid
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone


class Investment(models.Model):
    """Investment model for tracking user investments in projects."""
    
    PAYMENT_METHOD_CHOICES = [
        ('mobile_money', 'Mobile Money'),
        ('bank_transfer', 'Virement bancaire'),
        ('card', 'Carte bancaire'),
        ('cash', 'Espèces'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('processing', 'En cours de traitement'),
        ('completed', 'Complété'),
        ('failed', 'Échec'),
        ('cancelled', 'Annulé'),
        ('refunded', 'Remboursé'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    investor = models.ForeignKey(
        'accounts.User', 
        on_delete=models.CASCADE, 
        related_name='investments'
    )
    project = models.ForeignKey(
        'projects.Project', 
        on_delete=models.CASCADE, 
        related_name='investments'
    )
    amount = models.DecimalField(
        max_digits=15, 
        decimal_places=2,
        validators=[MinValueValidator(1000)],  # Minimum 1000 FCFA
        help_text="Montant de l'investissement en FCFA"
    )
    message = models.TextField(
        blank=True, 
        help_text="Message optionnel pour le porteur de projet"
    )
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(
        max_length=20, 
        choices=PAYMENT_STATUS_CHOICES, 
        default='pending'
    )
    transaction_id = models.CharField(max_length=100, unique=True, blank=True)
    
    # Additional payment information
    payment_reference = models.CharField(max_length=100, blank=True)
    payment_provider = models.CharField(max_length=50, blank=True)
    
    # Timestamps
    invested_at = models.DateTimeField(auto_now_add=True)
    payment_completed_at = models.DateTimeField(null=True, blank=True)
    refunded_at = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    class Meta:
        db_table = 'investments_investment'
        verbose_name = 'Investissement'
        verbose_name_plural = 'Investissements'
        ordering = ['-invested_at']
    
    def __str__(self):
        return f"{self.investor.get_full_name()} - {self.amount} FCFA dans {self.project.title}"
    
    def save(self, *args, **kwargs):
        # Generate transaction ID if not provided
        if not self.transaction_id:
            self.transaction_id = f"INV-{uuid.uuid4().hex[:12].upper()}"
        
        # Set payment completed timestamp
        if self.payment_status == 'completed' and not self.payment_completed_at:
            self.payment_completed_at = timezone.now()
        
        # Set refunded timestamp
        if self.payment_status == 'refunded' and not self.refunded_at:
            self.refunded_at = timezone.now()
        
        super().save(*args, **kwargs)
        
        # Update project current amount if payment is completed
        if self.payment_status == 'completed':
            self.project.update_current_amount()
    
    @property
    def is_successful(self):
        """Check if investment was successful."""
        return self.payment_status == 'completed'
    
    @property
    def can_be_refunded(self):
        """Check if investment can be refunded."""
        return (
            self.payment_status == 'completed' and 
            self.project.status in ['failed', 'cancelled'] and
            not self.refunded_at
        )


class InvestmentReward(models.Model):
    """Rewards/perks offered to investors at different investment levels."""
    
    project = models.ForeignKey(
        'projects.Project', 
        on_delete=models.CASCADE, 
        related_name='rewards'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    minimum_amount = models.DecimalField(
        max_digits=15, 
        decimal_places=2,
        validators=[MinValueValidator(1000)]
    )
    estimated_delivery = models.DateField(null=True, blank=True)
    is_limited = models.BooleanField(default=False)
    quantity_available = models.PositiveIntegerField(null=True, blank=True)
    quantity_claimed = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'investments_investmentreward'
        verbose_name = 'Récompense d\'investissement'
        verbose_name_plural = 'Récompenses d\'investissement'
        ordering = ['minimum_amount']
    
    def __str__(self):
        return f"{self.project.title} - {self.title} ({self.minimum_amount} FCFA)"
    
    @property
    def is_available(self):
        """Check if reward is still available."""
        if not self.is_active:
            return False
        if self.is_limited and self.quantity_available:
            return self.quantity_claimed < self.quantity_available
        return True
    
    @property
    def backers_count(self):
        """Get number of backers who chose this reward."""
        return self.chosen_by.filter(payment_status='completed').count()


class InvestmentRewardChoice(models.Model):
    """Track which reward an investor chose."""
    
    investment = models.OneToOneField(
        Investment, 
        on_delete=models.CASCADE, 
        related_name='reward_choice'
    )
    reward = models.ForeignKey(
        InvestmentReward, 
        on_delete=models.CASCADE, 
        related_name='chosen_by'
    )
    delivery_address = models.TextField(blank=True)
    delivery_notes = models.TextField(blank=True)
    is_delivered = models.BooleanField(default=False)
    delivered_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'investments_investmentrewardchoice'
        verbose_name = 'Choix de récompense'
        verbose_name_plural = 'Choix de récompenses'
    
    def __str__(self):
        return f"{self.investment.investor.get_full_name()} - {self.reward.title}"