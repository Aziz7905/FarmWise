from django.urls import path
from .views import detect_olive_view

urlpatterns = [
    path('detect/', detect_olive_view, name='detect_olive'),
]
