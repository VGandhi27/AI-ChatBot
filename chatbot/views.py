import json
import numpy as np
import psycopg2
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from transformers import AutoTokenizer, AutoModel
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection 
import torch
import nltk

nltk.download("punkt")
from nltk.tokenize import sent_tokenize

# Load Hugging Face model for embedding generation
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

# PostgreSQL Connection
DB_CONFIG = {
    "dbname": "portfolio",
    "user": "postgres",
    "password": "root",
    "host": "localhost",
    "port": "5433",
}

# Function to generate embeddings
def generate_embedding(text):
    tokens = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        embedding = model(**tokens).last_hidden_state.mean(dim=1).squeeze().tolist()
    return embedding

@csrf_exempt
def search_embeddings(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            query_text = data.get("query")

            if not query_text:
                return JsonResponse({"error": "Query text is required"}, status=400)

            query_embedding = generate_embedding(query_text)

            # Connect to PostgreSQL
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()

            # Search in the vector database
            cursor.execute(
                """
                SELECT content, embedding <=> %s::vector AS distance
                FROM embeddings
                ORDER BY distance ASC
                LIMIT 5;
                """,
                (query_embedding,),
            )

            results = [{"text": row[0], "distance": row[1]} for row in cursor.fetchall()]

            cursor.close()
            conn.close()

            return JsonResponse({"results": results})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@api_view(['POST'])
def upload_text(request):
    """
    API to upload text, generate embeddings, and store in PostgreSQL using raw SQL.
    """
    try:
        text = request.data.get('text', None)
        if not text:
            return Response({"error": "No text provided."}, status=400)
        
        sentences = sent_tokenize(text)  # Split into sentences
        inserted_data = []

        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        for sentence in sentences:
            embedding = generate_embedding(sentence)  # ✅ Fixed embedding function
            cur.execute(
                "INSERT INTO embeddings (content, embedding) VALUES (%s, %s) RETURNING id;",
                (sentence, embedding)  # ✅ Store embedding correctly
            )
            new_id = cur.fetchone()[0]  # Get inserted ID
            inserted_data.append({"id": new_id, "content": sentence, "embedding": embedding})

        conn.commit()
        cur.close()
        conn.close()

        return Response({"message": "Embeddings stored successfully!", "data": inserted_data}, status=201)

    except Exception as e:
        return Response({"error": str(e)}, status=500)