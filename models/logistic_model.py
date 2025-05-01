import joblib
import numpy as np

class LogisticModel:
    def __init__(self):
        # Load the saved model components
        self.model = joblib.load('models/best_logistic_regression_model.pkl')
        self.scaler = joblib.load('models/scaler.pkl')
        self.label_encoder = joblib.load('models/label_encoder.pkl')
    
    def predict(self, input_data):
        """Make a prediction using the logistic regression model"""
        try:
            # Ensure input is in the correct format (2D array)
            if isinstance(input_data, list):
                input_data = np.array(input_data).reshape(1, -1)
            
            # Scale the input data
            input_scaled = self.scaler.transform(input_data)
            
            # Make prediction
            prediction = self.model.predict(input_scaled)
            
            # Convert encoded label back to original class name
            predicted_class = self.label_encoder.inverse_transform(prediction)
            
            return predicted_class[0], self.model.predict_proba(input_scaled).max() * 100
            
        except Exception as e:
            print(f"Prediction error: {str(e)}")
            return "Error", 0.0