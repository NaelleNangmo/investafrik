"""
Tests for models across all apps.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from decimal import Decimal
from datetime import date, timedelta

from apps.categories.models import Category
from apps.projects.models import Project
from apps.investments.models import Investment
from apps.messaging.models import Conversation, Message

User = get_user_model()


class UserModelTest(TestCase):
    """Test User model."""
    
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'user_type': 'porteur',
            'country': 'CM'
        }
    
    def test_create_user(self):
        """Test creating a user."""
        user = User.objects.create_user(
            password='testpass123',
            **self.user_data
        )
        
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.user_type, 'porteur')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_create_superuser(self):
        """Test creating a superuser."""
        user = User.objects.create_superuser(
            password='testpass123',
            **self.user_data
        )
        
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
    
    def test_user_str_representation(self):
        """Test user string representation."""
        user = User.objects.create_user(
            password='testpass123',
            **self.user_data
        )
        
        expected = "Test User (Porteur de Projet)"
        self.assertEqual(str(user), expected)
    
    def test_user_properties(self):
        """Test user properties."""
        porteur = User.objects.create_user(
            password='testpass123',
            user_type='porteur',
            **{k: v for k, v in self.user_data.items() if k != 'user_type'}
        )
        
        investisseur = User.objects.create_user(
            email='investor@example.com',
            username='investor',
            password='testpass123',
            first_name='Investor',
            last_name='User',
            user_type='investisseur',
            country='SN'
        )
        
        self.assertTrue(porteur.is_porteur)
        self.assertFalse(porteur.is_investisseur)
        
        self.assertFalse(investisseur.is_porteur)
        self.assertTrue(investisseur.is_investisseur)


class CategoryModelTest(TestCase):
    """Test Category model."""
    
    def test_create_category(self):
        """Test creating a category."""
        category = Category.objects.create(
            name='Test Category',
            description='Test description',
            icon_class='fas fa-test',
            color_hex='#FF0000'
        )
        
        self.assertEqual(category.name, 'Test Category')
        self.assertEqual(category.slug, 'test-category')
        self.assertTrue(category.is_active)
    
    def test_category_str_representation(self):
        """Test category string representation."""
        category = Category.objects.create(
            name='Agriculture',
            description='Test description',
            icon_class='fas fa-seedling',
            color_hex='#4CAF50'
        )
        
        self.assertEqual(str(category), 'Agriculture')


class ProjectModelTest(TestCase):
    """Test Project model."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='owner@example.com',
            username='owner',
            password='testpass123',
            first_name='Project',
            last_name='Owner',
            user_type='porteur',
            country='CM'
        )
        
        self.category = Category.objects.create(
            name='Technology',
            description='Tech projects',
            icon_class='fas fa-laptop',
            color_hex='#2196F3'
        )
    
    def test_create_project(self):
        """Test creating a project."""
        project = Project.objects.create(
            title='Test Project',
            short_description='A test project',
            full_description='<p>Full description</p>',
            owner=self.user,
            category=self.category,
            goal_amount=Decimal('1000000.00'),
            country='CM',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=60)
        )
        
        self.assertEqual(project.title, 'Test Project')
        self.assertEqual(project.slug, 'test-project')
        self.assertEqual(project.owner, self.user)
        self.assertEqual(project.status, 'draft')
    
    def test_project_properties(self):
        """Test project calculated properties."""
        project = Project.objects.create(
            title='Test Project',
            short_description='A test project',
            full_description='<p>Full description</p>',
            owner=self.user,
            category=self.category,
            goal_amount=Decimal('1000000.00'),
            current_amount=Decimal('250000.00'),
            country='CM',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            status='active'
        )
        
        self.assertEqual(project.funding_percentage, 25.0)
        self.assertEqual(project.days_remaining, 30)
        self.assertTrue(project.is_active)
        self.assertFalse(project.is_successful)
    
    def test_project_str_representation(self):
        """Test project string representation."""
        project = Project.objects.create(
            title='Amazing Project',
            short_description='A test project',
            full_description='<p>Full description</p>',
            owner=self.user,
            category=self.category,
            goal_amount=Decimal('1000000.00'),
            country='CM',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=60)
        )
        
        self.assertEqual(str(project), 'Amazing Project')


class InvestmentModelTest(TestCase):
    """Test Investment model."""
    
    def setUp(self):
        self.porteur = User.objects.create_user(
            email='porteur@example.com',
            username='porteur',
            password='testpass123',
            first_name='Project',
            last_name='Owner',
            user_type='porteur',
            country='CM'
        )
        
        self.investisseur = User.objects.create_user(
            email='investor@example.com',
            username='investor',
            password='testpass123',
            first_name='Investor',
            last_name='User',
            user_type='investisseur',
            country='SN'
        )
        
        self.category = Category.objects.create(
            name='Technology',
            description='Tech projects',
            icon_class='fas fa-laptop',
            color_hex='#2196F3'
        )
        
        self.project = Project.objects.create(
            title='Test Project',
            short_description='A test project',
            full_description='<p>Full description</p>',
            owner=self.porteur,
            category=self.category,
            goal_amount=Decimal('1000000.00'),
            country='CM',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=60),
            status='active'
        )
    
    def test_create_investment(self):
        """Test creating an investment."""
        investment = Investment.objects.create(
            investor=self.investisseur,
            project=self.project,
            amount=Decimal('50000.00'),
            payment_method='mobile_money',
            payment_status='completed'
        )
        
        self.assertEqual(investment.investor, self.investisseur)
        self.assertEqual(investment.project, self.project)
        self.assertEqual(investment.amount, Decimal('50000.00'))
        self.assertTrue(investment.is_successful)
        self.assertIsNotNone(investment.transaction_id)
    
    def test_investment_str_representation(self):
        """Test investment string representation."""
        investment = Investment.objects.create(
            investor=self.investisseur,
            project=self.project,
            amount=Decimal('50000.00'),
            payment_method='mobile_money'
        )
        
        expected = "Investor User - 50000.00 FCFA dans Test Project"
        self.assertEqual(str(investment), expected)


class ConversationModelTest(TestCase):
    """Test Conversation model."""
    
    def setUp(self):
        self.user1 = User.objects.create_user(
            email='user1@example.com',
            username='user1',
            password='testpass123',
            first_name='User',
            last_name='One',
            user_type='porteur',
            country='CM'
        )
        
        self.user2 = User.objects.create_user(
            email='user2@example.com',
            username='user2',
            password='testpass123',
            first_name='User',
            last_name='Two',
            user_type='investisseur',
            country='SN'
        )
    
    def test_create_conversation(self):
        """Test creating a conversation."""
        conversation = Conversation.objects.create(
            participant_1=self.user1,
            participant_2=self.user2
        )
        
        self.assertEqual(conversation.participant_1, self.user1)
        self.assertEqual(conversation.participant_2, self.user2)
        self.assertEqual(conversation.unread_count_p1, 0)
        self.assertEqual(conversation.unread_count_p2, 0)
    
    def test_get_other_participant(self):
        """Test getting other participant."""
        conversation = Conversation.objects.create(
            participant_1=self.user1,
            participant_2=self.user2
        )
        
        self.assertEqual(conversation.get_other_participant(self.user1), self.user2)
        self.assertEqual(conversation.get_other_participant(self.user2), self.user1)
    
    def test_get_or_create_conversation(self):
        """Test get or create conversation method."""
        # First call should create
        conv1, created1 = Conversation.get_or_create_conversation(self.user1, self.user2)
        self.assertTrue(created1)
        
        # Second call should return existing
        conv2, created2 = Conversation.get_or_create_conversation(self.user2, self.user1)
        self.assertFalse(created2)
        self.assertEqual(conv1, conv2)


class MessageModelTest(TestCase):
    """Test Message model."""
    
    def setUp(self):
        self.user1 = User.objects.create_user(
            email='user1@example.com',
            username='user1',
            password='testpass123',
            first_name='User',
            last_name='One',
            user_type='porteur',
            country='CM'
        )
        
        self.user2 = User.objects.create_user(
            email='user2@example.com',
            username='user2',
            password='testpass123',
            first_name='User',
            last_name='Two',
            user_type='investisseur',
            country='SN'
        )
        
        self.conversation = Conversation.objects.create(
            participant_1=self.user1,
            participant_2=self.user2
        )
    
    def test_create_message(self):
        """Test creating a message."""
        message = Message.objects.create(
            conversation=self.conversation,
            sender=self.user1,
            content='Hello, this is a test message!'
        )
        
        self.assertEqual(message.sender, self.user1)
        self.assertEqual(message.content, 'Hello, this is a test message!')
        self.assertFalse(message.is_read)
        self.assertEqual(message.message_type, 'text')
    
    def test_message_str_representation(self):
        """Test message string representation."""
        message = Message.objects.create(
            conversation=self.conversation,
            sender=self.user1,
            content='This is a long message that should be truncated in the string representation'
        )
        
        expected = "Message de User One - This is a long message that should be truncated in..."
        self.assertEqual(str(message), expected)