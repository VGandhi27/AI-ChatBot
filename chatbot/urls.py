from django.urls import path
from .views import search_embeddings,upload_text

urlpatterns = [
    path("search/", search_embeddings, name="search_embeddings"),
    path("upload/", upload_text, name="upload_text"),
]
