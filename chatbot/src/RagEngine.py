'''
************************************************************************************************

    FileName       : RagEngine.py
    Description    : File handles ragengine response
    Created By     : Vidushi Gandhi
    Date           : 9th April 2025

************************************************************************************************
'''

# Import Modules 
import requests
from chatbot.src import Common

# Model Config 
model_config =  Common.model_config()

# Ollama API
OLLAMA_API_URL = f"http://{model_config['Host']}:{model_config['Port']}/api/generate"

# 🔹 Optional: Clean up repetitive/robotic phrases
def clean_response(text):
    unwanted = [
        "Based on the information provided",
        "According to the context",
        "Based on the context",
        "According to the information provided",
    ]
    for phrase in unwanted:
        text = text.replace(phrase, "")
    return text.strip().capitalize()

# 🔹 Generate LLM Response using Ollama phi
def rag_response(context, question, model="phi"):
    prompt =f"""
You’re a helpful, articulate AI assistant trained on Vidushi Gandhi’s professional background. 
You think like a curious, well-informed human who communicates clearly and thoughtfully.

Answer the user's question using only the information below. Don’t make up facts or assume anything not mentioned. 
If the answer isn’t there, just say: “I’m not sure about that.”

Imagine you're chatting with someone genuinely interested in Vidushi’s journey. 
Keep your tone friendly and natural — like you're explaining something, not reading a report.
Aim for clear, varied sentence structures. Avoid robotic phrases like “based on the context.”

---
Here’s what you know:
Information:
{context}

User's Question: {question}

Answer:
""".strip()

    try:
        response = requests.post(
            OLLAMA_API_URL, json={"model": model, "prompt": prompt, "stream": False},
        )
        if response.status_code == 200:
            answer = response.json().get("response", "I'm not sure about that.")
            return clean_response(answer)
        else:
            return f"Error: {response.text}"

    except Exception as e:
        return f"Error connecting to model: {str(e)}"
