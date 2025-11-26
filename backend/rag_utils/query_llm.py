from rag_utils.embeddings import get_embedding
import numpy as np
from phi import OllamaLLM 

# Initialize Phi LLM
llm = OllamaLLM(model="phi")  

# Example documents (later replace with PDF chunks)
documents = [
    {"id": 1, "text": "Hello world, this is a test document."},
    {"id": 2, "text": "Ollama is a local LLM you can run."},
    {"id": 3, "text": "RAG allows you to answer questions from documents."},
]

# Compute embeddings for all documents
for doc in documents:
    doc["embedding"] = get_embedding(doc["text"])

# Step 1: Find most relevant document(s)
def get_most_similar_doc(query, docs, top_k=1):
    query_emb = get_embedding(query)
    similarities = []
    for doc in docs:
        sim = np.dot(query_emb, doc["embedding"])  # cosine-ish similarity
        similarities.append((doc, sim))
    similarities.sort(key=lambda x: x[1], reverse=True)
    return [doc for doc, sim in similarities[:top_k]]

# Step 2: RAG answer using Phi
def rag_answer(query):
    top_doc = get_most_similar_doc(query, documents)[0]
    context = top_doc["text"]

    prompt = f"""
    Answer the user query based on the following document:

    Document: {context}

    User Query: {query}

    Answer:
    """
    response = llm.generate(prompt)
    return response.text  # Phi returns an object; .text extracts the answer

# Example test
if __name__ == "__main__":
    query = "What is RAG?"
    print(rag_answer(query))
