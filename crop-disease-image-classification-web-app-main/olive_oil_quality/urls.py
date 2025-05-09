from django.urls import path
from .views import analyse_view

urlpatterns = [
    path('analyse/', analyse_view, name='analyse_olive_quality'),
]
