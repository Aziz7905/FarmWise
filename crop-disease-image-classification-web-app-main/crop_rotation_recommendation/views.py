from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils.qa_chain import answer_question
import json

@csrf_exempt
def chat_view(request):
    if request.method == "GET":
        return render(request, "crop_rotation_recommendation/chat.html")

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            question = data.get("question", "").strip()
            if not question:
                return JsonResponse({"response": "No question provided."}, status=400)

            answer = answer_question(question)
            return JsonResponse({"response": answer})
        except json.JSONDecodeError as e:
            return JsonResponse({"response": f"Invalid JSON data: {str(e)}"}, status=400)
        except Exception as e:
            return JsonResponse({"response": f"Server error: {str(e)}"}, status=500)
        

    return JsonResponse({"response": "Only GET and POST allowed"}, status=405)
