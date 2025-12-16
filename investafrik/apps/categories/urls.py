"""
API URLs for categories app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
]