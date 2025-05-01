from tensorflow.keras.models import load_model
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.efficientnet import preprocess_input
from PIL import Image

GRAPE_CLASSES = ['ESCA', 'Black Rot', 'Healthy', 'Leaf Blight']

class GrapeModel:
    def __init__(self, model_path='assets/my_plant_classifier.h5'):
        self.model = load_model(model_path)
    
    def predict(self, img_path):
        img = Image.open(img_path).resize((64, 64))
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        preds = self.model.predict(img_array)
        return GRAPE_CLASSES[np.argmax(preds)], float(np.max(preds)) * 100
