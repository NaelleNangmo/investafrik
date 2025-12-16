"""
Messaging models for InvestAfrik platform.
"""
import uuid
from django.db import models
from django.utils import timezone


class Conversation(models.Model):
    """Conversation between two users."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participant_1 = models.ForeignKey(
        'accounts.User', 
        on_delete=models.CASCADE, 
        related_name='conversations_as_p1'
    )
    participant_2 = models.ForeignKey(
        'accounts.User', 
        on_delete=models.CASCADE, 
        related_name='conversations_as_p2'
    )
    
    # Related project (optional - conversations can be about specific projects)
    project = models.ForeignKey(
        'projects.Project', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='conversations'
    )
    
    # Unread message counts for each participant
    unread_count_p1 = models.PositiveIntegerField(default=0)
    unread_count_p2 = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Last message info (for quick display)
    last_message_at = models.DateTimeField(null=True, blank=True)
    last_message_preview = models.CharField(max_length=100, blank=True)
    
    class Meta:
        db_table = 'messaging_conversation'
        verbose_name = 'Conversation'
        verbose_name_plural = 'Conversations'
        unique_together = ('participant_1', 'participant_2')
        ordering = ['-last_message_at', '-updated_at']
    
    def __str__(self):
        return f"Conversation entre {self.participant_1.get_full_name()} et {self.participant_2.get_full_name()}"
    
    def get_other_participant(self, user):
        """Get the other participant in the conversation."""
        if user == self.participant_1:
            return self.participant_2
        return self.participant_1
    
    def get_unread_count_for_user(self, user):
        """Get unread message count for a specific user."""
        if user == self.participant_1:
            return self.unread_count_p1
        return self.unread_count_p2
    
    def mark_as_read_for_user(self, user):
        """Mark all messages as read for a specific user."""
        if user == self.participant_1:
            self.unread_count_p1 = 0
        else:
            self.unread_count_p2 = 0
        self.save(update_fields=['unread_count_p1', 'unread_count_p2'])
    
    def increment_unread_for_user(self, user):
        """Increment unread count for a specific user."""
        if user == self.participant_1:
            self.unread_count_p1 += 1
        else:
            self.unread_count_p2 += 1
        self.save(update_fields=['unread_count_p1', 'unread_count_p2'])
    
    @classmethod
    def get_or_create_conversation(cls, user1, user2, project=None):
        """Get existing conversation or create new one between two users."""
        # Ensure consistent ordering to avoid duplicates
        if user1.id > user2.id:
            user1, user2 = user2, user1
        
        conversation, created = cls.objects.get_or_create(
            participant_1=user1,
            participant_2=user2,
            defaults={'project': project}
        )
        return conversation, created


class Message(models.Model):
    """Individual message in a conversation."""
    
    MESSAGE_TYPE_CHOICES = [
        ('text', 'Texte'),
        ('image', 'Image'),
        ('file', 'Fichier'),
        ('system', 'Message système'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(
        Conversation, 
        on_delete=models.CASCADE, 
        related_name='messages'
    )
    sender = models.ForeignKey(
        'accounts.User', 
        on_delete=models.CASCADE, 
        related_name='sent_messages'
    )
    
    # Message content
    content = models.TextField()
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPE_CHOICES, default='text')
    
    # File attachment
    attachment = models.FileField(upload_to='messages/attachments/', blank=True, null=True)
    attachment_name = models.CharField(max_length=255, blank=True)
    attachment_size = models.PositiveIntegerField(null=True, blank=True)
    
    # Message status
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    
    # Timestamps
    sent_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'messaging_message'
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['sent_at']
    
    def __str__(self):
        return f"Message de {self.sender.get_full_name()} - {self.content[:50]}..."
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
            # Update conversation's last message info
            self.conversation.last_message_at = self.sent_at
            self.conversation.last_message_preview = self.content[:100]
            self.conversation.updated_at = timezone.now()
            
            # Increment unread count for the recipient
            recipient = self.conversation.get_other_participant(self.sender)
            self.conversation.increment_unread_for_user(recipient)
    
    def mark_as_read(self):
        """Mark message as read."""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])
    
    @property
    def is_image(self):
        """Check if message contains an image."""
        return self.message_type == 'image' or (
            self.attachment and 
            self.attachment.name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))
        )
    
    @property
    def attachment_url(self):
        """Get attachment URL if exists."""
        return self.attachment.url if self.attachment else None


class MessageReaction(models.Model):
    """Reactions to messages (like, love, etc.)."""
    
    REACTION_CHOICES = [
        ('like', '👍'),
        ('love', '❤️'),
        ('laugh', '😂'),
        ('wow', '😮'),
        ('sad', '😢'),
        ('angry', '😠'),
    ]
    
    message = models.ForeignKey(
        Message, 
        on_delete=models.CASCADE, 
        related_name='reactions'
    )
    user = models.ForeignKey(
        'accounts.User', 
        on_delete=models.CASCADE, 
        related_name='message_reactions'
    )
    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'messaging_messagereaction'
        verbose_name = 'Réaction au message'
        verbose_name_plural = 'Réactions aux messages'
        unique_together = ('message', 'user')
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_reaction_type_display()} sur message"