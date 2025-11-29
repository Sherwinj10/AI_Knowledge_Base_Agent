# AI Knowledge Base Agent

An intelligent document assistant capable of ingesting, retrieving, and answering questions from PDF and Text documents using Retrieval-Augmented Generation (RAG) with session memory.

## Overview
The **AI Knowledge Base Agent** is designed to bridge the gap between static documents and dynamic information retrieval. By leveraging **RAG**, it allows users to upload PDF or Text documents and ask natural language questions about them.

Unlike generic AI models, this agent grounds its answers strictly in the provided content, ensuring accuracy and relevance for specific use cases like HR policies, technical manuals, or legal contracts.

## Features & Limitations

### Features
*   **Document Ingestion**: Supports **PDF** and **TXT** files using LangChain's `PyPDFLoader` and `TextLoader`.
*   **Context-Aware Answers**: Uses RAG to retrieve relevant document chunks for accurate answering.
*   **Structured Output**: Answers are formatted with bullet points, a summary, and confidence levels.
*   **Source Citations**: Provides transparency by citing the specific document chunks used.
*   **Local Privacy**: Uses local **HuggingFace embeddings** (`all-MiniLM-L6-v2`) to generate vectors on your machine.
*   **Modern UI**: Built with a clean **HTML/JS Frontend** and a fast **FastAPI Backend**.
*   **Cost-Effective**: Uses **Google Gemini 2.5 Flash** for high-speed, low-cost inference.

### Limitations
*   **Text-Only Analysis**: Currently extracts text only; does not process images or tables within PDFs (no OCR).
*   **Single File Upload**: Optimized for processing one file at a time.
*   **Session Memory**: Chat history is session-based and clears when you refresh the page.

## Tech Stack & APIs Used

*   **Frontend**: HTML, CSS, JavaScript (Vanilla)
*   **Backend**: [FastAPI](https://fastapi.tiangolo.com/) (Python)
*   **Ingestion**: [LangChain](https://www.langchain.com/) (PyPDFLoader, TextLoader)
*   **LLM**: [Google Gemini 2.5 Flash](https://ai.google.dev/) (via `langchain-google-genai`)
*   **Embeddings**: [HuggingFace](https://huggingface.co/) `all-MiniLM-L6-v2` (Local execution)
*   **Vector Database**: [ChromaDB](https://www.trychroma.com/) (Local persistence)

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
    GOOGLE_API_KEY=your_google_key
    ```

### Running the App
1.  **Start the Backend Server**:
    ```bash
    uvicorn backend.main:app --reload
    ```
2.  **Access the App**:
    Open your browser and navigate to `http://localhost:8000`.

## Potential Improvements
*   **Multi-File Support**: Allow uploading entire folders or multiple PDFs at once.
*   **OCR Integration**: Add support for scanned documents and images using Tesseract or specialized models.
*   **Chat History Persistence**: Save chat history to a database (SQLite/Postgres).
*   **Docker Support**: Containerize the application for easier deployment.

## Architecture Diagram

```mermaid
graph TD
    subgraph Ingestion
        A[PDF/TXT Document] -->|PyPDFLoader/TextLoader| B(Raw Text)
        B -->|RecursiveSplitter| C[Text Chunks]
    end

    subgraph Embedding & Storage
        C -->|HuggingFace Embeddings| D[(ChromaDB)]
    end

    subgraph Retrieval & Generation
        E[User Query] -->|Embed| F[Query Embedding]
        F -->|Vector Search| D
        D -->|Retrieve Top-k| G[Relevant Context]
        G -->|Context + Query| H[Gemini 2.5 Flash]
        H -->|Generate| I[Structured Answer]
    end
    
    subgraph UI
        J[Frontend (HTML/JS)] <-->|API| K[Backend (FastAPI)]
        K <--> H
    end
```