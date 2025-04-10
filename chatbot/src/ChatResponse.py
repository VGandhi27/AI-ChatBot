'''
************************************************************************************************
    
    FileName : ChatResponse.py
    File Description : This file handles chat bot response
    Created By : Vidushi Gandhi
    Date : 10th April 2025

************************************************************************************************
'''

# Import Modules 
import re 
import psycopg2
from chatbot.src import ChatEmbed,RagEngine,Common

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

# Model Config 
model_config =  Common.model_config()

SIMILARITY_THRESHOLD = 0.2

# 🔹 Preprocess query
def _preprocess_query(query):
    query = query.lower().strip()
    query = re.sub(r"[^\w\s]", "", query)
    query = query.replace("who is", "about").replace("what is", "describe")
    return query


def chatres_search_embeddings(data):
    
    try:
        query_text = data.get("query")
        if not query_text:
            return {"error": "Query text is required"}, 400

        # 🔹 Preprocess + Embed the Query
        query_text_cleaned = _preprocess_query(query_text)
        query_embedding = ChatEmbed.chatem_generate_embedding(query_text_cleaned)
        query_embedding_str = "[" + ", ".join(map(str, query_embedding)) + "]"

        # 🔹 Retrieve relevant chunks from DB
        conn = psycopg2.connect(**db_cred)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT content, 1 - (embedding <#> %s::vector) AS similarity
            FROM embeddings
            ORDER BY similarity DESC
            LIMIT 5;
            """,
            (query_embedding_str,),
        )

        top_results = cursor.fetchall()
        filtered_results = [
            {"text": row[0], "similarity": row[1]}
            for row in top_results
            if row[1] >= SIMILARITY_THRESHOLD
        ]

        cursor.close()
        conn.close()

        if not filtered_results:
            res = {
                "generated_answer": "Sorry, I couldn't find relevant information.",
                "results": []
            }
            return res ,400

        # 🔹 Combine retrieved chunks as context
        context = "\n".join([res["text"] for res in filtered_results])

        # 🔹 Generate final answer using phi
        generated_answer = RagEngine.rag_response(context, query_text, model=model_config['Model'])
        res = {
            "query": query_text,
            "context": context,
            "generated_answer": generated_answer,
            "results": filtered_results
        }
        return res, 200

    except Exception as e:
        return {"error": str(e)}, 500


