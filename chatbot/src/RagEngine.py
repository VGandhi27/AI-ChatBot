'''
************************************************************************************************

    FileName       : RagEngine.py
    Description    : File handles RAG engine response
    Created By     : Vidushi Gandhi
    Date           : 9th April 2025

************************************************************************************************
'''

# Import Modules 
import os
import torch
import requests
import logging
from chatbot.src import Common

os.environ["TRANSFORMERS_NO_TF"] = "1"

# Hugging Face Grammar Model
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

'''***************************************** Main Code ********************************************'''
# Adding app_logger
chat_logger = logging.getLogger('app_logger')


# Initialize variables
tokenizer, model = None, None

def load_model():
    # Load grammar correction model once
    global tokenizer, model
    if tokenizer is None or model is None:
        tokenizer = AutoTokenizer.from_pretrained("vennify/t5-base-grammar-correction")
        model = AutoModelForSeq2SeqLM.from_pretrained("vennify/t5-base-grammar-correction", from_tf=False)
    return tokenizer, model


def polish_grammar(text):
    tokenizer, model = load_model()
    input_text = f"grammar: {text}"
    inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(inputs, max_length=512, num_beams=4, early_stopping=True)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Model Config 
model_config =  Common.model_config()
OLLAMA_API_URL = f"http://{model_config['Host']}:{model_config['Port']}/api/generate"

# Clean up repetitive/robotic phrases
def clean_response(text):
    unwanted = [
        "Based on the information provided",
        "According to the context",
        "Based on the context",
        "According to the information provided",
    ]
    for phrase in unwanted:
        text = text.replace(phrase, "")
    return text.strip()

# Generate LLM Response using Ollama
def rag_response(context, question, model="phi"):
    chat_logger.debug(f'rag_response request: {context, question, model}')
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
            chat_logger.debug(f'Rag Engine successfully fetch the response from ollama model')
            raw_answer = response.json().get("response", "I'm not sure about that.")
            cleaned = clean_response(raw_answer)
            polished = polish_grammar(cleaned)
            return polished
        else:
            chat_logger.debug(f'Failure in ollama res : {response.text}')
            chat_logger.error(f'Failure in ollama res : {response.text}')
            return f"Error: {response.text}"

    except Exception as e:
        chat_logger.debug(f'Error connecting to model: {str(e)}')
        chat_logger.error(f'Error connecting to model: {str(e)}')
        return f"Error connecting to model: {str(e)}"
