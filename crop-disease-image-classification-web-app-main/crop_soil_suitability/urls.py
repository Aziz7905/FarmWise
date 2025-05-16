from django.urls import path
from .views import predict_crop_view

urlpatterns = [
    path('predict/', predict_crop_view, name='crop_soil_suitability'),
]
