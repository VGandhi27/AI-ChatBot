import json
import numpy as np
import psycopg2
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection
import torch
import nltk
import re
from nltk.tokenize import sent_tokenize
from transformers import AutoTokenizer, AutoModel

nltk.download("punkt")

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

# Similarity Threshold
SIMILARITY_THRESHOLD = 0.6


# 🔥 Function to generate embeddings
def generate_embedding(text):
    tokens = tokenizer(
        text,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=512,  # ✅ Ensures no data is lost
    )
    with torch.no_grad():
        embedding = model(**tokens).last_hidden_state.mean(dim=1).squeeze().tolist()
    return embedding


# 🔥 Preprocess the query to normalize it
def preprocess_query(query):
    query = query.lower().strip()
    query = re.sub(r"[^\w\s]", "", query)  # Remove special characters
    query = query.replace("who is", "about").replace("what is", "describe")
    return query


# 🔥 Split and combine text into meaningful chunks before embedding
def split_and_combine(text, max_len=300):
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_len:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks


# 📡 API to store embeddings in PostgreSQL
@api_view(["POST"])
def upload_text(request):
    """
    API to upload text, generate embeddings, and store in PostgreSQL using raw SQL.
    """
    try:
        text = request.data.get("text", None)
        if not text:
            return Response({"error": "No text provided."}, status=400)

        # Split and combine text into meaningful chunks
        sentences = split_and_combine(text)
        inserted_data = []

        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        for sentence in sentences:
            embedding = generate_embedding(sentence)
            cur.execute(
                "INSERT INTO embeddings (content, embedding) VALUES (%s, %s) RETURNING id;",
                (sentence, embedding),
            )
            new_id = cur.fetchone()[0]
            inserted_data.append(
                {"id": new_id, "content": sentence, "embedding": embedding}
            )

        conn.commit()
        cur.close()
        conn.close()

        return Response(
            {"message": "Embeddings stored successfully!", "data": inserted_data},
            status=201,
        )

    except Exception as e:
        return Response({"error": str(e)}, status=500)


# 🔍 API to search embeddings and retrieve best matches
@csrf_exempt
def search_embeddings(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            query_text = data.get("query")

            if not query_text:
                return JsonResponse({"error": "Query text is required"}, status=400)

            # Preprocess and generate query embedding
            query_text = preprocess_query(query_text)
            query_embedding = generate_embedding(query_text)

            # Connect to PostgreSQL
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()

            # Search in the vector database with a similarity threshold
            cursor.execute(
                """
                SELECT content, 1 - (embedding <=> %s::vector) AS similarity
                FROM embeddings
                ORDER BY similarity DESC
                LIMIT 10;
                """,
                (query_embedding,),
            )

            # Filter results by threshold
            filtered_results = [
                {"text": row[0], "similarity": row[1]}
                for row in cursor.fetchall()
                if row[1] >= SIMILARITY_THRESHOLD
            ]

            cursor.close()
            conn.close()

            if not filtered_results:
                return JsonResponse(
                    {"results": [], "message": "No relevant results found."}
                )

            return JsonResponse({"results": filtered_results})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)
