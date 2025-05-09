# prediction/urls.py
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path('home/', views.upload_image, name='home'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
