"""
Serializers for messaging app.
"""
from rest_framework import serializers
from .models import Conversation, Message
from apps.accounts.serializers import UserSerializer


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model."""
    sender = UserSerializer(read_only=True)
    is_image = serializers.SerializerMethodField()
    attachment_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = [
            'id', 'sender', 'content', 'message_type', 'attachment',
            'attachment_name', 'is_read', 'sent_at', 'is_image',
            'attachment_url'
        ]
        read_only_fields = ['id', 'sent_at', 'is_read']
    
    def get_is_image(self, obj):
        """Check if attachment is an image."""
        if obj.attachment:
            try:
                return obj.attachment.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))
            except:
                return False
        return False
    
    def get_attachment_url(self, obj):
        """Get attachment URL safely."""
        if obj.attachment:
            try:
                return obj.attachment.url
            except:
                return None
        return None


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for Conversation model."""
    participant_1 = UserSerializer(read_only=True)
    participant_2 = UserSerializer(read_only=True)
    other_participant = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = [
            'id', 'participant_1', 'participant_2', 'other_participant',
            'project', 'unread_count', 'last_message', 'last_message_at',
            'last_message_preview', 'created_at'
        ]
    
    def get_other_participant(self, obj):
        request = self.context.get('request')
        if request and request.user:
            other = obj.get_other_participant(request.user)
            return UserSerializer(other).data
        return None
    
    def get_unread_count(self, obj):
        request = self.context.get('request')
        if request and request.user:
            return obj.get_unread_count_for_user(request.user)
        return 0
    
    def get_last_message(self, obj):
        last_message = obj.messages.filter(is_deleted=False).last()
        if last_message:
            return MessageSerializer(last_message).data
        return None