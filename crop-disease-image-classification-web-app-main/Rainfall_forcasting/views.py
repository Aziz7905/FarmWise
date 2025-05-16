import os
import pandas as pd
from django.shortcuts import render
from django.conf import settings
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
    crops_path = os.path.join(settings.BASE_DIR, 'Rainfall_forcasting',  'crop_parameters_clean.csv')
    crop_df = pd.read_csv(crops_path)
    crop_names = crop_df['Crop'].tolist()
    context['crops'] = crop_names

    if request.method == 'POST':
        region = request.POST.get('region')
        crop_name = request.POST.get('crop')
        start_month = request.POST.get('start_date')
        end_month = request.POST.get('end_date')

        try:
            model = models_map.get(region.lower().replace(" ", "_"))
            if not model:
                raise ValueError("Invalid station name.")

            # Predict far into the future until 2030
            last_date = pd.to_datetime("2023-12-01")
            future_dates = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=84, freq='MS')
            forecast = model.forecast(len(future_dates))

            forecast_df = pd.DataFrame({
                'Date': future_dates,
                'Forecast': forecast,
                'Station': region
            })

            # Filter by date range if provided
            if start_month and end_month:
                start_date = pd.to_datetime(start_month + "-01")
                end_date = pd.to_datetime(end_month + "-01") + pd.offsets.MonthEnd(0)
                forecast_df = forecast_df[(forecast_df['Date'] >= start_date) & (forecast_df['Date'] <= end_date)]

            # Get crop parameters and calculate ETc
            crop_row = crop_df[crop_df['Crop'] == crop_name].iloc[0]
            r_avg = (crop_row['Ropt_min'] + crop_row['Ropt_max']) / 2
            duration_avg = (crop_row['Duration_min'] + crop_row['Duration_max']) / 2
            etc = (r_avg / duration_avg) * 30

            forecast_df['ETc'] = etc
            forecast_df['Deficit'] = forecast_df['ETc'] - forecast_df['Forecast']

            context['region'] = region
            context['crop'] = crop_name
            context['forecast_data'] = forecast_df.to_dict(orient='records')
            context['dates'] = forecast_df['Date'].dt.strftime('%Y-%m-%d').tolist()
            context['forecast'] = forecast_df['Forecast'].tolist()
            context['deficit'] = forecast_df['Deficit'].tolist()
            context['etc'] = etc

        except Exception as e:
            context['error'] = str(e)

    return render(request, 'Rainfall_forcasting/forecast.html', context)
