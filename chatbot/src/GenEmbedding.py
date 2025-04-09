'''
************************************************************************************************
    
    FileName : GenEmbedding.py
    File Description : File handles generating embeddings
    Created By : Vidushi Gandhi
    Date : 9th April 2025

************************************************************************************************
'''

# Import Modules 

# 🔹 Generate Embedding
def generate_embedding(text, model=model_config['Model']):
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