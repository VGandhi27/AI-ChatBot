'''
************************************************************************************************
    
    FileName          : ChatStore.py
    Description       : File handle storing data in database
    Created By        : Vidushi Gandhi
    Date              : 9th April 2025

************************************************************************************************
'''

# Import Modules 
import nltk
import logging
import psycopg2
import traceback
from nltk.tokenize import sent_tokenize
from chatbot.src import ChatEmbed, Common

# Add your local nltk_data path here
nltk.data.path.append('./nltk_data')

'''***************************************** Main Code ********************************************'''
# Adding app_logger
chat_logger = logging.getLogger('app_logger')


# Ensure 'punkt' is available (important for cloud deployments like Render)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', download_dir='./nltk_data')


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
        if len(current_chunk) + len(sentence) + 1 <= max_len:
            current_chunk += " " + sentence if current_chunk else sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def cstore_upload_data(text):
    chat_logger.debug(f"cstore_upload_data text:{text}")
    try:
        if not text:
            res = {"error": "No text provided."}
            chat_logger.debug(f'Error storing embeddings: {res}')
            chat_logger.error(f'Error storing embeddings: {res}')
            return res, 400

        sentences = split_and_combine(text)
        inserted_data = []

        
        with psycopg2.connect(**db_cred) as conn:
            with conn.cursor() as cur:
                for sentence in sentences:
                    embedding = ChatEmbed.chatem_generate_embedding(sentence)
                    # PostgreSQL vector format
                    embedding_str = "[" + ", ".join(map(str, embedding)) + "]"  

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
        res = {"message": "Embeddings stored successfully!", "data": inserted_data}
        chat_logger.debug(f'Embeddings stored in db : {res}')
        return res, 201

    except Exception as e:
        res = {"error": f"{type(e).__name__}: {str(e)}", "trace": traceback.format_exc()}
        
        chat_logger.debug(f'Error storing embeddings : {res}')
        chat_logger.error(f'Error storing embeddings : {res}')
        return res, 500
