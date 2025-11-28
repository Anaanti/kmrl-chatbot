# query_llm.py
import os
import subprocess
import json
from dotenv import load_dotenv
import psycopg2
from sentence_transformers import SentenceTransformer
from math import sqrt

# ---------------------------
# Load environment variables
# ---------------------------
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# ---------------------------
# Postgres connection
# ---------------------------
def get_conn():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

# ---------------------------
# LLM (Ollama) function
# ---------------------------
def ask_llm(prompt: str, timeout: int = 30) -> str:
    payload = json.dumps({"prompt": prompt})
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3"],
            input=payload,
            capture_output=True,
            text=True,
            check=True,
            encoding="utf-8",
            timeout=timeout
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "LLM call timed out."
    except subprocess.CalledProcessError as e:
        return f"Error calling LLM: {e}\nOutput: {e.output}\nStderr: {e.stderr}"

# ---------------------------
# Embedding model
# ---------------------------
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: str) -> list:
    return embed_model.encode(text).tolist()

# ---------------------------
# Euclidean distance
# ---------------------------
def euclidean(a, b):
    return sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

# ---------------------------
# Query documents from DB
# ---------------------------
def query_documents(user_query, top_k=5):
    vec = get_embedding(user_query)
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT doc_name, content, embeddings FROM document_embedding;")
    rows = cur.fetchall()
    results = []

    for doc_name, content, embeddings in rows:
        try:
            # Convert Postgres vector to list of floats
            if isinstance(embeddings, str):
                embeddings = [float(x) for x in embeddings.strip("[]").split(",")]
            dist = euclidean(vec, embeddings)
            results.append({"doc_name": doc_name, "content": content, "similarity": dist})
        except Exception as e:
            print(f"Skipping {doc_name} due to error: {e}")

    # Sort by smallest distance (closest match)
    results.sort(key=lambda x: x["similarity"])
    return results[:top_k]

# ---------------------------
# Get answer using LLM
# ---------------------------
def answer_query(user_query, top_k=5):
    top_docs = query_documents(user_query, top_k)
    context = "\n\n".join([doc['content'] for doc in top_docs])
    prompt = f"Answer the question using the context below:\n\n{context}\n\nQuestion: {user_query}"
    answer = ask_llm(prompt)
    return {"answer": answer, "sources": top_docs}

# ---------------------------
# Optional test
# ---------------------------
if __name__ == "__main__":
    q = "tell me about Git"
    res = query_documents(q, top_k=3)
    print("Top docs:")
    for r in res:
        print(r["doc_name"], r["similarity"])
    ans = answer_query(q)
    print("\nAnswer:", ans["answer"])
    print("Sources:")
    for src in ans["sources"]:
        print(src["doc_name"])
