import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.efficientnet import preprocess_input
from .base_model import BasePlantModel

class DatesModel(BasePlantModel):
    CLASSES = ['brown spots', 'healthy', 'white scale']
    
    def __init__(self, model_path):
        from tensorflow.keras.mixed_precision import Policy
        self.model = load_model(model_path, custom_objects={"DTypePolicy": Policy})
        self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    
    def predict(self, image_path):
        img = self.load_image(image_path)
        img = img.resize((224, 224))
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        
        preds = self.model.predict(img_array)
        class_idx = np.argmax(preds)
        confidence = float(np.max(preds)) * 100
        all_preds = {self.CLASSES[i]: float(preds[0][i]) * 100 for i in range(len(self.CLASSES))}
        
        return {
            'class': self.CLASSES[class_idx],
            'confidence': confidence,
            'all_predictions': all_preds,
            'model_name': 'Date Palm Stage Classifier'
        }