from django.urls import path
from .views import search_embeddings

urlpatterns = [
    path("search/", search_embeddings, name="search_embeddings"),
]
