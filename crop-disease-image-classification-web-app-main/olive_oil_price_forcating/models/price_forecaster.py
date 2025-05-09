import joblib
import pandas as pd

class OlivePriceForecaster:
    def __init__(self, model_path):
        self.model = joblib.load(model_path)

    def predict(self, ds, year, month, is_harvest_season, production, surplus,
                import_demand, market_tension, price_premium, global_price):
        
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
        
        forecast = self.model.predict(df)[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
        return forecast.to_dict(orient='records')[0]
