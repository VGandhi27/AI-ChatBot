'''
************************************************************************************************
    
    FileName : RagEngine.py
    File Description : File handles ragengine response
    Created By : Vidushi Gandhi
    Date : 9th April 2025

************************************************************************************************
'''

# Import Modules 
import requests

# 🔹 Generate LLM Response using Ollama phi
def rag_response(context, question, model="phi"):
    prompt = f"""
You are a helpful assistant chatbot trained exclusively on Vidushi Gandhi's professional and technical experience.

Use the following context to answer the question. If the answer is not in the context, just say "I don't know".

Context:
{context}

Question: {question}
Answer:
""".strip()

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False},
    )

    if response.status_code == 200:
        return response.json().get("response", "I'm not sure about that.")
    else:
        return f"Error: {response.text}"
