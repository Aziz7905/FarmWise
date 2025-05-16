from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import FarmerProfile

@receiver(post_save, sender=User)
def create_farmer_profile(sender, instance, created, **kwargs):
    if created:
        FarmerProfile.objects.create(user=instance)
