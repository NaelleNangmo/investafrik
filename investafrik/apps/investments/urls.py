"""
API URLs for investments app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.InvestmentViewSet, basename='investment')

urlpatterns = [
    path('my-investments/', views.MyInvestmentsView.as_view(), name='my_investments'),
    path('', include(router.urls)),
]