import os
from django.conf import settings
from django.shortcuts import render
from .models.price_forecaster import OlivePriceForecaster 

MODEL_PATH = os.path.join(settings.BASE_DIR, 'olive_oil_price_forcating', 'olive_oil_price_model.pkl')
forecaster = OlivePriceForecaster(MODEL_PATH)

def forecast_price_view(request):
    context = {}
    if request.method == 'POST':
        try:
            prediction = forecaster.predict(
                ds=request.POST['ds'],
                year=int(request.POST['year']),
                month=int(request.POST['month']),
                is_harvest_season=int(request.POST['is_harvest_season']),
                production=float(request.POST['production']),
                surplus=float(request.POST['surplus']),
                import_demand=float(request.POST['import_demand']),
                market_tension=float(request.POST['market_tension']),
                price_premium=float(request.POST['price_premium']),
                global_price=float(request.POST['global_price']),
            )
            context['result'] = prediction
        except Exception as e:
            context['error'] = str(e)
    return render(request, 'olive_oil_price_forcating/forecast.html', context)
