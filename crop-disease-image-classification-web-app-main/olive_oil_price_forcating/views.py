import os
from datetime import datetime
from django.conf import settings
from django.shortcuts import render
from .models.price_forecaster import OlivePriceForecaster

MODEL_PATH = os.path.join(settings.BASE_DIR, 'olive_oil_price_forcating', 'olive_oil_price_model.pkl')
forecaster = OlivePriceForecaster(MODEL_PATH)

def forecast_price_view(request):
    context = {
        'field_labels': [
            ('production', 'Production'),
            ('surplus', 'Surplus'),
            ('import_demand', 'Import Demand'),
            ('market_tension', 'Market Tension'),
            ('price_premium', 'Price Premium'),
            ('global_price', 'Global Price'),
        ]
    }
    

    if request.method == 'POST':
        try:
            ds = request.POST['ds']
            date_obj = datetime.strptime(ds, '%Y-%m-%d')
            year = date_obj.year
            month = date_obj.month

            prediction = forecaster.predict(
                ds=ds,
                year=year,
                month=month,
                is_harvest_season=int(request.POST['is_harvest_season']),
                production=float(request.POST['production']),
                surplus=float(request.POST['surplus']),
                import_demand=float(request.POST['import_demand']),
                market_tension=float(request.POST['market_tension']),
                price_premium=float(request.POST['price_premium']),
                global_price=float(request.POST['global_price']),
            )

            prediction['is_harvest_season_display'] = 'Yes' if prediction['is_harvest_season'] else 'No'
            context['result'] = prediction
            context['forecast_plot'] = prediction['plot']
        except Exception as e:
            context['error'] = str(e)

    return render(request, 'olive_oil_price_forcating/forecast.html', context)

