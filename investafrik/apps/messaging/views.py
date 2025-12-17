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


# Frontend Views
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect


class ConversationsPageView(LoginRequiredMixin, TemplateView):
    """Page des conversations."""
    template_name = 'messaging/conversations.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Récupérer les conversations de l'utilisateur
        user = self.request.user
        conversations = Conversation.objects.filter(
            models.Q(participant_1=user) | models.Q(participant_2=user)
        ).select_related('participant_1', 'participant_2').order_by('-last_message_at')
        
        # Récupérer tous les utilisateurs pour démarrer de nouvelles conversations
        from apps.accounts.models import User
        all_users = User.objects.exclude(id=user.id).filter(is_active=True)
        
        # Compter les messages non lus
        unread_count = 0
        for conversation in conversations:
            unread_count += conversation.get_unread_count_for_user(user)
        
        # Conversation sélectionnée (si spécifiée dans l'URL)
        selected_conversation = None
        conversation_id = self.request.GET.get('conversation')
        if conversation_id:
            try:
                selected_conversation = conversations.get(id=conversation_id)
            except Conversation.DoesNotExist:
                pass
        
        # Messages de la conversation sélectionnée
        messages = []
        if selected_conversation:
            messages = selected_conversation.messages.filter(is_deleted=False).select_related('sender').order_by('sent_at')
        
        context.update({
            'conversations': conversations,
            'all_users': all_users,
            'unread_count': unread_count,
            'selected_conversation': selected_conversation,
            'messages': messages,
        })
        
        return context


class ConversationDetailView(LoginRequiredMixin, TemplateView):
    """Vue pour une conversation spécifique."""
    template_name = 'messaging/conversation_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        conversation_id = kwargs.get('conversation_id')
        user = self.request.user
        
        try:
            conversation = Conversation.objects.filter(
                models.Q(participant_1=user) | models.Q(participant_2=user)
            ).get(id=conversation_id)
            
            # Messages de la conversation
            messages = conversation.messages.filter(is_deleted=False).select_related('sender').order_by('sent_at')
            
            # Marquer comme lu
            conversation.mark_as_read_for_user(user)
            
            context.update({
                'conversation': conversation,
                'messages': messages,
                'other_user': conversation.participant_2 if conversation.participant_1 == user else conversation.participant_1,
            })
            
        except Conversation.DoesNotExist:
            context['error'] = 'Conversation non trouvée'
        
        return context
    
    def post(self, request, *args, **kwargs):
        """Envoyer un message."""
        conversation_id = kwargs.get('conversation_id')
        content = request.POST.get('content', '').strip()
        
        if not content:
            return redirect(f'/messaging/conversations/{conversation_id}/')
        
        try:
            conversation = Conversation.objects.filter(
                models.Q(participant_1=request.user) | models.Q(participant_2=request.user)
            ).get(id=conversation_id)
            
            # Créer le message
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content
            )
            
        except Conversation.DoesNotExist:
            pass
        
        return redirect(f'/messaging/conversations/{conversation_id}/')


class NewConversationView(LoginRequiredMixin, TemplateView):
    """Créer une nouvelle conversation."""
    
    def post(self, request, *args, **kwargs):
        """Créer une nouvelle conversation."""
        participant_2_id = request.POST.get('participant_2')
        
        if not participant_2_id:
            return redirect('/messaging/conversations/')
        
        try:
            from apps.accounts.models import User
            participant_2 = User.objects.get(id=participant_2_id)
            
            # Créer ou récupérer la conversation
            conversation, created = Conversation.get_or_create_conversation(
                request.user, participant_2
            )
            
            return redirect(f'/messaging/conversations/{conversation.id}/')
            
        except User.DoesNotExist:
            pass
        
        return redirect('/messaging/conversations/')