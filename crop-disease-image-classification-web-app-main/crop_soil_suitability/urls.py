from django.urls import path
from .views import suitability_view

urlpatterns = [
    path('suitability/', suitability_view, name='crop_soil_suitability'),
]
