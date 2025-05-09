from django.shortcuts import render
import joblib
import os
import numpy as np
from django.conf import settings

# Load model
MODEL_PATH = os.path.join(settings.BASE_DIR, 'crop_soil_suitability', 'knn_model.joblib')

model = joblib.load(MODEL_PATH)



def suitability_view(request):
    feature_labels = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    
    context = {
        'feature_labels': feature_labels,
        'prediction': None,
        'error': None
    }

    if request.method == 'POST':
        try:
            features = [float(request.POST[f"f{i}"]) for i in range(1, 8)]
            label_map = {
             0: 'maize',
            1: 'chickpea',
            2: 'lentil',
             3: 'pomegranate',
             4: 'kidneybeans',
              5: 'grapes',
              6: 'watermelon',
              7: 'muskmelon',
                 8: 'apple',
             9: 'orange',
             10: 'cotton'
            }
            prediction_index = model.predict([features])[0]
            prediction_label = label_map.get(prediction_index, "Unknown")
            context['prediction'] = prediction_label

            #prediction = model.predict([features])[0]
        except Exception as e:
            context['error'] = str(e)
    
    return render(request, 'crop_soil_suitability/suitability.html', context)

