'''
************************************************************************************************
    
    FileName        : GenEmbedding.py
    Description     : File handles generating embeddings
    Created By      : Vidushi Gandhi
    Date            : 9th April 2025

************************************************************************************************
'''

# Import Modules 
import requests
import logging
from chatbot.src import Common

'''***************************************** Main Code ********************************************'''
# Adding app_logger
chat_logger = logging.getLogger('app_logger')

# Model Config 
model_config =  Common.model_config()

# Ollama API
OLLAMA_API_URL = f"http://{model_config['Host']}:{model_config['Port']}/api/embeddings"

# 🔹 Generate Embedding
def chatem_generate_embedding(text, model=model_config['Model']):
    chat_logger.debug (f'chatem_generate_embedding request: {text, model}')
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
            chat_logger.debug (f'Embeddings generated')
            return embeddings
        else:
            chat_logger.debug (f'No embeddings returned.')
            chat_logger.error (f'No embeddings returned.')
            raise Exception("No embeddings returned.")
    else:
        res = f"Ollama error: {response.text}"
        chat_logger.debug (res)
        chat_logger.error (res)
        raise Exception(res)