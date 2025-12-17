"""
Frontend URLs for messaging app.
"""
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from . import views

app_name = 'messaging'

class ChatView(LoginRequiredMixin, TemplateView):
    template_name = 'messaging/chat.html'

urlpatterns = [
    path('conversations/', views.ConversationsPageView.as_view(), name='conversations'),
    path('conversations/<uuid:conversation_id>/', views.ConversationDetailView.as_view(), name='conversation_detail'),
    path('new/', views.NewConversationView.as_view(), name='new'),
    path('chat/<uuid:conversation_id>/', ChatView.as_view(), name='chat'),
]