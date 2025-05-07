from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import numpy as np
import os
import pandas as pd
import torch
import torchvision.transforms as transforms
from torchvision import models
import torch.nn as nn
from django.conf import settings
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.layers import InputLayer
from sentence_transformers import SentenceTransformer, util


from tensorflow.keras.layers import InputLayer, Conv2D
from tensorflow.keras.initializers import GlorotUniform
from tensorflow.keras.optimizers import Adam

# Suppress TensorFlow logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.get_logger().setLevel('ERROR')

# Class labels
GRAPE_CLASSES = ['ESCA', 'Black Rot', 'Healthy', 'Leaf Blight']
DATES_CLASSES = ['brown spots', 'healthy', 'white scale']
ORANGE_CLASSES = ['grenning', 'canker', 'blackspot', 'fresh']
APPLE_CLASSES = ['healthy', 'multiple_diseases', 'rust', 'scab']

# Initialize device for PyTorch
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Define the Apple model architecture
class PlantDiseaseModel(nn.Module):
    def __init__(self, num_classes=4, pretrained=False):
        super(PlantDiseaseModel, self).__init__()
        self.backbone = models.resnet50(pretrained=pretrained)
        in_features = self.backbone.fc.in_features
        self.backbone.fc = nn.Sequential(
            nn.Linear(in_features, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, num_classes)
        )

    def forward(self, x):
        return self.backbone(x)

# Apple image transformations
apple_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

def custom_load_model(model_path):
    try:
        # Define a proper DTypePolicy class
        class DTypePolicy:
            def __init__(self, name='float32'):
                self.name = name
            
            @classmethod
            def from_config(cls, config):
                return cls(**config)
            
            def get_config(self):
                return {'name': self.name}

        # Define all custom objects needed for your models
        custom_objects = {
            'InputLayer': InputLayer,
            'Conv2D': Conv2D,
            'DTypePolicy': DTypePolicy,
            '_DTypePolicy': DTypePolicy,  # Sometimes it's registered with underscore
            'GlorotUniform': GlorotUniform,
            'Adam': Adam,
            # Add any other custom objects your model might need
        }
        
        # Try loading with custom objects
        with tf.keras.utils.custom_object_scope(custom_objects):
            model = tf.keras.models.load_model(model_path)
            model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
            return model
            
    except Exception as e:
        print(f"Error loading model {model_path}: {str(e)}")
        raise

# Load models with error handling
try:
    # Load Keras models
    grape_model = custom_load_model(os.path.join(settings.BASE_DIR, 'prediction', 'notebooks', 'my_plant_classifier.h5'))
    grape_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    
    dates_model = load_model(os.path.join(settings.BASE_DIR, 'prediction', 'notebooks', 'my_dates_classifier.h5'))
    dates_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    
    orange_model = load_model(os.path.join(settings.BASE_DIR, 'prediction', 'notebooks', 'my_oranges_classifier.h5'))
    orange_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    
    # Load PyTorch Apple model
    apple_model = PlantDiseaseModel(num_classes=len(APPLE_CLASSES), pretrained=False)
    state_dict = torch.load(
        os.path.join(settings.BASE_DIR, 'prediction', 'notebooks', 'my_apple_classifier.pth'),
        map_location=device
    )
    apple_model.load_state_dict(state_dict)
    apple_model = apple_model.to(device)
    apple_model.eval()
    
except Exception as e:
    raise RuntimeError(f"Error loading models: {e}")

# Load pesticide data and initialize recommendation system
try:
    # Load pesticide data
    pesticide_data_path = os.path.join(settings.BASE_DIR, 'prediction', 'notebooks', 'final_cleaned_pesticide_data.csv')
    pesticide_data = pd.read_csv(pesticide_data_path)
    pesticide_data.columns = pesticide_data.columns.str.strip()
    
    # Initialize sentence embedding model
    recommendation_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    
    # Pre-compute disease embeddings
    disease_column = "USAGE"
    pesticide_column = "SUBSTANCE ACTIVE"
    disease_texts = pesticide_data[disease_column].astype(str).tolist()
    disease_embeddings = recommendation_model.encode(disease_texts, convert_to_tensor=True)
    
except Exception as e:
    raise RuntimeError(f"Error loading pesticide recommendation system: {e}")

# Disease to pesticide mapping
DISEASE_TO_KEYWORD = {
    'ESCA': 'Esca grapevine',
    'Black Rot': 'Black rot grapevine',
    'Leaf Blight': 'Leaf blight grapevine',
    'brown spots': 'brown spots date palm',
    'white scale': 'white scale date palm',
    'grenning': 'greening citrus',
    'canker': 'canker citrus',
    'blackspot': 'black spot citrus',
    'rust': 'apple rust',
    'scab': 'apple scab',
    'multiple_diseases': 'apple diseases'
}

def recommend_pesticide(disease_name):
    """Recommend pesticide based on disease name"""
    try:
        # Get the search keyword for the disease
        search_term = DISEASE_TO_KEYWORD.get(disease_name, disease_name)
        
        # Encode the input disease
        input_embedding = recommendation_model.encode(search_term, convert_to_tensor=True)
        
        # Compute similarity scores
        similarity_scores = util.pytorch_cos_sim(input_embedding, disease_embeddings)
        
        # Get top 3 matches
        top_k = min(3, len(similarity_scores[0]))
        top_results = torch.topk(similarity_scores, k=top_k)
        
        recommendations = []
        for score, idx in zip(top_results[0][0], top_results[1][0]):
            idx = idx.item()
            recommendation = {
                'pesticide': pesticide_data.iloc[idx]['SUBSTANCE ACTIVE'],
                'company': pesticide_data.iloc[idx].get('SOCIETE', 'N/A'),
                'concentration': pesticide_data.iloc[idx].get('CONC.', 'N/A'),
                'usage': pesticide_data.iloc[idx]['USAGE'],
                'score': round(score.item() * 100, 2)  # Convert to percentage
            }
            recommendations.append(recommendation)
            
        return recommendations
        
    except Exception as e:
        print(f"Error in recommendation: {e}")
        return []

def predict_image(img_path, model_type):
    try:
        if model_type == 'dates':
            # Date palm model processing
            img = Image.open(img_path).convert('RGB')
            img = img.resize((224, 224))
            img_array = img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)
            
            preds = dates_model.predict(img_array)
            class_idx = np.argmax(preds)
            confidence = float(np.max(preds)) * 100
            all_preds = {DATES_CLASSES[i]: float(preds[0][i]) * 100 for i in range(len(DATES_CLASSES))}
            return DATES_CLASSES[class_idx], confidence, all_preds
            
        elif model_type == 'orange':
            # Orange model processing
            img = Image.open(img_path).convert('RGB')
            img = img.resize((224, 224))
            img_array = img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)
            
            preds = orange_model.predict(img_array)
            class_idx = np.argmax(preds)
            confidence = float(np.max(preds)) * 100
            all_preds = {ORANGE_CLASSES[i]: float(preds[0][i]) * 100 for i in range(len(ORANGE_CLASSES))}
            return ORANGE_CLASSES[class_idx], confidence, all_preds
            
        elif model_type == 'apple':
            # Apple model processing (PyTorch)
            img = Image.open(img_path).convert('RGB')
            img = apple_transform(img).unsqueeze(0).to(device)
            
            with torch.no_grad():
                outputs = apple_model(img)
                probabilities = torch.nn.functional.softmax(outputs, dim=1)
                confidence, class_idx = torch.max(probabilities, 1)
                confidence = confidence.item() * 100
                class_idx = class_idx.item()
                
                # Get all predictions
                all_probs = probabilities.squeeze().tolist()
                all_preds = {APPLE_CLASSES[i]: float(all_probs[i]) * 100 for i in range(len(APPLE_CLASSES))}
                
                return APPLE_CLASSES[class_idx], confidence, all_preds
            
        else:
            # Grape model processing
            img = Image.open(img_path).convert('RGB')
            img = img.resize((64, 64))
            img_array = np.array(img).astype('float32') / 255.0
            img_array = np.expand_dims(img_array, axis=0)
            
            preds = grape_model.predict(img_array)
            class_idx = np.argmax(preds)
            confidence = float(np.max(preds)) * 100
            all_preds = {GRAPE_CLASSES[i]: float(preds[0][i]) * 100 for i in range(len(GRAPE_CLASSES))}
            return GRAPE_CLASSES[class_idx], confidence, all_preds
            
    except Exception as e:
        raise RuntimeError(f"Prediction error: {str(e)}")

def upload_image(request):
    if request.method == 'POST':
        try:
            if 'image' not in request.FILES:
                return render(request, 'index.html', {'error': 'No image uploaded'})
            
            model_type = request.POST.get('model_type', 'grape')
            uploaded_file = request.FILES['image']
            
            if uploaded_file.size > 10*1024*1024:
                return render(request, 'index.html', {'error': 'File too large (max 10MB)'})
            
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            filepath = os.path.join(settings.MEDIA_ROOT, filename)
            
            class_name, confidence, all_preds = predict_image(filepath, model_type)
            
            # Get pesticide recommendations if not healthy
            recommendations = []
            if class_name.lower() != 'healthy':
                recommendations = recommend_pesticide(class_name)
            
            model_names = {
                'grape': 'Grape Disease Classifier',
                'dates': 'Date Palm Stage Classifier',
                'orange': 'Orange Disease Classifier',
                'apple': 'Apple Disease Classifier'
            }
            
            return render(request, 'index.html', {
                'result': {
                    'uploaded_file_url': fs.url(filename),
                    'class': class_name,
                    'confidence': confidence,
                    'all_predictions': all_preds,
                    'model_name': model_names.get(model_type, 'Plant Classifier'),
                    'recommendations': recommendations,
                    'is_healthy': class_name.lower() == 'healthy'
                }
            })
            
        except Exception as e:
            return render(request, 'index.html', {
                'error': f"Error processing image: {str(e)}"
            })
    
    return render(request, 'index.html')