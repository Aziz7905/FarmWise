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
        if not self.model:
            raise ValueError("Model is not loaded. Cannot make predictions.")

    # Constructing start_date to align with model expectations
        start_date = pd.Timestamp(f"{start_year}-{start_month:02d}-01")
    
    # Create a time range from the start_date
        dates = pd.date_range(start=start_date, periods=months, freq='MS')

    # Prepare the features in the correct format (if the model expects year and month)
        features = [[d.year, d.month] for d in dates]

        try:
            predictions = self.model.predict(features)
        except Exception as e:
            raise ValueError(f"Error during prediction: {str(e)}")

        df = pd.DataFrame({
            "Date": dates,
            "Predicted Rainfall (mm)": predictions
        })
        return df


