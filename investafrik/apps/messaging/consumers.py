"""
WebSocket consumers for real-time messaging.
"""
import json
import uuid
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import Conversation, Message


class ChatConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for chat functionality."""
    
    async def connect(self):
        """Handle WebSocket connection."""
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'chat_{self.conversation_id}'
        
        # Check if user is authenticated
        if self.scope['user'] == AnonymousUser():
            await self.close()
            return
        
        # Check if user is participant in this conversation
        if not await self.is_participant():
            await self.close()
            return
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        """Handle received WebSocket message."""
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type', 'chat_message')
            
            if message_type == 'chat_message':
                await self.handle_chat_message(text_data_json)
            elif message_type == 'typing':
                await self.handle_typing(text_data_json)
            elif message_type == 'mark_read':
                await self.handle_mark_read(text_data_json)
                
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'error': 'Invalid JSON'
            }))
    
    async def handle_chat_message(self, data):
        """Handle chat message."""
        content = data.get('message', '').strip()
        if not content:
            return
        
        # Save message to database
        message = await self.save_message(content)
        if not message:
            return
        
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': {
                    'id': str(message.id),
                    'content': message.content,
                    'sender': {
                        'id': str(message.sender.id),
                        'name': message.sender.get_full_name(),
                        'avatar': message.sender.profile_picture.url if message.sender.profile_picture else None,
                    },
                    'sent_at': message.sent_at.isoformat(),
                    'is_read': message.is_read,
                }
            }
        )
    
    async def handle_typing(self, data):
        """Handle typing indicator."""
        is_typing = data.get('is_typing', False)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'typing_indicator',
                'user_id': str(self.scope['user'].id),
                'user_name': self.scope['user'].get_full_name(),
                'is_typing': is_typing,
            }
        )
    
    async def handle_mark_read(self, data):
        """Handle mark messages as read."""
        await self.mark_conversation_as_read()
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'messages_read',
                'user_id': str(self.scope['user'].id),
            }
        )
    
    async def chat_message(self, event):
        """Send chat message to WebSocket."""
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message']
        }))
    
    async def typing_indicator(self, event):
        """Send typing indicator to WebSocket."""
        # Don't send typing indicator to the sender
        if event['user_id'] != str(self.scope['user'].id):
            await self.send(text_data=json.dumps({
                'type': 'typing_indicator',
                'user_id': event['user_id'],
                'user_name': event['user_name'],
                'is_typing': event['is_typing'],
            }))
    
    async def messages_read(self, event):
        """Send messages read status to WebSocket."""
        await self.send(text_data=json.dumps({
            'type': 'messages_read',
            'user_id': event['user_id'],
        }))
    
    @database_sync_to_async
    def is_participant(self):
        """Check if current user is participant in conversation."""
        try:
            conversation = Conversation.objects.get(id=self.conversation_id)
            return (
                conversation.participant_1 == self.scope['user'] or 
                conversation.participant_2 == self.scope['user']
            )
        except Conversation.DoesNotExist:
            return False
    
    @database_sync_to_async
    def save_message(self, content):
        """Save message to database."""
        try:
            conversation = Conversation.objects.get(id=self.conversation_id)
            message = Message.objects.create(
                conversation=conversation,
                sender=self.scope['user'],
                content=content
            )
            return message
        except Conversation.DoesNotExist:
            return None
    
    @database_sync_to_async
    def mark_conversation_as_read(self):
        """Mark conversation as read for current user."""
        try:
            conversation = Conversation.objects.get(id=self.conversation_id)
            conversation.mark_as_read_for_user(self.scope['user'])
        except Conversation.DoesNotExist:
            pass


class NotificationConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for real-time notifications."""
    
    async def connect(self):
        """Handle WebSocket connection."""
        # Check if user is authenticated
        if self.scope['user'] == AnonymousUser():
            await self.close()
            return
        
        self.user_group_name = f'notifications_{self.scope["user"].id}'
        
        # Join user's notification group
        await self.channel_layer.group_add(
            self.user_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        # Leave user's notification group
        if hasattr(self, 'user_group_name'):
            await self.channel_layer.group_discard(
                self.user_group_name,
                self.channel_name
            )
    
    async def receive(self, text_data):
        """Handle received WebSocket message."""
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type')
            
            if message_type == 'mark_notification_read':
                notification_id = text_data_json.get('notification_id')
                await self.mark_notification_read(notification_id)
                
        except json.JSONDecodeError:
            pass
    
    async def notification_message(self, event):
        """Send notification to WebSocket."""
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'notification': event['notification']
        }))
    
    @database_sync_to_async
    def mark_notification_read(self, notification_id):
        """Mark notification as read."""
        try:
            from apps.notifications.models import Notification
            notification = Notification.objects.get(
                id=notification_id, 
                user=self.scope['user']
            )
            notification.mark_as_read()
        except Notification.DoesNotExist:
            pass