"""
API URLs for notifications app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.NotificationViewSet, basename='notification')

urlpatterns = [
    path('mark-all-read/', views.MarkAllReadView.as_view(), name='mark_all_read'),
    path('', include(router.urls)),
]