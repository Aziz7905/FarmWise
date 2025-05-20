import joblib
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

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
            
            result = forecast.to_dict(orient='records')[0]
            result['is_harvest_season'] = is_harvest_season  
            return result
    def plot_forecast(self, forecast_df, title="Olive Oil Forecast"):
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(forecast_df['ds'], forecast_df['yhat'], label='Forecast')
        ax.fill_between(forecast_df['ds'], forecast_df['yhat_lower'], forecast_df['yhat_upper'], color='blue', alpha=0.2, label='95% CI')
        ax.set_title(title)
        ax.set_xlabel("Date")
        ax.set_ylabel("Price (TND/L)")
        ax.legend()

        # Save plot to base64-encoded PNG
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        return image_base64