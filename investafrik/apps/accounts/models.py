"""
User models for InvestAfrik platform.
"""
import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator


class UserManager(BaseUserManager):
    """Custom user manager for email-based authentication."""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user with an email and password."""
        if not email:
            raise ValueError('L\'adresse email est obligatoire')
        
        email = self.normalize_email(email)
        
        # Generate username from email if not provided
        if 'username' not in extra_fields:
            extra_fields['username'] = email.split('@')[0]
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with an email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 'porteur')
        extra_fields.setdefault('country', 'CM')
        extra_fields.setdefault('first_name', 'Admin')
        extra_fields.setdefault('last_name', 'User')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Le superuser doit avoir is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Le superuser doit avoir is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    """Custom User model extending Django's AbstractUser."""
    
    USER_TYPE_CHOICES = [
        ('porteur', 'Porteur de Projet'),
        ('investisseur', 'Investisseur'),
    ]
    
    AFRICAN_COUNTRIES = [
        ('CM', 'Cameroun'),
        ('SN', 'Sénégal'),
        ('CI', 'Côte d\'Ivoire'),
        ('BJ', 'Bénin'),
        ('TG', 'Togo'),
        ('BF', 'Burkina Faso'),
        ('ML', 'Mali'),
        ('NE', 'Niger'),
        ('GN', 'Guinée'),
        ('CD', 'RDC'),
        ('CG', 'Congo'),
        ('GA', 'Gabon'),
        ('TD', 'Tchad'),
        ('CF', 'RCA'),
        ('RW', 'Rwanda'),
        ('BI', 'Burundi'),
        ('KE', 'Kenya'),
        ('TZ', 'Tanzanie'),
        ('UG', 'Uganda'),
        ('NG', 'Nigeria'),
        ('GH', 'Ghana'),
        ('MG', 'Madagascar'),
        ('MU', 'Maurice'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Le numéro de téléphone doit être au format: '+999999999'. Jusqu'à 15 chiffres autorisés."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    country = models.CharField(max_length=2, choices=AFRICAN_COUNTRIES)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Additional fields for investors
    investment_interests = models.ManyToManyField(
        'categories.Category', 
        blank=True, 
        related_name='interested_investors'
    )
    available_budget = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Budget disponible en FCFA"
    )
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'user_type', 'country']
    
    class Meta:
        db_table = 'accounts_user'
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_user_type_display()})"
    
    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()
    
    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name
    
    @property
    def is_porteur(self):
        """Check if user is a project owner."""
        return self.user_type == 'porteur'
    
    @property
    def is_investisseur(self):
        """Check if user is an investor."""
        return self.user_type == 'investisseur'
    
    def get_country_display_name(self):
        """Get the full country name."""
        return dict(self.AFRICAN_COUNTRIES).get(self.country, self.country)


class UserProfile(models.Model):
    """Extended profile information for users."""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    website = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    company = models.CharField(max_length=100, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    experience_years = models.PositiveIntegerField(null=True, blank=True)
    
    # Notification preferences
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    push_notifications = models.BooleanField(default=True)
    
    # Privacy settings
    profile_visibility = models.CharField(
        max_length=20,
        choices=[
            ('public', 'Public'),
            ('investors_only', 'Investisseurs seulement'),
            ('private', 'Privé'),
        ],
        default='public'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'accounts_userprofile'
        verbose_name = 'Profil utilisateur'
        verbose_name_plural = 'Profils utilisateurs'
    
    def __str__(self):
        return f"Profil de {self.user.get_full_name()}"