from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os
from .ingestion import load_document, chunk_text
from .database import add_documents, get_retriever, reset_database
from .rag import generate_answer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str
    session_id: str = "default"

# In-memory session storage
# Format: {session_id: [(question, answer), ...]}
sessions = {}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_location = f"temp_{file.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Load and chunk using LangChain
        documents = load_document(file_location)
        chunks = chunk_text(documents)
        
        # Add metadata source if missing
        for chunk in chunks:
            if "source" not in chunk.metadata:
                chunk.metadata["source"] = file.filename
                
        add_documents(chunks)
        
        os.remove(file_location)
        return {"message": "File processed and indexed successfully", "filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
async def query_knowledge_base(request: QueryRequest):
    try:
        # Get retriever from vector store
        retriever = get_retriever()
        
        # Get chat history for session
        chat_history = sessions.get(request.session_id, [])
        
        # Generate answer using RAG chain with history
        result = generate_answer(request.question, retriever, chat_history)
        
        # Update chat history
        chat_history.append((request.question, result["answer"]))
        sessions[request.session_id] = chat_history
        
        return {"answer": result["answer"], "sources": result["sources"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reset")
async def reset_knowledge_base():
    try:
        reset_database()
        return {"message": "Knowledge base reset successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount static files for frontend
# We mount this LAST so it doesn't override the API routes
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if not os.path.exists(frontend_dir):
    os.makedirs(frontend_dir)
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
