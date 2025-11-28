# rag_utils/test_retrieval.py

from rag_utils.query_llm import answer_query, query_documents

def run_test():
    query = input("Enter your query: ")

    # Step 1: Retrieve top chunks
    top_chunks = query_documents(query, top_k=3)
    print("\nTop chunks:")
    print("-" * 40)
    for chunk in top_chunks:
        print(f"Document: {chunk['doc_name']}")
        print(f"Distance: {chunk['similarity']}")
        snippet = chunk['content'][:300]  # preview first 300 chars
        print(f"Content snippet: {snippet}")
        print("\n" + "-" * 40)

    # Step 2: Generate LLM answer
    answer = answer_query(query, top_k=3)
    print("\nGenerated Answer:\n")
    print(answer["answer"])

if __name__ == "__main__":
    run_test()
