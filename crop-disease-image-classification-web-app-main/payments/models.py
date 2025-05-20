from django.db import models
from users.models import FarmerProfile
from .enum import SubscriptionTier

class SubscriptionPlan(models.Model):
    tier = models.CharField(max_length=10, choices=SubscriptionTier.choices(), unique=True)
    stripe_price_id = models.CharField(max_length=100)

    def __str__(self):
        return self.get_tier_display()


class FarmerSubscription(models.Model):
    farmer = models.OneToOneField(FarmerProfile, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    stripe_customer_id = models.CharField(max_length=100)
    stripe_subscription_id = models.CharField(max_length=100, null=True, blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.farmer.user.username} - {self.plan}'
