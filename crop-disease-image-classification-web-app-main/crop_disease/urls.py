"""
URL configuration for crop_disease project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')), 
    path('', include('prediction.urls')),
    

     # AI Model Apps
    path('', include('olive_fruit_detection.urls')),
    path('', include('Rainfall_forcasting.urls')),
    path('', include('crop_rotation_recommendation.urls')),
    path('', include('crop_soil_suitability.urls')),
    path('', include('olive_oil_quality.urls')),
    path('', include('olive_oil_price_forcating.urls')),
    path('', include('farm_yield_estimator.urls')),
    path('', include('soil_composition.urls')),
    path('', include('payments.urls')),

    

    

   
] 
# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
