'''
* File Name         : Upload2.py
* Description       : Functions related to Upload data in postgresql
'''

# Import Modules
import json
import requests
import nltk
from nltk.tokenize import sent_tokenize
from chatbot.src import Common
nltk.download("punkt")

# Updated JSON data
portfolio_data = [
    {
        "question": "Who is Vidushi Gandhi?",
        "content": "Vidushi Gandhi is a Data Science Engineer at Iktara Data Sciences, where she is actively involved in building Airtel's Transmission System and an inventory data storage pipeline. She specializes in detecting configuration changes, developing network dashboards, and creating a Dark Network Operating Center for Airtel. Her expertise lies in network data storage, alarm systems, and analytics, contributing to the transformation of telecom networks into intent-driven autonomous systems.",
        "section": "bio"
    },
    {
        "question": "Where did Vidushi Gandhi work before Iktara Data Sciences?",
        "content": "Previously, Vidushi worked as a Software Engineer at Microsoft, developing Computer Vision systems and Mixed Reality applications for HoloLens. She also has experience as a Software Engineer at GitHub, where she worked part-time.",
        "section": "bio"
    },
    {
        "question": "What is Vidushi Gandhi's educational background?",
        "content": "Vidushi completed her undergraduate degree in Computer Science and Engineering from Echelon Institute of Technology, Faridabad. She secured AIR-157 (5th category) in CDAC C-CAT 2025 and is planning to pursue post-graduation.",
        "section": "bio"
    },
    {
        "question": "What research papers has Vidushi Gandhi published?",
        "content": "Vidushi Gandhi has conducted extensive research in AI & Machine Learning, with two published research papers, including 'SVM-Based Framework for Breast Cancer Detection', published in Springer Advances in Artificial-Business Analytics and Quantum Machine Learning, and 'Analyzing the Causes of Mood Disorders: A Comprehensive Study'.",
        "section": "research"
    },
    {
        "question": "What are Vidushi Gandhi's technical skills?",
        "content": "Vidushi has expertise in Programming & Development (Python, Django, Flask, React.js, Next.js), Machine Learning & AI (TensorFlow, PyTorch, Logistic Regression, KNN, SVM, Decision Trees), Web Development (Tailwind CSS, Sass), Database Management (PostgreSQL, Vector Databases), and Network Automation & Data Analytics (inventory/configuration rules, performance monitoring, alarm detection).",
        "section": "skills"
    },
    {
        "question": "What hackathons has Vidushi Gandhi participated in?",
        "content": "Vidushi Gandhi participated in the Alt Hack (IIT Delhi), where her team’s Water Management System (Blockchain & IoT) project was selected in the top 14 out of 405 teams. She also organized and won 2nd place in the TECHLON Hackathon (Inter-University).",
        "section": "hackathons"
    },
    {
        "question": "What community work has Vidushi Gandhi done?",
        "content": "Vidushi Gandhi served as a GDSC Lead at the Google Developer Students Club and contributed as a Technical Writer at Hashnode. She also contributed to Hacktoberfest 2023 and was recognized as an early contributor, resulting in a tree being planted in her name in Tanzania.",
        "section": "community"
    },
    {
        "question": "What features does Vidushi Gandhi's portfolio include?",
        "content": "Vidushi is currently working on a 3D home page for her portfolio using Next.js. She is also designing a professional chatbot about herself, integrating it with a vector database and AI model for interactive responses. Her portfolio includes a structured blog section integrating content from Dev.to, a Research Section showcasing her published papers, and a Chatbot that answers queries about her work and experience.",
        "section": "portfolio"
    },
    {
        "question": "What are Vidushi Gandhi's future aspirations?",
        "content": "Vidushi aims to leverage AI & Machine Learning in network automation, autonomous systems, and intelligent data analytics. She is passionate about building scalable AI solutions that drive innovation in telecom, automation, and real-time analytics.",
        "section": "goals"
    },
    {
        "question": "What are Vidushi Gandhi's contributions to open-source?",
        "content": "Vidushi contributed to Hacktoberfest 2023 and was among the initial 50,000 contributors, resulting in a tree being planted in her name in Tanzania.",
        "section": "community"
    }
]

# API Endpoint
cbot_config = Common.chat_bot_config()
url = f"http://{cbot_config['Host']}:{cbot_config['Port']}/chatbot/upload/"

# Upload data to API with correct format
for item in portfolio_data:
    
    sentence = f"{item['question']} {item['content']}"
    print(f'sentence--{sentence}')
    response = requests.post(url, json={"text": sentence})
    # response = requests.post(url, json=item)
    if response.status_code == 200:
        print(f"✅ Uploaded: {item['question'][:50]}... | Response: {response.json()}")
    else:
        print(f"❌ Failed: {item['question'][:50]}... | Status: {response.status_code}")

print("\n🎉✅ Data uploaded successfully!")
