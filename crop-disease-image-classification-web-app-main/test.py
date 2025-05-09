import pickle
import os

import joblib

# Absolute path construction (adjust BASE_DIR as needed)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'Rainfall_forcasting', 'models', 'model_kasserine.pkl')

print(f"Trying to load model from: {model_path}")

try:
    model = joblib.load(model_path)

    print("✅ Model loaded successfully!")
    print("Model type:", type(model))
except Exception as e:
    print("❌ Failed to load model.")
    print("Error:", str(e))


