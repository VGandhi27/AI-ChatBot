# 📚 AI-Powered Chatbot with Django Backend

## 🎯 Project Overview
This project integrates an AI-powered chatbot that answers user queries based on **Vidushi Gandhi's** professional experiences, blogs, and technical expertise. It leverages:  
- **Django Backend** to handle vector-based search, AI inference, and chat processing.  
- **PostgreSQL** to store and query vector embeddings efficiently.  
- **Hugging Face Models** for AI-powered response generation with contextual understanding.  

---

## 🛠️ Key Features
✅ **AI Chatbot with Context Awareness**  
- Responds to user queries about Vidushi's blogs, research papers, projects, and achievements.  
- Maintains conversational context to provide intelligent and coherent responses.  

✅ **Vector Search using PostgreSQL**  
- Stores text embeddings in PostgreSQL using a vector data store.  
- Enables fast and accurate retrieval of relevant content by matching query embeddings.  

✅ **Hugging Face NLP Models**  
- Integrates with Hugging Face models to process natural language and generate AI responses.  
- Supports transfer learning and fine-tuned models for enhanced accuracy.  

✅ **API Endpoints for Chat and Embeddings**  
- REST APIs to handle incoming queries and update vector embeddings dynamically.  

---

## 🚀 Tech Stack

### ⚙️ Backend
- **Django** – REST API and backend logic  
- **PostgreSQL** – Vector embeddings storage and search  
- **Hugging Face Transformers** – AI model integration for NLP  

### 📊 Database
- PostgreSQL with **PGVector** extension for vector similarity search  

### 🧠 AI & NLP Models
- **Hugging Face Models** – For AI inference and embeddings  

---

## 📂 Project Structure

/ai-chatbot-backend ├── /chatbot_api # Main chatbot API logic │ ├── /embeddings # Embedding models and utilities │ ├── /models # AI models and Hugging Face integration │ ├── /utils # Helper functions for chat processing │ └── /views # API endpoints and business logic ├── /config # Django settings and configurations │ ├── settings.py │ └── urls.py ├── /db # PostgreSQL configuration and migrations ├── /templates # Template files for chatbot interface └── /static # Static files and assets

---

## 🔥 Getting Started

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/vidushi-gandhi/ai-chatbot-backend.git
cd ai-chatbot-backend

### 2️⃣ Setup Virtual Environment

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

3️⃣ Configure PostgreSQL Database
Create a PostgreSQL database.

Update DATABASES in config/settings.py with your credentials.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ai_chatbot_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

4️⃣ Setup Environment Variables
Create a .env file in the project root and add:

DATABASE_URL=postgres://username:password@localhost:5432/ai_chatbot_db
HUGGINGFACE_API_KEY=your_huggingface_api_key

5️⃣ Run Database Migrations

# Apply migrations
python manage.py makemigrations
python manage.py migrate

6️⃣ Generate Vector Embeddings
To generate and store embeddings for Vidushi’s blogs and work data:
python manage.py runscript generate_embeddings

# Start development server
python manage.py runserver


📖 API Endpoints
Method	Endpoint	Description
POST	/api/chat/	Handles user queries and returns responses
POST	/api/embeddings/	Stores and updates vector embeddings
GET	/api/history/	Retrieves user chat history
🤖 How It Works
User Query Input: The chatbot receives user queries and processes them.

Vector Search & Retrieval: Query embeddings are matched with stored embeddings using PostgreSQL’s vector store.

AI Response Generation: Relevant data is passed through Hugging Face models for context-aware responses.

Context Management: The chatbot maintains a conversation history to preserve context across multiple interactions.

📝 Project Workflow
Extract & Embed Blog Data:

Extract content from Vidushi’s blogs, achievements, and projects.

Convert data to vector embeddings using a pre-trained Hugging Face model.

Store Embeddings in PostgreSQL:

Store generated embeddings in PostgreSQL with similarity-based indexing.

Chatbot Query Handling:

Receive user queries, generate query embeddings, and retrieve matching content.

Return context-aware responses using AI models.

📊 Vector Embedding Process
Text Extraction: Content is pre-processed and converted to embeddings.

Vector Storage: Embeddings are stored in PostgreSQL with PGVector extension.

Similarity Search: User queries are matched with stored embeddings for relevant responses.

📝 Environment Variables
Create a .env file in the project root with the following configuration:

DATABASE_URL=postgres://username:password@localhost:5432/ai_chatbot_db
HUGGINGFACE_API_KEY=your_huggingface_api_key
🔥 To-Do List
 Implement WebSocket support for real-time responses.

 Add user authentication for personalized conversations.

 Enhance query latency optimization with advanced vector search techniques.

🤝 Contributing
Contributions are welcome! Here's how to contribute:

Fork the repository.

Create a new branch (feature/your-feature).

Commit your changes.

Open a pull request.

📧 Contact Me
For any queries, reach out to me on:

✉️ LinkedIn

🌐 Portfolio

⚡ License
This project is licensed under the MIT License.

--- bash


✅ **This is the complete, well-structured, and formatted `README.md` file.**  
You can directly add this file to your GitHub project. If any adjustments or additional features are needed, let me know! 🚀😊
