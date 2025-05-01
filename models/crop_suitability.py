import joblib
import numpy as np
import os
from pathlib import Path

class CropSuitabilityModel:
    def __init__(self):
        # Initialize paths to model files
        self.model_path =  'assets/best_logistic_regression_model.pkl'
        self.scaler_path = 'assets/scaler.pkl'
        self.encoder_path = 'assets/label_encoder.pkl'
        
        # Load models
        self.model = None
        self.scaler = None
        self.label_encoder = None
        
        self.load_models()
    
    def load_models(self):
        """Load the trained model, scaler, and label encoder"""
        try:
            self.model = joblib.load(self.model_path)
            self.scaler = joblib.load(self.scaler_path)
            self.label_encoder = joblib.load(self.encoder_path)
        except Exception as e:
            raise RuntimeError(f"Failed to load model files: {str(e)}")
    
    def predict(self, input_data):
        """
        Predict suitable crops based on input parameters
        
        Args:
            input_data: Dictionary containing the following keys:
                - 'N': Nitrogen value (ppm)
                - 'P': Phosphorus value (ppm)
                - 'K': Potassium value (ppm)
                - 'temperature': Temperature (°C)
                - 'humidity': Humidity (%)
                - 'ph': Soil pH
                - 'rainfall': Rainfall (mm)
        
        Returns:
            Dictionary of crops with their probability scores (sorted by score)
        """
        if not all(key in input_data for key in ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']):
            raise ValueError("Input data must contain all required parameters")
        
        try:
            # Convert input to numpy array in correct order
            input_array = np.array([
                [
                    input_data['N'],
                    input_data['P'],
                    input_data['K'],
                    input_data['temperature'],
                    input_data['humidity'],
                    input_data['ph'],
                    input_data['rainfall']
                ]
            ])
            
            # Scale the input data
            scaled_input = self.scaler.transform(input_array)
            
            # Get prediction probabilities
            probabilities = self.model.predict_proba(scaled_input)[0]
            
            # Get all class labels
            class_labels = self.label_encoder.classes_
            
            # Create dictionary of crops with their probabilities
            results = {label: prob * 100 for label, prob in zip(class_labels, probabilities)}
            
            # Sort by probability (descending)
            sorted_results = dict(sorted(results.items(), key=lambda item: item[1], reverse=True))
            
            return sorted_results
            
        except Exception as e:
            raise RuntimeError(f"Prediction failed: {str(e)}")

def load_suitability_model():
    """Factory function to load and return the suitability model"""
    return CropSuitabilityModel()