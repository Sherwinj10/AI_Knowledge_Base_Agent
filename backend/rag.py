from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

from langchain.prompts import PromptTemplate

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)

def generate_answer(query: str, retriever, chat_history: list) -> dict:
    
    # Custom prompt template
    template = """You are a Knowledge Base Answering Agent.

    Always return output in the following structured format.
    Do not merge sections. Do not return prose paragraphs.

    Answer:
    • Short bullet points only
    • Direct factual statements
    • No paragraph responses

    Steps (if process/procedure is involved):
    1. Step one
    2. Step two
    3. Step three
    (continue until complete)

    Summary:
    One short sentence summarizing the entire answer.

    Evidence:
    • Quote the lines used from context with metadata

    Confidence:
    High / Medium / Low
    
    Context:
    {context}
    
    Question: {question}
    
    Now generate the formatted answer exactly in this structure.
    
    Answer:"""
    
    QA_PROMPT = PromptTemplate(template=template, input_variables=["context", "question"])

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        verbose=False,
        chain_type="stuff",
        combine_docs_chain_kwargs={"prompt": QA_PROMPT}
    )

    result = qa_chain.invoke({"question": query, "chat_history": chat_history})

    answer = result["answer"]
    docs = result["source_documents"]

    # Compute confidence by chunk agreement
    matched_chunks = [doc.page_content for doc in docs]
    overlap = sum(answer.lower() in chunk.lower() or chunk.lower() in answer.lower()
                  for chunk in matched_chunks)

    confidence = "High" if overlap >= 2 else "Medium" if overlap == 1 else "Low"

    formatted = {
        "answer": answer,
        "sources": [
            {
                "text": doc.page_content[:400] + "...",  # compress chunk for readability
                "source": doc.metadata.get("source", "Unknown")
            } for doc in docs
        ],
        "confidence": confidence
    }

    return formatted

