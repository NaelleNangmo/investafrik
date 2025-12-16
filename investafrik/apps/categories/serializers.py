"""
Serializers for categories app.
"""
from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""
    project_count = serializers.ReadOnlyField()
    total_funded_amount = serializers.ReadOnlyField()
    
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'description', 'icon_class',
            'color_hex', 'project_count', 'total_funded_amount',
            'order', 'created_at'
        ]


class CategoryListSerializer(serializers.ModelSerializer):
    """Simplified serializer for category lists."""
    project_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon_class', 'color_hex', 'project_count']