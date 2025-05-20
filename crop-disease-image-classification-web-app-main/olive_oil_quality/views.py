from django.shortcuts import render
import joblib
import os
import numpy as np
from django.conf import settings

# Load model
MODEL_PATH = os.path.join(settings.BASE_DIR, 'olive_oil_quality', 'decision_tree_model.joblib')
model = joblib.load(MODEL_PATH)


def analyse_view(request):
    context = {}
    feature_labels = [
        'palmitic', 'palmitoleic', 'stearic', 'oleic',
        'linoleic', 'linolenic', 'arachidic', 'eicosenoic'
    ]
    context['feature_labels'] = feature_labels

    if request.method == 'POST':
        try:
            features = [float(request.POST[f"f{i}"]) for i in range(1, 9)]
            prediction = model.predict([features])[0]

            context['prediction'] = prediction
        except Exception as e:
            context['error'] = str(e)
    return render(request, 'olive_oil_quality/analyse.html', context)

