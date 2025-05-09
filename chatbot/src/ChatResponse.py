'''
************************************************************************************************

    FileName        : ChatResponse.py
    Description     : Handles chatbot response with embedding search + RAG
    Created By      : Vidushi Gandhi
    Date            : 10th April 2025

************************************************************************************************
'''

# Import Modules 
import re 
import psycopg2
import logging
from chatbot.src import ChatEmbed, RagEngine, Common

'''***************************************** Main Code ********************************************'''
# Adding app_logger
chat_logger = logging.getLogger('app_logger')

# Database Config
db_config = Common.db_config()
model_config = Common.model_config()
SIMILARITY_THRESHOLD = 0.2

# PostgreSQL Config
db_cred = {
    "dbname": db_config['DBName'],
    "user": db_config['User'],
    "password": db_config['Password'],
    "host": db_config['Host'],
    "port": db_config['Port'],
}

# Preprocess query
def _preprocess_query(query):
    query = query.lower().strip()
    query = re.sub(r"[^\w\s,.!?-]", "", query)
    query = re.sub(r"\bwho is\b", "about", query)
    query = re.sub(r"\bwhat is\b", "describe", query)
    return query

# Main function for embedding-based search
def chatres_search_embeddings(data):
    chat_logger.debug(f'chatres_search_embeddings data:{data}')
    try:
        query_text = data.get("query")
        if not query_text:
            res = {"error": "Query text is required."}
            chat_logger.debug(f'Error in chatres_search_embeddings: {res}')
            chat_logger.error(f"Error in chatres_search_embeddings: {res}")
       
            return res, 400

        # 🔹 Preprocess + Embed
        query_text_cleaned = _preprocess_query(query_text)
        chat_logger.debug(f'Successfully preprocess the query')
        query_embedding = ChatEmbed.chatem_generate_embedding(query_text_cleaned)
        chat_logger.debug(f'Embeddings generated ')
        query_embedding_str = "[" + ", ".join(map(str, query_embedding)) + "]"

        chat_logger.debug(f"Query: {query_text_cleaned}")

        # 🔹 Vector search in PostgreSQL
        with psycopg2.connect(**db_cred) as conn:
            with conn.cursor() as cursor:
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

        # 🔹 Filter top relevant chunks
        filtered_results = [
            {"text": row[0], "similarity": row[1]}
            for row in top_results
            if row[1] >= SIMILARITY_THRESHOLD
        ]

        if not filtered_results:
            res = {
                "generated_answer": "Sorry, I couldn't find relevant information.",
                "source_texts": []
            }
            chat_logger.debug(f'Error in chatres_search_embeddings: {res}')
            chat_logger.error(f"Error in chatres_search_embeddings: {res}")
        
            return res, 200

        # Join context and generate answer
        context = "\n".join([res["text"] for res in filtered_results])
        generated_answer = RagEngine.rag_response(
            context, query_text, model=model_config['Model']
        )

        #  Prepare response with sources
        source_texts = [
            {
                "source": f"chunk_{i + 1}",
                "text": res["text"],
                "similarity": round(res["similarity"], 3)
            }
            for i, res in enumerate(filtered_results)
        ]

        res = {
            "query": query_text,
            "generated_answer": generated_answer,
            "source_texts": source_texts,
            "model": model_config['Model']
        }
        chat_logger.debug(f'Chat response {generated_answer}')
        return res, 200

    except Exception as e:
        chat_logger.debug(f'Error in chatres_search_embeddings: {e}')
        chat_logger.error(f"Error in chatres_search_embeddings: {e}")
        return {"error": str(e)}, 500
