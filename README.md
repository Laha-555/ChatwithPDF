📄 Chat With Your PDF (RAG App)





An AI-powered application that allows users to upload a PDF and interact with it using natural language. Built using Streamlit, LangChain, ChromaDB, and Google Gemini.





🚀 Features
📂 Upload any PDF file
💬 Ask questions based on document content
🔍 Context-aware answers using RAG (Retrieval-Augmented Generation)
⚡ Fast semantic search using vector database (Chroma)
🤖 Powered by Google Gemini LLM
🧠 How It Works (RAG Pipeline)






This project implements a Retrieval-Augmented Generation (RAG) pipeline:

Document Loading
PDF is loaded using PyPDFLoader
Text Splitting
Split into chunks using RecursiveCharacterTextSplitter
Embedding Creation
Convert chunks into vectors using GoogleGenerativeAIEmbeddings
Vector Storage
Store embeddings in Chroma vector database
Query Processing
User query is matched against stored vectors
Context Retrieval
Most relevant chunks are retrieved
LLM Response
Context + Query → passed to Gemini model for final answer






🏗️ Tech Stack


Frontend: Streamlit
LLM: Google Gemini (gemini-2.5-flash)
Embeddings: gemini-embedding-001
Framework: LangChain
Vector DB: ChromaDB
Language: Python





3️⃣ Install dependencies



pip install -r requirements.txt




🔑 Environment Variables


Create a .env file and add your API key:


GOOGLE_API_KEY=your_api_key_here



▶️ Run the App
streamlit run app.py






📸 Demo Workflow
Upload a PDF
Ask a question
Get an AI-generated answer based on document context





⚠️ Error Handling
Displays error if no readable text is found in PDF
Handles empty chunks safely







