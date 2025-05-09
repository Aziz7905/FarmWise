import os
import joblib
import pandas as pd
from django.conf import settings


class RainfallForecaster:
    def __init__(self, region):
        self.region = region
        self.model = None

        # Define the path to the models directory
        models_dir = os.path.dirname(__file__)

        # Define the region-to-model mapping
        region_to_model = {
            'Kebili': 'model_kebili.pkl',
            'Kasserine': 'model_kasserine.pkl',
            'Monastir': 'model_monastir.pkl',
            'Sidi Bouzid': 'model_sidi_bouzid.pkl',
            'Sousse': 'model_sousse.pkl'
        }

        # Check if the region exists in the mapping
        if region not in region_to_model:
            raise ValueError(f"Model not found for region: {region}")

        # Get the model filename for the region
        model_filename = region_to_model[region]
        model_path = os.path.join(models_dir, model_filename)

        try:
            # Load the model
            self.model = joblib.load(model_path)
            print(f"Model loaded successfully for region {region}")
            print("Model type:", type(self.model))  # This will help you debug if the model is loaded correctly

        except Exception as e:
            raise ValueError(f"Failed to load model for region {region}: {str(e)}")
        



    def predict_period(self, start_year, start_month, months=12):
        # Generate a list of future months starting from the provided start date
        start_date = pd.Timestamp(f"{start_year}-{start_month:02d}")
        future_dates = pd.date_range(start=start_date, periods=months, freq='MS')  # 'MS' gives the start of each month

        # The model likely expects a time-series index for prediction, so we need to predict based on a Datetime index
        features = pd.Series([1] * months, index=future_dates)  # Placeholder series to match the model input format

        # Use the model to make the forecast
        predictions = self.model.forecast(len(features))

        # Ensure no negative values (as seen in your training code)
        predictions[predictions < 0] = 0

        # Combine the future dates with the predictions into a DataFrame
        forecast_df = pd.DataFrame({
            'Date': future_dates,
            'Predicted Rainfall (mm)': predictions
        })
        
        return forecast_df


