from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)

def generate_answer(query: str, retriever) -> dict:
    """Generates an answer using LangChain's RetrievalQA chain."""
    
    # Custom prompt template to ensure citations
    template = """Use the following pieces of context to answer the question at the end. 
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Always cite the source of your answer based on the context provided.
    
    Context:
    {context}
    
    Question: {question}
    
    Answer:"""
    
    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )
    
    result = qa_chain.invoke({"query": query})
    
    # Format output to match previous API contract
    answer = result["result"]
    source_documents = result["source_documents"]
    
    formatted_sources = []
    for doc in source_documents:
        formatted_sources.append({
            "text": doc.page_content,
            "source": doc.metadata.get("source", "Unknown")
        })
        
    return {"answer": answer, "sources": formatted_sources}
