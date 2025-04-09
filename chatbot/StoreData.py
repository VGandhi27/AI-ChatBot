'''
************************************************************************************************
    
    FileName : StoreData.py
    File Description : File handle storing data in database
    Created By : Vidushi Gandhi
    Date : 9th April 2025

************************************************************************************************
'''

# Import Modules 
import nltk
import re
import psycopg2
from chatbot.src import Common
from chatbot import views
from nltk.tokenize import sent_tokenize

'''***************************************** Main Code ********************************************'''

# Database Config
db_config = Common.db_config()

# PostgreSQL Config
db_cred = {
    "dbname": db_config['DBName'],
    "user": db_config['User'],
    "password": db_config['Password'],
    "host": db_config['Host'],
    "port": db_config['Port'],
}


# Chunk large text
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


def upload_text(request):
    try:
        text = request.data.get("text", None)
        if not text:
            return {"error": "No text provided."}

        sentences = split_and_combine(text)
        inserted_data = []

        conn = psycopg2.connect(**db_cred)
        cur = conn.cursor()

        for sentence in sentences:
            embedding = views.generate_embedding(sentence)
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

        return {"message": "Embeddings stored successfully!", "data": inserted_data}
    except Exception as e:
        return {"error": str(e)}

