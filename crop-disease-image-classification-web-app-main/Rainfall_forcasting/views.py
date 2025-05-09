from django.shortcuts import render
from .models.rainfall_forcaster import RainfallForecaster
import pandas as pd

def rainfall_forecast_view(request):
    if request.method == 'POST':
        region = request.POST.get('region')
        year = int(request.POST.get('year'))
        month = int(request.POST.get('month'))

        try:
            forecaster = RainfallForecaster(region)

            # Predict next 12 months
            predicted_values = forecaster.predict_period(year, month, months=12)

            # Generate proper date range starting from input year/month
            forecast_dates = pd.date_range(start=f"{year}-{month:02d}", periods=12, freq='MS')

            # If predict_period() returns just a Series/array, align it with the dates
            if not isinstance(predicted_values, pd.DataFrame):
                forecast_df = pd.DataFrame({
                    'Date': forecast_dates,
                    'Predicted Rainfall (mm)': predicted_values
                })
            else:
                # If it returns a DataFrame, ensure the Date column is set properly
                forecast_df = predicted_values.copy()
                forecast_df['Date'] = forecast_dates

            # Prepare data for template
            forecast_data = forecast_df.to_dict(orient='records')
            forecast_dates_list = forecast_df['Date'].dt.strftime('%B %Y').tolist()
            predicted_rainfall = forecast_df['Predicted Rainfall (mm)'].tolist()

            return render(request, 'Rainfall_forcasting/forecast.html', {
                'result_list': forecast_data,
                'region': region,
                'forecast_dates': forecast_dates_list,
                'predicted_rainfall': predicted_rainfall
            })

        except ValueError as e:
            return render(request, 'Rainfall_forcasting/forecast.html', {'error': str(e)})

        except Exception as e:
            return render(request, 'Rainfall_forcasting/forecast.html', {'error': f"An error occurred: {str(e)}"})

    return render(request, 'Rainfall_forcasting/forecast.html')
