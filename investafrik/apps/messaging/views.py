"""
API views for messaging app.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import models
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for conversations."""
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(
            models.Q(participant_1=user) | models.Q(participant_2=user)
        ).order_by('-last_message_at')
    
    def create(self, request, *args, **kwargs):
        """Create a new conversation."""
        from apps.accounts.models import User
        
        participant_2_id = request.data.get('participant_2')
        if not participant_2_id:
            return Response(
                {'error': 'participant_2 est requis'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            participant_2 = User.objects.get(id=participant_2_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'Utilisateur non trouvé'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        if participant_2 == request.user:
            return Response(
                {'error': 'Vous ne pouvez pas créer une conversation avec vous-même'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Créer ou récupérer la conversation
        try:
            conversation, created = Conversation.get_or_create_conversation(
                request.user, participant_2
            )
            
            serializer = self.get_serializer(conversation, context={'request': request})
            status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
            return Response(serializer.data, status=status_code)
            
        except Exception as e:
            return Response(
                {'error': f'Erreur lors de la création de la conversation: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """Get messages in a conversation."""
        conversation = self.get_object()
        messages = conversation.messages.filter(is_deleted=False)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        """Send a message in a conversation."""
        conversation = self.get_object()
        content = request.data.get('content', '').strip()
        
        if not content:
            return Response(
                {'error': 'Le message ne peut pas être vide'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=content
        )
        
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark conversation as read."""
        conversation = self.get_object()
        conversation.mark_as_read_for_user(request.user)
        return Response({'message': 'Conversation marquée comme lue'})