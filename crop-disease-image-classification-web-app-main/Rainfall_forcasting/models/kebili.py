import os
import joblib
import pandas as pd
from django.conf import settings

class KebiliRainfallModel:
    def __init__(self):
        path = os.path.join(settings.BASE_DIR, 'Rainfall_forcasting','models', 'model_kebili.pkl')
        self.model = joblib.load(path)

    def forecast(self, months=36):
        forecast = self.model.forecast(months)
        forecast[forecast < 0] = 0
        return forecast
