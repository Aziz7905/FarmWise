from django.shortcuts import render
from .models.rainfall_forcaster import RainfallForecaster

def rainfall_forecast_view(request):
    if request.method == 'POST':
        region = request.POST.get('region')
        year = int(request.POST.get('year'))
        month = int(request.POST.get('month'))

        try:
            forecaster = RainfallForecaster(region)
            forecast_df = forecaster.predict_period(year, month, months=12)

            # Prepare the data for charting and table display
            forecast_data = forecast_df.to_dict(orient='records')
            forecast_dates = forecast_df['Date'].dt.strftime('%Y-%m-%d').tolist()
            predicted_rainfall = forecast_df['Predicted Rainfall (mm)'].tolist()

            return render(request, 'forecast.html', {
                'result_list': forecast_data,
                'region': region,
                'forecast_dates': forecast_dates,
                'predicted_rainfall': predicted_rainfall
            })

        except ValueError as e:
            # Catch region-related errors and provide a custom message
            return render(request, 'Rainfall_forcasting/forecast.html', {'error': str(e)})

        except Exception as e:
            # Catch other errors
            return render(request, 'Rainfall_forcasting/forecast.html', {'error': f"An error occurred: {str(e)}"})

    return render(request, 'Rainfall_forcasting/forecast.html')
