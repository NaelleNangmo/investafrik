"""
Frontend URLs for investments app.
"""
from django.urls import path
from . import views

app_name = 'investments'

urlpatterns = [
    path('my-investments/', views.MyInvestmentsPageView.as_view(), name='my_investments'),
]