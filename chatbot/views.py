import json
import logging
from django.http import JsonResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from chatbot.src import ChatStore,ChatResponse
from rest_framework.response import Response

# Adding app_logger
chat_logger = logging.getLogger('app_logger')


# 🔹 Upload text & embeddings
@api_view(["POST"])
def upload_text(request):
    text = request.data.get("text", None)
    chat_logger.info(f'Upload the text data in db request:{text}')
    res,status = ChatStore.cstore_upload_data(text)
    return Response(res,status=status )


# 🔹 RAG Search Embeddings + Generation
@csrf_exempt
def search_embeddings(request):
    if request.method == "POST":
        data = json.loads(request.body)
        chat_logger.info(f'Search Embeddings :{data}')
        res , code = ChatResponse.chatres_search_embeddings(data)
        return JsonResponse(res, status = code)
    return JsonResponse({"error": "Invalid request method"}, status=405)


def notfound(request, exception):
    chat_logger.info(f'Not found request :{request},exception:{exception}')
    return HttpResponseNotFound("Oops! Page not found.")