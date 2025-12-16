"""
Serializers for investments app.
"""
from rest_framework import serializers
from .models import Investment, InvestmentReward
from apps.accounts.serializers import UserSerializer
from apps.projects.serializers import ProjectListSerializer


class InvestmentSerializer(serializers.ModelSerializer):
    """Serializer for Investment model."""
    investor = UserSerializer(read_only=True)
    project = ProjectListSerializer(read_only=True)
    is_successful = serializers.ReadOnlyField()
    can_be_refunded = serializers.ReadOnlyField()
    
    class Meta:
        model = Investment
        fields = [
            'id', 'investor', 'project', 'amount', 'message',
            'payment_method', 'payment_status', 'transaction_id',
            'payment_reference', 'payment_provider', 'invested_at',
            'payment_completed_at', 'is_successful', 'can_be_refunded'
        ]
        read_only_fields = [
            'id', 'transaction_id', 'invested_at', 'payment_completed_at'
        ]


class InvestmentRewardSerializer(serializers.ModelSerializer):
    """Serializer for InvestmentReward model."""
    is_available = serializers.ReadOnlyField()
    backers_count = serializers.ReadOnlyField()
    
    class Meta:
        model = InvestmentReward
        fields = [
            'id', 'title', 'description', 'minimum_amount',
            'estimated_delivery', 'is_limited', 'quantity_available',
            'quantity_claimed', 'is_available', 'backers_count'
        ]