import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import SubscriptionPlan, FarmerSubscription

stripe.api_key = settings.STRIPE_SECRET_KEY
import logging
logger = logging.getLogger(__name__)



@login_required
def pricing(request):
    plans = SubscriptionPlan.objects.all()
    subscription = getattr(request.user.farmerprofile, 'farmersubscription', None)
    current_plan = subscription.plan.tier if subscription and subscription.active else None

    return render(request, 'payments/pricing.html', {
        'plans': plans,
        'current_plan': current_plan,
    })


@login_required
def create_checkout_session(request, plan_id):
    plan = get_object_or_404(SubscriptionPlan, id=plan_id)
    subscription = getattr(request.user.farmerprofile, 'farmersubscription', None)

    if subscription and subscription.plan == plan and subscription.active:
        messages.info(request, "You are already subscribed to this plan.")
        return redirect('pricing')

    customer = stripe.Customer.create(email=request.user.email)

    checkout_session = stripe.checkout.Session.create(
        customer=customer.id,
        payment_method_types=['card'],
        line_items=[{
            'price': plan.stripe_price_id,
            'quantity': 1,
        }],
        mode='subscription',
        success_url=request.build_absolute_uri('/dashboard/'),
        cancel_url=request.build_absolute_uri('/'),
    )

    FarmerSubscription.objects.update_or_create(
        farmer=request.user.farmerprofile,
        defaults={
            'plan': plan,
            'stripe_customer_id': customer.id,
            'stripe_subscription_id': checkout_session.subscription,
            'active': False
        }
    )

    return redirect(checkout_session.url, code=303)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    logger.info(f"Webhook called. Payload: {payload}")
    logger.info(f"Signature header: {sig_header}")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        logger.error(f"Invalid payload: {e}")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Invalid signature: {e}")
        return HttpResponse(status=400)

    logger.info(f"Webhook event type: {event['type']}")

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_id = session.get("customer")
        logger.info(f"Checkout complete. Customer ID: {customer_id}")
        subscription = FarmerSubscription.objects.filter(stripe_customer_id=customer_id).first()
        if subscription:
            subscription.active = True
            subscription.save()
            logger.info(f"Subscription activated for customer {customer_id}")

    return HttpResponse(status=200)

