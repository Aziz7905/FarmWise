from django.shortcuts import render
from django.conf import settings
import pandas as pd
from Rainfall_forcasting.models.kasserine import KasserineRainfallModel
from Rainfall_forcasting.models.kebili import KebiliRainfallModel
from Rainfall_forcasting.models.monastir import MonastirRainfallModel
from Rainfall_forcasting.models.sidi_bouzid import SidiBouzidRainfallModel
from Rainfall_forcasting.models.sousse import SousseRainfallModel

models_map = {
    'kasserine': KasserineRainfallModel(),
    'kebili': KebiliRainfallModel(),
    'monastir': MonastirRainfallModel(),
    'sidi_bouzid': SidiBouzidRainfallModel(),
    'sousse': SousseRainfallModel(),
}

def rainfall_forecast_view(request):
    context = {}
    if request.method == 'POST':
        station = request.POST.get('region')
        try:
            model = models_map.get(station.lower().replace(" ", "_"))
            if not model:
                raise ValueError("Invalid station name.")

            last_date = pd.to_datetime("2023-12-01")
            future_dates = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=36, freq='MS')
            forecast = model.forecast(36)

            forecast_df = pd.DataFrame({
                'Date': future_dates,
                'Forecast': forecast,
                'Station': station
            })

            context['forecast_data'] = forecast_df.to_dict(orient='records')
            context['dates'] = forecast_df['Date'].dt.strftime('%Y-%m-%d').tolist()
            context['values'] = forecast_df['Forecast'].tolist()
            context['region'] = station

        except Exception as e:
            context['error'] = str(e)

    return render(request, 'Rainfall_forcasting/forecast.html', context)
