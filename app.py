import streamlit as st
import os
import shutil
from backend.ingestion import load_document, chunk_text
from backend.database import add_documents, get_retriever
from backend.rag import generate_answer

# Page Config
st.set_page_config(
    page_title="AI Knowledge Base Agent",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for premium look
st.markdown("""
<style>
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    .stSidebar {
        background-color: #1e293b;
    }
    .stTextInput > div > div > input {
        background-color: #1e293b;
        color: #f8fafc;
        border: 1px solid #334155;
    }
    .stButton > button {
        background-color: #3b82f6;
        color: white;
        border: none;
        border-radius: 8px;
    }
    .stButton > button:hover {
        background-color: #2563eb;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
    }
    .chat-message.user {
        background-color: #1e293b;
        border: 1px solid #334155;
    }
    .chat-message.bot {
        background-color: #334155;
        border: 1px solid #475569;
    }
    .chat-message .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        margin-right: 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
    }
    .chat-message .content {
        flex: 1;
    }
    .source-box {
        font-size: 0.8rem;
        color: #94a3b8;
        margin-top: 0.5rem;
        padding-top: 0.5rem;
        border-top: 1px solid #475569;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar - File Upload
with st.sidebar:
    st.title("Document Upload")
    uploaded_file = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])
    
    if uploaded_file:
        if st.button("Process Document"):
            with st.spinner("Processing..."):
                try:
                    # Save temp file
                    file_location = f"temp_{uploaded_file.name}"
                    with open(file_location, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Process
                    documents = load_document(file_location)
                    chunks = chunk_text(documents)
                    
                    # Add metadata
                    for chunk in chunks:
                        if "source" not in chunk.metadata:
                            chunk.metadata["source"] = uploaded_file.name
                            
                    add_documents(chunks)
                    
                    # Cleanup
                    os.remove(file_location)
                    st.success(f"Successfully indexed {uploaded_file.name}!")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# Main Chat Interface
st.title("🤖 AI Knowledge Base Agent")
st.markdown("Ask questions about your uploaded documents.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    sources = message.get("sources", [])
    
    with st.chat_message(role):
        st.markdown(content)
        if sources:
            with st.expander("View Sources"):
                for source in sources:
                    st.markdown(f"**{source['source']}**: {source['text']}")

# Chat Input
if prompt := st.chat_input("Ask a question..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                retriever = get_retriever()
                result = generate_answer(prompt, retriever)
                response = result["answer"]
                sources = result["sources"]
                
                st.markdown(response)
                if sources:
                    with st.expander("View Sources"):
                        for source in sources:
                            st.markdown(f"**{source['source']}**: {source['text']}")
                
                # Add assistant message
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response,
                    "sources": sources
                })
            except Exception as e:
                st.error(f"Error generating answer: {str(e)}")
