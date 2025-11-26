from rag_utils.vector_store import query_documents
from rag_utils.embeddings import get_embedding

documents = load_all_pdfs()

question = input("Ask a question: ")
results = query_documents(question, documents, top_k=2)

print("\nMost relevant document(s):")
for doc, score in results:
    print(f"\nScore: {score:.3f}")
    print(f"Chunk Text:\n{doc['text'][:300]}...")