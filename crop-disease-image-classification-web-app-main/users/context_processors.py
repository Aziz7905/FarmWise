from payments.models import FarmerSubscription

def subscription_tier(request):
    if request.user.is_authenticated:
        try:
            return {
                'subscription_tier': request.user.farmerprofile.farmersubscription.plan.tier
            }
        except:
            return {'subscription_tier': 'FREE'}
    return {'subscription_tier': None}
  
  