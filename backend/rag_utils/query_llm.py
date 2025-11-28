import os
import random
import json
import subprocess
import psycopg2
from dotenv import load_dotenv
import ast
# Load .env file
load_dotenv()

# ---------------------------
# Database connection
# ---------------------------
def get_conn():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
    )

# ---------------------------
# LLM function (CLI-based)
# ---------------------------
def ask_llm(prompt: str) -> str:
    payload = json.dumps({"prompt": prompt})
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3"],
            input=payload,
            capture_output=True,
            text=True,
            check=True,
            encoding="utf-8"
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error calling LLM: {e}\nOutput: {e.output}\nStderr: {e.stderr}"

# ---------------------------
# Embedding function
# ---------------------------
def get_embedding(text: str) -> list:
    # Mock embedding (384-dim vector)
    return [random.random() for _ in range(384)]

# ---------------------------
# Query documents
# ---------------------------
import ast  # for safely evaluating stringified lists

def query_documents(user_query: str, top_k: int = 5):
    vec = get_embedding(user_query)
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT id, doc_name, content, embeddings FROM document_embedding;")
    rows = cur.fetchall()

    def euclidean(a, b):
        # if b is string, parse it into a list
        if isinstance(b, str):
            b = ast.literal_eval(b)
        b = [float(x) for x in b]  # ensure floats
        return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5

    results = []
    for row in rows:
        doc_id, doc_name, content, embeddings = row
        distance = euclidean(vec, embeddings)
        results.append({"doc_name": doc_name, "content": content, "similarity": distance})

    results.sort(key=lambda x: x["similarity"])
    return results[:top_k]


# ---------------------------
# Answer query using top documents
# ---------------------------
def answer_query(user_query: str, top_k: int = 5):
    top_docs = query_documents(user_query, top_k=top_k)
    context = "\n\n".join([doc['content'] for doc in top_docs])
    answer = ask_llm(f"Answer the question using the context below:\n\n{context}\n\nQuestion: {user_query}")
    return {"answer": answer, "sources": top_docs}

# ---------------------------
# Optional quick test
# ---------------------------
if __name__ == "__main__":
    print("LLM output:", ask_llm("What is KMRL?"))
    print("Embedding length:", len(get_embedding("Hello world")))
    docs = query_documents("What is KMRL?", top_k=3)
    print("Top docs:", docs)
