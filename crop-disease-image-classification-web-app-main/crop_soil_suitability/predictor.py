import joblib
import numpy as np

class CropSuitabilityModel:
    def __init__(self):
        self.model_path = 'crop_soil_suitability/best_logistic_regression_model.pkl'
        self.scaler_path = 'crop_soil_suitability/scaler.pkl'
        self.encoder_path = 'crop_soil_suitability/label_encoder.pkl'

        self.model = joblib.load(self.model_path)
        self.scaler = joblib.load(self.scaler_path)
        self.label_encoder = joblib.load(self.encoder_path)

    def predict(self, input_data):
        if not all(k in input_data for k in ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']):
            raise ValueError("Missing one or more required input keys")

        input_array = np.array([[
            input_data['N'], input_data['P'], input_data['K'],
            input_data['temperature'], input_data['humidity'],
            input_data['ph'], input_data['rainfall']
        ]])
        scaled_input = self.scaler.transform(input_array)
        probabilities = self.model.predict_proba(scaled_input)[0]
        class_labels = self.label_encoder.classes_
        results = {label: prob * 100 for label, prob in zip(class_labels, probabilities)}
        return dict(sorted(results.items(), key=lambda x: x[1], reverse=True))

def load_suitability_model():
    return CropSuitabilityModel()
