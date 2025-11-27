from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

def load_document(file_path: str) -> list:
    """Extracts text from a PDF or TXT file using LangChain loaders."""
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith(".txt"):
        loader = TextLoader(file_path)
    else:
        raise Exception("Unsupported file format. Please upload PDF or TXT.")
    
    return loader.load()

def chunk_text(documents: list, chunk_size: int = 1000, overlap: int = 100) -> list:
    """Splits text into chunks using LangChain splitter."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap
    )
    return text_splitter.split_documents(documents)
