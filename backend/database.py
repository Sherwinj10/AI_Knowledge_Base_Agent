from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Embeddings
# Using local HuggingFace embeddings to avoid API rate limits
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Initialize Vector Store
# LangChain's Chroma wrapper handles persistence
vector_store = Chroma(
    collection_name="documents",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

def add_documents(chunks: list):
    """Adds document chunks to the vector store."""
    vector_store.add_documents(documents=chunks)

def get_retriever():
    """Returns a retriever object for the vector store."""
    return vector_store.as_retriever(search_kwargs={"k": 5})

def reset_database():
    """Clears the vector store by deleting the persistence directory."""
    global vector_store
    import shutil
    
    if os.path.exists("./chroma_db"):
        shutil.rmtree("./chroma_db")
    
    # Re-initialize
    vector_store = Chroma(
        collection_name="documents",
        embedding_function=embeddings,
        persist_directory="./chroma_db"
    )
