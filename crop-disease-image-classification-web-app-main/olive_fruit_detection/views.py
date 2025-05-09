from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from .yolo_detector import OliveFruitDetector

MODEL_PATH = os.path.join(settings.BASE_DIR, 'olive_fruit_detection', 'oliveDetection4_YOLO11.pt')
detector = OliveFruitDetector(MODEL_PATH)

def detect_olive_view(request):
    context = {}
    if request.method == 'POST' and 'image' in request.FILES:
        uploaded_file = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        filepath = os.path.join(settings.MEDIA_ROOT, filename)

        try:
            result = detector.detect(filepath, save_dir=settings.MEDIA_ROOT)
            context['result_image'] = fs.url(os.path.basename(result["saved_path"]))
            context['box_count'] = result["boxes"]
            context['labels'] = list(zip(result["labels"], result["confidences"]))
            context['estimated_weight'] = result["estimated_weight_g"]

        except Exception as e:
            context['error'] = str(e)

    return render(request, 'olive_fruit_detection/detect.html', context)
