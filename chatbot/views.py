import json
import numpy as np
import psycopg2
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
import nltk
import re
from nltk.tokenize import sent_tokenize

nltk.download("punkt")

# Ollama API
OLLAMA_API_URL = "http://127.0.0.1:11434/api/embeddings"

# PostgreSQL Config
DB_CONFIG = {
    "dbname": "portfolio",
    "user": "postgres",
    "password": "root",
    "host": "localhost",
    "port": "5433",
}

SIMILARITY_THRESHOLD = 0.2

# 🔹 Generate Embedding
def generate_embedding(text, model="dolphin-phi"):
    url = OLLAMA_API_URL
    payload = {
        "model": model,
        "prompt": text,
        "format": "json",
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        result = response.json()
        embeddings = result.get("embedding", [])
        if embeddings:
            return embeddings
        else:
            raise Exception("No embeddings returned.")
    else:
        raise Exception(f"Ollama error: {response.text}")

# 🔹 Preprocess query
def preprocess_query(query):
    query = query.lower().strip()
    query = re.sub(r"[^\w\s]", "", query)
    query = query.replace("who is", "about").replace("what is", "describe")
    return query

# 🔹 Chunk large text
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

# 🔹 Upload text & embeddings
@api_view(["POST"])
def upload_text(request):
    try:
        text = request.data.get("text", None)
        if not text:
            return Response({"error": "No text provided."}, status=400)

        sentences = split_and_combine(text)
        inserted_data = []

        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        for sentence in sentences:
            embedding = generate_embedding(sentence)
            embedding_str = "[" + ", ".join(map(str, embedding)) + "]"  # ✅ Convert to PostgreSQL vector format

            cur.execute(
                "INSERT INTO embeddings (content, embedding) VALUES (%s, %s::vector) RETURNING id;",
                (sentence, embedding_str),
            )
            new_id = cur.fetchone()[0]
            inserted_data.append({
                "id": new_id,
                "content": sentence,
                "embedding": embedding,
            })

        conn.commit()
        cur.close()
        conn.close()

        return Response(
            {"message": "Embeddings stored successfully!", "data": inserted_data},
            status=201,
        )

    except Exception as e:
        return Response({"error": str(e)}, status=500)

# 🔹 Search embeddings
@csrf_exempt
def search_embeddings(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            query_text = data.get("query")
            if not query_text:
                return JsonResponse({"error": "Query text is required"}, status=400)

            query_text = preprocess_query(query_text)
            query_embedding = generate_embedding(query_text)
            query_embedding_str = "[" + ", ".join(map(str, query_embedding)) + "]"

            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT content, 1 - (embedding <#> %s::vector) AS similarity
                FROM embeddings
                ORDER BY similarity DESC
                LIMIT 10;
                """,
                (query_embedding_str,),
            )

            filtered_results = [
                {"text": row[0], "similarity": row[1]}
                for row in cursor.fetchall()
                if row[1] >= SIMILARITY_THRESHOLD
            ]

            cursor.close()
            conn.close()

            return JsonResponse({"results": filtered_results})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)
