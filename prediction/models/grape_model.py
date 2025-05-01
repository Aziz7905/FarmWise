import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.mixed_precision import Policy
from .base_model import BasePlantModel
from tensorflow.keras.layers import InputLayer

class GrapeModel(BasePlantModel):
    CLASSES = ['ESCA', 'Black Rot', 'Healthy', 'Leaf Blight']
    
    def __init__(self, model_path):
        self.model = self._load_model(model_path)
        
    def _load_model(self, model_path):
        try:
            # Try normal loading first
            return load_model(model_path)
        except TypeError as e:
            if "Unrecognized keyword arguments: ['batch_shape']" in str(e):
                # Patch InputLayer to ignore 'batch_shape'
                def patched_input_layer(**kwargs):
                    kwargs.pop('batch_shape', None)
                    return InputLayer(**kwargs)

                custom_objects = {
                    'InputLayer': patched_input_layer,
                    'DTypePolicy': Policy
                }
                return load_model(model_path, custom_objects=custom_objects)
            raise  # Re-raise any other unexpected errors
    
def predict(self, image_path):
    img = self.load_image(image_path)
    img = img.resize((64, 64))
    img_array = np.array(img).astype('float32') / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    try:
        preds = self.model.predict(img_array)

        if preds is None or len(preds) == 0:
            raise ValueError("Prediction returned None or empty array.")

        class_idx = np.argmax(preds)
        confidence = float(np.max(preds)) * 100
        all_preds = {
            self.CLASSES[i]: float(preds[0][i]) * 100
            for i in range(len(self.CLASSES))
        }

        return {
            'class': self.CLASSES[class_idx],
            'confidence': confidence,
            'all_predictions': all_preds,
            'model_name': 'Grape Disease Classifier'
        }
    except Exception as e:
        print(f"Error during prediction: {e}")
        return {
            'error': str(e),
            'model_name': 'Grape Disease Classifier'
        }
