from tensorflow.keras.models import load_model
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.efficientnet import preprocess_input
from PIL import Image

ORANGE_CLASSES = ['grenning', 'canker', 'blackspot', 'fresh']

class OrangeModel:
    def __init__(self, model_path='assets/my_oranges_classifier.h5'):
        self.model = load_model(model_path)
    
    def predict(self, img_path):
        img = Image.open(img_path).resize((224, 224))
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        preds = self.model.predict(img_array)
        return ORANGE_CLASSES[np.argmax(preds)], float(np.max(preds)) * 100
