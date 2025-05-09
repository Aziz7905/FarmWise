from django.urls import path
from .views import yield_estimation_view

urlpatterns = [
    path('estimate/', yield_estimation_view, name='yield_estimate'),
]
