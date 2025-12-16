"""
Serializers for projects app.
"""
from rest_framework import serializers
from .models import Project, ProjectImage, ProjectUpdate, ProjectComment
from apps.categories.serializers import CategoryListSerializer
from apps.accounts.serializers import UserSerializer


class ProjectImageSerializer(serializers.ModelSerializer):
    """Serializer for ProjectImage model."""
    
    class Meta:
        model = ProjectImage
        fields = ['id', 'image', 'caption', 'order']


class ProjectListSerializer(serializers.ModelSerializer):
    """Simplified serializer for project lists."""
    owner = UserSerializer(read_only=True)
    category = CategoryListSerializer(read_only=True)
    funding_percentage = serializers.ReadOnlyField()
    days_remaining = serializers.ReadOnlyField()
    investor_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'short_description', 'owner',
            'category', 'goal_amount', 'current_amount', 'currency',
            'funding_percentage', 'days_remaining', 'investor_count',
            'featured_image', 'status', 'is_featured', 'created_at'
        ]


class ProjectSerializer(serializers.ModelSerializer):
    """Full serializer for Project model."""
    owner = UserSerializer(read_only=True)
    category = CategoryListSerializer(read_only=True)
    images = ProjectImageSerializer(many=True, read_only=True)
    funding_percentage = serializers.ReadOnlyField()
    days_remaining = serializers.ReadOnlyField()
    investor_count = serializers.ReadOnlyField()
    is_active = serializers.ReadOnlyField()
    is_successful = serializers.ReadOnlyField()
    
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'short_description', 'full_description',
            'owner', 'category', 'goal_amount', 'current_amount', 'currency',
            'country', 'start_date', 'end_date', 'status', 'is_featured',
            'featured_image', 'video_url', 'budget_breakdown', 'views_count',
            'funding_percentage', 'days_remaining', 'investor_count',
            'is_active', 'is_successful', 'images', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'slug', 'current_amount', 'views_count', 'created_at', 'updated_at']


class ProjectUpdateSerializer(serializers.ModelSerializer):
    """Serializer for ProjectUpdate model."""
    
    class Meta:
        model = ProjectUpdate
        fields = ['id', 'title', 'content', 'created_at']


class ProjectCommentSerializer(serializers.ModelSerializer):
    """Serializer for ProjectComment model."""
    user = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = ProjectComment
        fields = ['id', 'user', 'content', 'created_at', 'replies']
    
    def get_replies(self, obj):
        if obj.replies.exists():
            return ProjectCommentSerializer(obj.replies.all(), many=True).data
        return []