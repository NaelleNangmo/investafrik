"""
Management command to create a superuser with proper user_type.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Create a superuser with proper user_type'
    
    def add_arguments(self, parser):
        parser.add_argument('--email', required=True, help='Email address')
        parser.add_argument('--username', required=True, help='Username')
        parser.add_argument('--password', required=True, help='Password')
        parser.add_argument('--first_name', required=True, help='First name')
        parser.add_argument('--last_name', required=True, help='Last name')
        parser.add_argument('--country', default='CM', help='Country code (default: CM)')
    
    def handle(self, *args, **options):
        if User.objects.filter(email=options['email']).exists():
            self.stdout.write(
                self.style.ERROR(f'User with email {options["email"]} already exists')
            )
            return
        
        user = User.objects.create_superuser(
            email=options['email'],
            username=options['username'],
            password=options['password'],
            first_name=options['first_name'],
            last_name=options['last_name'],
            user_type='porteur',  # Default to porteur for admin
            country=options['country']
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'Superuser {user.email} created successfully!')
        )