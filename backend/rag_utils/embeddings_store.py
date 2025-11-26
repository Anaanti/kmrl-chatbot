from rag_utils.embeddings import get_embedding

# Example documents
documents = [
    {"id": 1, "text": "Hello world, this is a test document."},
    {"id": 2, "text": "Ollama is a local LLM you can run."},
    {"id": 3, "text": "RAG allows you to answer questions from documents."},
]

# Compute embeddings and store
for doc in documents:
    doc["embedding"] = get_embedding(doc["text"])
