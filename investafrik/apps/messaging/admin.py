"""
Admin configuration for messaging app.
"""
from django.contrib import admin
from .models import Conversation, Message, MessageReaction


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    """Admin for Conversation model."""
    list_display = [
        'participant_1', 'participant_2', 'project',
        'last_message_at', 'created_at'
    ]
    list_filter = ['created_at', 'last_message_at']
    search_fields = [
        'participant_1__email', 'participant_2__email',
        'project__title'
    ]
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Admin for Message model."""
    list_display = [
        'sender', 'conversation', 'message_type',
        'is_read', 'sent_at'
    ]
    list_filter = ['message_type', 'is_read', 'sent_at']
    search_fields = ['sender__email', 'content']
    readonly_fields = ['sent_at']


@admin.register(MessageReaction)
class MessageReactionAdmin(admin.ModelAdmin):
    """Admin for MessageReaction model."""
    list_display = ['user', 'message', 'reaction_type', 'created_at']
    list_filter = ['reaction_type', 'created_at']