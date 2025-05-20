from django.shortcuts import render
from .predictor import load_suitability_model

model = load_suitability_model()

def predict_crop_view(request):
    predictions = None
    error = None
    if request.method == 'POST':
        try:
            input_data = {
                'N': float(request.POST['N']),
                'P': float(request.POST['P']),
                'K': float(request.POST['K']),
                'temperature': float(request.POST['temperature']),
                'humidity': float(request.POST['humidity']),
                'ph': float(request.POST['ph']),
                'rainfall': float(request.POST['rainfall']),
            }
            model = load_suitability_model()
            predictions = model.predict(input_data)
        except Exception as e:
            error = str(e)

    return render(request, 'crop_soil_suitability/predict_crop.html', {
        'predictions': predictions,
        'error': error
    })

