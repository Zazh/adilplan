from django.urls import path
from .views import FeedbackCreateView
from django.views.generic import TemplateView

urlpatterns = [
    path('', FeedbackCreateView.as_view(), name='feedback'),
    path('success/', TemplateView.as_view(template_name='feedback/success.html'), name='feedback-success'),
]
