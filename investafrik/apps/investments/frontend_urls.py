"""
Frontend URLs for investments app.
"""
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

app_name = 'investments'

class MyInvestmentsView(LoginRequiredMixin, TemplateView):
    template_name = 'investments/my_investments.html'

urlpatterns = [
    path('my-investments/', MyInvestmentsView.as_view(), name='my_investments'),
]