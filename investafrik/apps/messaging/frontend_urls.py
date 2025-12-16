"""
Frontend URLs for messaging app.
"""
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

app_name = 'messaging'

class ConversationsView(LoginRequiredMixin, TemplateView):
    template_name = 'messaging/conversations.html'

class ChatView(LoginRequiredMixin, TemplateView):
    template_name = 'messaging/chat.html'

urlpatterns = [
    path('conversations/', ConversationsView.as_view(), name='conversations'),
    path('chat/<uuid:conversation_id>/', ChatView.as_view(), name='chat'),
    path('new/', TemplateView.as_view(template_name='messaging/new_conversation.html'), name='new'),
]