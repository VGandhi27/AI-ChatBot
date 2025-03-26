'''
* File Name         : upload_data.py
* Description       : Functions related to Upload data in postgresql
'''

# Import modules 
import json
import requests
import nltk
from nltk.tokenize import sent_tokenize
from chatbot.src import Common

nltk.download("punkt")

# Your structured JSON data
portfolio_data = {
    "name": "Vidushi Gandhi",
    "role": "Data Science Engineer at Iktara Data Sciences",
    "professional_background": "Developing Airtel Transmission System, creating inventory storage pipeline...",
    "education": "B.Tech in Computer Science & Engineering from Echelon Institute of Technology, Faridabad",
    "research_papers": [
        "SVM-Based Framework for Breast Cancer Detection (Springer, 2023)",
        "Analysing the Causes of Mood Disorders: A Comprehensive Study"
    ],
    "technical_skills": ["Python", "Django", "PostgreSQL", "Hugging Face Transformers", "NLP"],
    "hackathons": [
        "Alt Hack at IIT Delhi - Blockchain & IoT-based Water Management System",
        "TECHLON Hackathon - 2nd Place"
    ],
    "community_work": [
        "GDSC Lead at Google Developer Students Club",
        "Technical Writer at Hashnode"
    ],
    "portfolio_features": [
        "3D Home Page using Next.js",
        "AI Chatbot with Vector Search (PostgreSQL)",
        "Network Dashboard Visualization"
    ],
    "future_goals": "Exploring Generative AI and Autonomous Networks in Telecom"
}

# Convert JSON values into a list of sentences
sentences = []
for key, value in portfolio_data.items():
    if isinstance(value, list):  # If the value is a list, flatten it
        sentences.extend(value)
    else:
        sentences.extend(sent_tokenize(str(value)))  # Tokenize text into sentences

# API Endpoint
cbot_config = Common.chat_bot_config()
url = f"http://{cbot_config['Host']}:{cbot_config['Port']}/chatbot/upload/"

# Upload each sentence separately
for sentence in sentences:
    response = requests.post(url, json={"text": sentence})
    print(f"Uploaded: {sentence[:50]}... | Response: {response.json()}")

print("\n✅ Data uploaded successfully!")

# Run code python -m chatbot.src.upload_data