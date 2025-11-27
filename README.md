# AI Knowledge Base Agent

## Overview
The **AI Knowledge Base Agent** is an intelligent document assistant designed to bridge the gap between static documents and dynamic information retrieval. By leveraging **RAG (Retrieval-Augmented Generation)**, it allows users to upload PDF or Text documents and ask natural language questions about them.

Unlike generic AI models, this agent grounds its answers strictly in the provided content, ensuring accuracy and relevance for specific use cases like HR policies, technical manuals, or legal contracts.

---

## Features & Limitations

### Features
*   **Document Ingestion**: Upload and process PDF and TXT files instantly.
*   **Context-Aware Answers**: Uses RAG to find the exact section of your document relevant to your question.
*   **Source Citations**: Provides transparency by citing the source of the information.
*   **Local Privacy**: Uses local embeddings (HuggingFace) so your document vectors are generated on your machine.
*   **Modern UI**: Built with Streamlit for a clean, dark-mode chat interface.
*   **Cost-Effective**: Uses Google Gemini 1.5 Flash for high-speed, low-cost inference.

### Limitations
*   **Single File Upload**: Currently optimized for processing one file at a time (though the backend supports multiple).
*   **Text-Only Analysis**: Does not currently extract data from images or tables within PDFs (OCR is not implemented).
*   **Session Memory**: Chat history is session-based and clears when you refresh the page.

---

## Tech Stack & APIs

*   **Frontend**: [Streamlit](https://streamlit.io/) (Pure Python UI)
*   **Framework**: [LangChain](https://www.langchain.com/) (Orchestration)
*   **LLM**: [Google Gemini 2.5 Flash](https://ai.google.dev/) (via `langchain-google-genai`)
*   **Embeddings**: [HuggingFace](https://huggingface.co/) `all-MiniLM-L6-v2` (Local execution)
*   **Vector Database**: [ChromaDB](https://www.trychroma.com/) (Local persistence)

---

## Setup & Run Instructions

### Prerequisites
*   Python 3.10 or higher
*   A Google Cloud API Key (for Gemini)

### Installation

1.  **Clone the Repository**
    ```bash
    git clone <your-repo-url>
    cd AI_Knowledge_Base_Agent
    ```

2.  **Create a Virtual Environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r backend/requirements.txt
    ```

4.  **Set Up Environment Variables**
    Create a `.env` file in `backend/.env` and add your API key:
    ```bash
    GOOGLE_API_KEY=your_api_key_here
    ```

### Running the App
```bash
streamlit run app.py
```
The application will launch automatically at `http://localhost:8501`.

---

## Potential Improvements
*   **Multi-File Support**: Allow uploading entire folders or multiple PDFs at once.
*   **OCR Integration**: Add support for scanned documents and images using Tesseract or specialized models.
*   **Chat History Persistence**: Save chat history to a database (SQLite/Postgres) to resume conversations later.
*   **Docker Support**: Containerize the application for easier deployment.
*   **Advanced RAG**: Implement "Hybrid Search" (Keyword + Vector) for better retrieval accuracy.


---

## Architecture Diagram

```mermaid
graph TD
    User([User]) <--> UI[Streamlit App]
    
    subgraph "Frontend Layer"
        UI
    end
    
    subgraph "Backend Logic"
        Ingest[Ingestion Module]
        Chunk[Text Splitter]
        Embed[HuggingFace Embeddings]
        VectorDB[(ChromaDB)]
        RAG[RAG Chain]
        LLM[Gemini 1.5 Flash]
    end
    
    UI -- "1. Upload PDF/Txt" --> Ingest
    Ingest --> Chunk
    Chunk --> Embed
    Embed -- "2. Store Vectors" --> VectorDB
    
    UI -- "3. Ask Question" --> RAG
    RAG -- "4. Embed Query" --> Embed
    Embed -- "5. Retrieve Context" --> VectorDB
    VectorDB -- "6. Return Chunks" --> RAG
    RAG -- "7. Prompt + Context" --> LLM
    LLM -- "8. Answer" --> UI
```

---