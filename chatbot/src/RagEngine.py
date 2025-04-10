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
    prompt = f"""
You are Vidushi Gandhi's intelligent assistant.

Answer the user's question truthfully and helpfully using the information provided below. 
Do not mention that the answer is based on context or source.
If the answer isn’t available, simply respond with: “I’m not sure about that.”

---
Information:
{context}

User's Question: {question}

Answer:
""".strip()

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
        )

        if response.status_code == 200:
            answer = response.json().get("response", "I'm not sure about that.")
            return clean_response(answer)
        else:
            return f"Error: {response.text}"

    except Exception as e:
        return f"Error connecting to model: {str(e)}"
