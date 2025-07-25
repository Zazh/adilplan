from django.urls import path
from .views import landing_detail, main_landing

urlpatterns = [
    path('', main_landing, name='main_landing'),
    path('landing/<slug:slug>/', landing_detail, name='landing_detail'), # /landing/abc/
]
