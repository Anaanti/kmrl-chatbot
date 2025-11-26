from ollama import Ollama
from rag_utils.vector_store import query_documents

client = Ollama(model="phi")  # Your local LLM

def ask_ollama(query):
    # Step 1: Get top 2 relevant documents
    docs = query_documents(query, top_k=2)
    
    # Step 2: Combine their text
    context = "\n".join([doc["text"] for doc in docs])
    
    # Step 3: Formulate prompt
    prompt = f"Answer the question based on the following documents:\n{context}\n\nQuestion: {query}"
    
    # Step 4: Get response
    response = client.chat(prompt)
    return response
