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
from chatbot.src import Common

# Model Config 
model_config =  Common.model_config()

# Ollama API
OLLAMA_API_URL = f"http://{model_config['Host']}:{model_config['Port']}/api/embeddings"

# 🔹 Generate Embedding
def chatem_generate_embedding(text, model=model_config['Model']):
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