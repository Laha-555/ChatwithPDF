import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from dotenv import load_dotenv
import tempfile

load_dotenv()

st.title("Chat With Your PDF")
st.write("Upload your text pdf and chat with it")

# -------- Upload PDF -------- #
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file is not None:

    # Save temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        file_path = tmp.name

    # --------load the pdf----------------#
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    print("Docs:", len(docs))  # ✅ debug

    #-----------split the pdf------------#
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    splitted_data = splitter.split_documents(docs)

    print("Chunks:", len(splitted_data))  # ✅ debug

    # ✅ FIX (only added, no change in structure)
    if len(splitted_data) == 0:
        st.error("No readable text found in PDF!")
        st.stop()

    #-----------embeddings------------------#
    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

    #-----------------vector store------------------------#
    vector_store = Chroma.from_documents(
        documents=splitted_data,
        embedding=embeddings
    )

    #---------------llm-------------------#
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

    #---------------context---------------#
    def get_context(query: str):
        data = vector_store.similarity_search(query=query)
        context = ""
        for doc in data:
            context += doc.page_content

        return {
            "context": context,
            "question": query
        }

    #-----------------------prompt--------------------#
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are a helpful AI assistant.
Answer the question based only on the context below.

context:{context}
question:{question}
"""
    )

    #----------------------rag pipeline--------------------#
    rag_chain = get_context | prompt | llm

    # -------- Input -------- #
    query = st.text_input("Ask something")

    if query:
        res = rag_chain.invoke(query)
        st.write("ai:", res.content)