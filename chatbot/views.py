import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from chatbot.src import ChatStore,ChatResponse
from rest_framework.response import Response


# 🔹 Upload text & embeddings
@api_view(["POST"])
def upload_text(request):
    text = request.data.get("text", None)
    res,status = ChatStore.cstore_upload_data(text)
    return Response(res,status=status )


# 🔹 RAG Search Embeddings + Generation
@csrf_exempt
def search_embeddings(request):
    if request.method == "POST":
        data = json.loads(request.body)
        res , code = ChatResponse.chatres_search_embeddings(data)
        return JsonResponse(res, status = code)
    return JsonResponse({"error": "Invalid request method"}, status=405)
