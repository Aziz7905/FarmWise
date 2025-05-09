import pandas as pd
import joblib
import os
from django.shortcuts import render
from django.conf import settings

MODEL_PATH = os.path.join(settings.BASE_DIR, 'olive_oil_price_forcating', 'olive_oil_price_model.pkl')
model = joblib.load(MODEL_PATH)

def forecast_price_view(request):
    context = {}
    if request.method == 'POST':
        try:
            # Extract form inputs
            ds = request.POST['ds']
            year = int(request.POST['year'])
            month = int(request.POST['month'])
            is_harvest_season = int(request.POST['is_harvest_season'])
            production = float(request.POST['production'])
            surplus = float(request.POST['surplus'])
            import_demand = float(request.POST['import_demand'])
            market_tension = float(request.POST['market_tension'])
            price_premium = float(request.POST['price_premium'])
            global_price = float(request.POST['global_price'])

            # Create DataFrame for prediction
            df = pd.DataFrame([{
                'ds': ds,
                'year': year,
                'month': month,
                'is_harvest_season': is_harvest_season,
                'production': production,
                'surplus': surplus,
                'import_demand': import_demand,
                'market_tension': market_tension,
                'price_premium': price_premium,
                'global_price': global_price,
            }])

            forecast = model.predict(df)[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
            context['result'] = forecast.to_dict(orient='records')[0]

        except Exception as e:
            context['error'] = str(e)
    return render(request, 'olive_oil_price_forcating/forecast.html', context)
